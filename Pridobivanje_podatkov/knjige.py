import csv
import os
import requests
import re
import math

###############################################################################
# Najprej definirajmo nekaj pomožnih orodij za pridobivanje podatkov s spleta.
###############################################################################
SKUPNO_ST_KNJIG = 100
ST_KNJIG_NA_STRAN = 100 #konstantno, ne moremo spremeniti
ST_STRANI = math.ceil(SKUPNO_ST_KNJIG / ST_KNJIG_NA_STRAN)



# definiratje URL glavne strani goodreads z najboljšimi knjigami
book_frontpage_url = 'https://www.goodreads.com/list/show/1.Best_Books_Ever?page={}'
book_subpage_url = 'https://www.goodreads.com/book/show/{}'
# mapa, v katero bomo shranili podatke
book_directory = 'Pridobivanje_podatkov'
# ime datoteke v katero bomo shranili glavno stran
frontpage_filename = 'best_books.html'
subpage_filename = 'book_subpage.html'
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







# def read_file_to_string(directory, filename):
#     """Funkcija vrne celotno vsebino datoteke "directory"/"filename" kot niz"""
#     path = os.path.join(directory, filename)
#     with open(path, 'r', encoding='utf-8') as file_in:
#         return file_in.read()


# Definirajte funkcijo, ki sprejme niz, ki predstavlja vsebino spletne strani,
# in ga razdeli na dele, kjer vsak del predstavlja en oglas. To storite s
# pomočjo regularnih izrazov, ki označujejo začetek in konec posameznega
# oglasa. Funkcija naj vrne seznam nizov.


# def page_to_books(page_content):
#     """Funkcija poišče posamezne knjige, ki se nahajajo v spletni strani in
#     vrne njih seznam"""
#     rx = re.compile(r'<li class="EntityList-item EntityList-item--Regular'
#                     r'(.*?)</article>',
#                     re.DOTALL)
#     books = re.findall(rx, page_content)
#     return books


# Definirajte funkcijo, ki sprejme niz, ki predstavlja oglas, in izlušči
# podatke o imenu, ceni in opisu v oglasu.


def get_dict_from_ad_block(block):
    """Funkcija iz niza za posamezno knjigo izlušči podatke ter vrne slovar,
     ki te podatke vsebuje"""
    rx = re.compile(#avtor:
                    r'<span itemprop="name">(?P<avtor>.+)<\/span>'
                    #naslov:
                    r'<h1 id="bookTitle".*itemprop="name">\s*(?P<naslov>.*)\s*<\/h1>'
                    #id knjige
                    r'ISBN13: <span itemprop=\'isbn\'>(?P<id_knjige>\d{13})'
                    #naslov serije TO DO:ce ne najde ti sporoci, da ves, da ni serija(stevilko v seriji nekam zapise)
                    r'<a class="greyText" href="\/series\/.*\s*\((?P<naslov_serije>.*)\)\s*<\/a>'
                    #ocena od 1 do 5
                    r'<span itemprop="ratingValue">\n*\s*(?P<ocena1do5>.+)\n*<\/span>'
                    #leto izdaje in zalozba 
                    r'<div class="row">\s*Published\s*.*(?P<datum>\d{4})\s*by\s*(?P<zalozba>.*)\s*<\/div>'
                    #ven vrze v obliki:[('2008', 'Scholastic Press')]
                    #stevilo ratingov(ocen)
                    r'<meta itemprop="ratingCount" content="(?P<ratings>\d*)"\s*\/>'
                    #stevilo reviewov
                    r'<meta itemprop="reviewCount" content="(?P<reviews>\d*)"\s*\/>'
                    #zanri + st glasov za ta zanr
                    r'(?P<st_ocen_zanra>\d+) people shelved this book as &#39;(?P<zanr>.+)&#39;'
                    #nagrade(+leto)
                    r'award\/show\/.*?>(?P<nagrade>.+?)\((?P<leto_nagrade>\d*)\)<\/a>',
                    re.DOTALL)
    data = re.search(rx, block)
    ad_dict = data.groupdict()

    return ad_dict


# Definirajte funkcijo, ki sprejme ime in lokacijo datoteke, ki vsebuje
# besedilo spletne strani, in vrne seznam slovarjev, ki vsebujejo podatke o
# vseh oglasih strani.


