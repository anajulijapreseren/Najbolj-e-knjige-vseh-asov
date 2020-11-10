import csv
import os
import requests
import re
import math
import os.path

SKUPNO_ST_KNJIG = 100
ST_KNJIG_NA_STRAN = 100 #konstantno, ne moremo spremeniti
ST_STRANI = math.ceil(SKUPNO_ST_KNJIG / ST_KNJIG_NA_STRAN)

#URL glavne strani goodreads z najboljšimi knjigami
book_frontpage_url = 'https://www.goodreads.com/list/show/1.Best_Books_Ever?page={}'
#URL podstrani posamezne knjige
book_subpage_url = 'https://www.goodreads.com/book/show/{}'
# mapa, v katero bomo shranili podatke
book_directory = 'Pridobivanje_podatkov'
# ime datoteke, v katero bomo shranili glavno stran
frontpage_filename = 'best_books.html'
#ime datoteke, v katero bomo shranili podstran posamezne knjige
subpage_filename = 'book_subpage.html'
# ime CSV datoteke v katero bomo shranili podatke
csv_filename = 'best_books.csv'


#REGEX VZORCI:
vzorec_url = r'href=[\'"]?\/book\/show\/([^\'" >]+)'
vzorec_id_avtor = r'author\/show\/(\d+)'
vzorec_score = r'score: (.+)<\/a>'
vzorec_st_glasov = r'false;">(.+) people voted<\/a>'
vzorec_avtor = r'<span itemprop="name">(?P<avtor>[^<]+)<+?'                  
vzorec_knjiga = r'<h1 id="bookTitle".*itemprop="name">\s*(?P<knjiga>.*)\s*</h1>'
vzorec_serija = r'<a class="greyText" href="/series/.*\s*\((?P<naslov_serije>.*)\)\s*</a>'
vzorec_povprecna_ocena = r'<span itemprop="ratingValue">\n*\s*(?P<povprecna_ocena>.+)\n*</span>'
vzorec_leto = r'<div class="row">\s*Published\s*.*(?P<leto>\d{4})\s*by'
vzorec_zalozba = r'<div class="row">\s*Published\s*.*\d{4}\s*by (?P<zalozba>.*)\s+'
vzorec_st_ocen = r'<meta itemprop="ratingCount" content="(?P<ratings>\d*)"\s*/>'
vzorec_st_reviewov = r'<meta itemprop="reviewCount" content="(?P<reviews>\d*)"\s*/>'
vzorec_zanr = r'people shelved this book as &#39;(?P<zanr>.+)&#39;'
vzorec_st_ocen_zanra = r'(?P<st_ocen_zanra>\d+) people shelved this book as &#39;'
vzorec_nagrade = r'award/show/.*?>(?P<nagrade>.+?)\(\d*\)</a>'
vzorec_leto_nagrade = r'award/show/.*?>.+?\((?P<leto_nagrade>\d*)\)</a>'
vzorec_opis = r'<span id="freeText.*" style=".*">(?P<opis>.*?)</span>'



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


def save_frontpage(page, directory, filename):
    """Funkcija shrani vsebino spletne strani na naslovu "page" v datoteko
    "directory"/"filename"."""

    html = download_url_to_string(page)
    if html: #Če ni "" ali če ni None
        save_string_to_file(html, directory, filename)
        return True
    raise NotImplementedError()

