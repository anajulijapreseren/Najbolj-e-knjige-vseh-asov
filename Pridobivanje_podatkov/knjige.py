import csv
import os
import requests
import re

###############################################################################
# Najprej definirajmo nekaj pomožnih orodij za pridobivanje podatkov s spleta.
###############################################################################

# definiratje URL glavne strani bolhe za oglase z mačkami
book_frontpage_url = 'https://www.goodreads.com/list/show/1.Best_Books_Ever?page=1'
# mapa, v katero bomo shranili podatke
book_directory = 'Pridobivanje_podatkov'
# ime datoteke v katero bomo shranili glavno stran
frontpage_filename = 'best_books.html'
# ime CSV datoteke v katero bomo shranili podatke
csv_filename = 'best_books.csv'


def download_url_to_string(url):
    """Funkcija kot argument sprejme niz in puskuša vrniti vsebino te spletne
    strani kot niz. V primeru, da med izvajanje pride do napake vrne None.
    """
    try:
        # del kode, ki morda sproži napako
        page_content = requests.get(url)
    except requests.exceptions.ConnectionError as e:
        # koda, ki se izvede pri napaki
        # dovolj je če izpišemo opozorilo in prekinemo izvajanje funkcije
        print("Prislo je do napake pri povezovanju")
        print(e)
        return None

    #status code(200,404..)
    if page_content.status_code == requests.codes.ok:#ni bilo napake
        return page_content.text

    # nadaljujemo s kodo če je prišlo do napake
    print("Težava pri vsebini strani")
    return None
    



def save_string_to_file(text, directory, filename):
    """Funkcija zapiše vrednost parametra "text" v novo ustvarjeno datoteko
    locirano v "directory"/"filename", ali povozi obstoječo. V primeru, da je
    niz "directory" prazen datoteko ustvari v trenutni mapi.
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None


# Definirajte funkcijo, ki prenese glavno stran in jo shrani v datoteko.


def save_frontpage(page, directory, filename):
    """Funkcija shrani vsebino spletne strani na naslovu "page" v datoteko
    "directory"/"filename"."""

    html = download_url_to_string(page)
    if html: #Če ni "" ali če ni None
        save_string_to_file(html, directory, filename)
        return True
    raise NotImplementedError()


###############################################################################
# Po pridobitvi podatkov jih želimo obdelati.
###############################################################################


def read_file_to_string(directory, filename):
    """Funkcija vrne celotno vsebino datoteke "directory"/"filename" kot niz"""
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as file_in:
        return file_in.read()


# Definirajte funkcijo, ki sprejme niz, ki predstavlja vsebino spletne strani,
# in ga razdeli na dele, kjer vsak del predstavlja en oglas. To storite s
# pomočjo regularnih izrazov, ki označujejo začetek in konec posameznega
# oglasa. Funkcija naj vrne seznam nizov.


def page_to_books(page_content):
    """Funkcija poišče posamezne knjige, ki se nahajajo v spletni strani in
    vrne njih seznam"""
    rx = re.compile(r'<li class="EntityList-item EntityList-item--Regular'
                    r'(.*?)</article>',
                    re.DOTALL)
    books = re.findall(rx, page_content)
    return books


# Definirajte funkcijo, ki sprejme niz, ki predstavlja oglas, in izlušči
# podatke o imenu, ceni in opisu v oglasu.


def get_dict_from_ad_block(block):
    """Funkcija iz niza za posamezen oglasni blok izlušči podatke o imenu, ceni
    in opisu ter vrne slovar, ki vsebuje ustrezne podatke
    """
    rx = re.compile(r'<h3.*>(?P<name>.*?)</a></h3>'
                    r'.*?"pubdate">(?P<time>.*?)</time>'
                    r'.*?<strong class="price price--hrk">\s*?(?P<price>.*?)(&|</strong>)',
                    re.DOTALL)
    data = re.search(rx, block)
    #print(data)
    #print(block)
    ad_dict = data.groupdict()


    # Ker nimajo vsi oglasi podatka o lokaciji, to rešimo z dodatnim vzorcem
    rloc = re.compile(r'Lokacija: </span>(?P<location>.*?)<br />')
    locdata = re.search(rloc, block)
    if locdata is not None:
        ad_dict['location'] = locdata.group('location')
    else:
        ad_dict['location'] = 'Unknown'

    return ad_dict


# Definirajte funkcijo, ki sprejme ime in lokacijo datoteke, ki vsebuje
# besedilo spletne strani, in vrne seznam slovarjev, ki vsebujejo podatke o
# vseh oglasih strani.


def ads_from_file(filename, directory):
    """Funkcija prebere podatke v datoteki "directory"/"filename" in jih
    pretvori (razčleni) v pripadajoč seznam slovarjev za vsak oglas posebej."""
    page = read_file_to_string(filename, directory)
    blocks = page_to_books(page)
    ads = [get_dict_from_ad_block(block) for block in blocks]
    return ads

def ads_frontpage():
    return ads_from_file(book_directory, frontpage_filename)
###############################################################################
# Obdelane podatke želimo sedaj shraniti.
###############################################################################


def write_csv(fieldnames, rows, directory, filename):
    """
    Funkcija v csv datoteko podano s parametroma "directory"/"filename" zapiše
    vrednosti v parametru "rows" pripadajoče ključem podanim v "fieldnames"
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return


# Definirajte funkcijo, ki sprejme neprazen seznam slovarjev, ki predstavljajo
# podatke iz oglasa mačke, in zapiše vse podatke v csv datoteko. Imena za
# stolpce [fieldnames] pridobite iz slovarjev.


def write_cat_ads_to_csv(ads, directory, filename):
    """Funkcija vse podatke iz parametra "ads" zapiše v csv datoteko podano s
    parametroma "directory"/"filename". Funkcija predpostavi, da sa ključi vseh
    sloverjev parametra ads enaki in je seznam ads neprazen.

    """
    # Stavek assert preveri da zahteva velja
    # Če drži se program normalno izvaja, drugače pa sproži napako
    # Prednost je v tem, da ga lahko pod določenimi pogoji izklopimo v
    # produkcijskem okolju
    assert ads and (all(j.keys() == ads[0].keys() for j in ads))
    write_csv(ads[0].keys(), ads, directory, filename)


# Celoten program poženemo v glavni funkciji

def main(redownload=True, reparse=True):
    """Funkcija izvede celoten del pridobivanja podatkov:
    1. Oglase prenese iz bolhe
    2. Lokalno html datoteko pretvori v lepšo predstavitev podatkov
    3. Podatke shrani v csv datoteko
    """
    # Najprej v lokalno datoteko shranimo glavno stran
    save_frontpage(book_frontpage_url, book_directory, frontpage_filename)
    # Iz lokalne (html) datoteke preberemo podatke
    #ads = page_to_ads(read_file_to_string(cat_directory, frontpage_filename))
    # Podatke prebermo v lepšo obliko (seznam slovarjev)
    #ads_nice = [get_dict_from_ad_block(ad) for ad in ads]
    # Podatke shranimo v csv datoteko
    #write_cat_ads_to_csv(ads_nice, cat_directory, csv_filename)
    # Dodatno: S pomočjo parameteov funkcije main omogoči nadzor, ali se
    # celotna spletna stran ob vsakem zagon prense (četudi že obstaja)
    # in enako za pretvorbo

    #raise NotImplementedError()




if __name__ == '__main__':
    main()