# def ads_from_file(filename, directory):
#     """Funkcija prebere podatke v datoteki "directory"/"filename" in jih
#     pretvori (razčleni) v pripadajoč seznam slovarjev za vsak oglas posebej."""
#     page = read_file_to_string(filename, directory)
#     blocks = page_to_books(page)
#     ads = [get_dict_from_ad_block(block) for block in blocks]
#     return ads

# def ads_frontpage():
#     return ads_from_file(book_directory, frontpage_filename)
###############################################################################
# Obdelane podatke želimo sedaj shraniti.
###############################################################################


# def write_csv(fieldnames, rows, directory, filename):
#     """
#     Funkcija v csv datoteko podano s parametroma "directory"/"filename" zapiše
#     vrednosti v parametru "rows" pripadajoče ključem podanim v "fieldnames"
#     """
#     os.makedirs(directory, exist_ok=True)
#     path = os.path.join(directory, filename)
#     with open(path, 'w') as csv_file:
#         writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#         writer.writeheader()
#         for row in rows:
#             writer.writerow(row)
#     return


# Definirajte funkcijo, ki sprejme neprazen seznam slovarjev, ki predstavljajo
# podatke iz oglasa mačke, in zapiše vse podatke v csv datoteko. Imena za
# stolpce [fieldnames] pridobite iz slovarjev.


# def write_cat_ads_to_csv(ads, directory, filename):
#     """Funkcija vse podatke iz parametra "ads" zapiše v csv datoteko podano s
#     parametroma "directory"/"filename". Funkcija predpostavi, da sa ključi vseh
#     sloverjev parametra ads enaki in je seznam ads neprazen.

#     """
#     # Stavek assert preveri da zahteva velja
#     # Če drži se program normalno izvaja, drugače pa sproži napako
#     # Prednost je v tem, da ga lahko pod določenimi pogoji izklopimo v
#     # produkcijskem okolju
#     assert ads and (all(j.keys() == ads[0].keys() for j in ads))
#     write_csv(ads[0].keys(), ads, directory, filename)


# Celoten program poženemo v glavni funkciji

def main(redownload=True, reparse=True):
    """Funkcija izvede celoten del pridobivanja podatkov:
    1. Oglase prenese iz bolhe
    2. Lokalno html datoteko pretvori v lepšo predstavitev podatkov
    3. Podatke shrani v csv datoteko
    """
    # Najprej v lokalno datoteko shranimo eno od glavnih strani
    for i in range(1, ST_STRANI + 1):
        #shranimo eno od strani, ki jih moramo analizirati
        save_frontpage(book_frontpage_url.format(i), book_directory, frontpage_filename)
        #iz te strani poberemo podatke, ki jih ne najdemo na podstrani posamezne knjige in url, ki
        #nas bo peljal na podstran vsake knjige, da dobimo ostale podatke
        with open(r"C:\Users\Ana Julija\Documents\Najbolj-e-knjige-vseh-asov\Pridobivanje_podatkov\best_books.html", "r", encoding="utf-8") as s:    
            string = s.read()
            avtorji_ime = re.findall(r'itemprop="name">(.+)<\/span>', string)
            avtorji_id = re.findall(r'author\/show\/(\d+)', string)
            score = re.findall(r'score: (.+)<\/a>', string)
            st_glasov = re.findall(r'false;">(.+) people voted<\/a>', string)
            #url vsake podstrani se ponovi 2x, zato odstranimo ponovitev
            urlji = list(set(re.findall(r'href=[\'"]?\/book\/show\/([^\'" >]+)', string)))
        #sedaj moramo prenesti podstran vsake knjige:
        #v datoteko shranimo podstran ene knjige, pridobimo podatke in jih nekam shranimo, 
        #nato pa shranimo naslednjo podstran in povozimo prejsnjo datoteko
        for j in range(ST_KNJIG_NA_STRAN):
            save_frontpage(book_subpage_url.format(urlji[j]), book_directory, subpage_filename)
            with open("subpage_filename", "r", encoding="utf-8") as sub:
                besedilo = sub.read()
                slovar = get_dict_from_ad_block(besedilo)
                slovar['avtor_id'] = avtorji_id[j]
                slovar['score'] = score[j]
                slovar['st_glasov'] = st_glasov[j]
                print(slovar)




        





if __name__ == '__main__':
    main()