def main(redownload=True, reparse=True):

    # Najprej v lokalno datoteko shranimo eno od glavnih strani
    for i in range(1, ST_STRANI + 1):
        id = 1
        #shranimo eno od strani, ki jih moramo analizirati
        #save_frontpage(book_frontpage_url.format(i), book_directory, frontpage_filename)
        #iz te strani poberemo podatke, ki jih ne najdemo na podstrani posamezne knjige in url, ki
        #nas bo peljal na podstran vsake knjige, da dobimo ostale podatke
    
        with open(r"C:\Users\Ana Julija\Documents\Najbolj-e-knjige-vseh-asov\Pridobivanje_podatkov\best_books.html", "r", encoding="utf-8") as s:    
            string = s.read()
            #podatke o avtorju, scoru in id-ju bomo potrebovali za csv, zato jih shranimo v list:
            id_avtor, score, st_glasov = [], [], []
            id_avtor.extend(re.findall(vzorec_id_avtor, string))
            score.extend(re.findall(vzorec_score, string))
            st_glasov.extend(re.findall(vzorec_st_glasov, string))
            #url vsake podstrani se ponovi 2x, zato odstranimo ponovitev
            urlji = list(set(re.findall(vzorec_url, string)))
        print('mjav')
        #sedaj moramo prenesti podstran vsake knjige:
        #v datoteko shranimo podstran ene knjige, pridobimo podatke in jih nekam shranimo, 
        #nato pa shranimo naslednjo podstran in povozimo prejsnjo datoteko
        for j in range(1):
            slovar_knjige = {}
            #save_frontpage(book_subpage_url.format(urlji[j]), book_directory, subpage_filename)
            with open(r"C:\Users\Ana Julija\Documents\Najbolj-e-knjige-vseh-asov\Pridobivanje_podatkov\book_subpage.html", "r", encoding="utf-8") as sub:
                besedilo = sub.read()
                for k in range(1):
                    #v slovar posamezne knjige moramo shraniti podatke, ki smo jih pridobili na glavni strani
                    # (id_avtor, score, st_glasov, te podatke bom zaradi lepsega izgleda slovarja vrinila med ostale)
                    
                #TO DO:ali dolocene zadeve, kjer je le en podatek dam v str/int

                    slovar_knjige["knjiga"] = re.findall(vzorec_knjiga, besedilo)[0]
                    slovar_knjige["id_knjige"] = id
                    id += 1
                    slovar_knjige["avtor"] = re.findall(vzorec_avtor, besedilo)[0]
                    slovar_knjige["id_avtor"] = int(id_avtor[k])
                    slovar_knjige["serija"] = re.findall(vzorec_serija, besedilo) != []
                    slovar_knjige["opis"] = (re.findall(vzorec_opis, besedilo)[0]).replace("<em>", "").replace("</em>", "").replace("<br />", "     ")
                    slovar_knjige["leto"] = int(re.findall(vzorec_leto, besedilo)[0])
                    slovar_knjige["zalozba"] = re.findall(vzorec_zalozba, besedilo)[0]
                    #TO DO:vzeti le nekaj zanrov 
                    #TO DO: direktno povezat leto in nagrado in glasove in zanr
                    slovar_knjige["zanr"] = re.findall(vzorec_zanr, besedilo)[:3]
                    #slovar_knjige["st_ocen_zanra"] = re.findall(vzorec_st_ocen_zanra, besedilo)
                    nagrade = re.findall(vzorec_nagrade, besedilo)
                    leto_nagrade = re.findall(vzorec_leto_nagrade, besedilo)
                    nagrade_sez = []
                    for n in range(len(nagrade)):
                        nagrade_sez.append([nagrade[n], leto_nagrade[n]])
                    slovar_knjige["nagrade"] = nagrade_sez
                    slovar_knjige["povprecna_ocena"] = float(re.findall(vzorec_povprecna_ocena, besedilo)[0])
                    slovar_knjige["score"] = int(score[k].replace(",", ""))
                    slovar_knjige["st_glasov"] = int(st_glasov[k].replace(",", ""))
                    slovar_knjige["st_ocen"] = int(re.findall(vzorec_st_ocen, besedilo)[0].replace(",", ""))
                    slovar_knjige["st_reviewov"] = int(re.findall(vzorec_st_reviewov, besedilo)[0].replace(",", ""))
                    
                    print(slovar_knjige)

                    #TO DO:slovar nekam shrani

                #TO DO: naredi csv file

        
                





if __name__ == '__main__':
    main()