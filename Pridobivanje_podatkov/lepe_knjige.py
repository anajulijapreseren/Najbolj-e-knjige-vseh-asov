import csv
import os
import requests
import re
import math
import os.path
import json
import sys

#--------------------------------------------------------------------------------------------------
#Definiramo konstante za število knjig in poimenujemo spletne strani ter datoteke in direktorije, 
#v katere bomo shranjevali podatke

SKUPNO_ST_KNJIG = 5000
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

#--------------------------------------------------------------------------------------------------
#REGEX VZORCI:

#vzorci, ki jih uporabimo na glavni strani(frontpage):

#url naslove poberemo, da lahko obiščemo podstran vsake knjige in pridobimo ostale podatke
vzorec_url = r'href=[\'"]?\/book\/show\/([^\'" >]+)'
vzorec_id_avtor = r'author\/show\/(\d+)'
vzorec_score = r'score: (.+)<\/a>'
vzorec_st_glasov = r'false;">(.+) people voted<\/a>'

#vzorci, ki jih uporabimo na podstrani(subpage):
vzorec_avtor = r'<span itemprop="name">(?P<avtor>[^<]+)<+?'                  
vzorec_knjiga = r'<h1 id="bookTitle".*itemprop="name">\s*(?P<knjiga>.*)\s*</h1>'
vzorec_serija = r'<div class="infoBoxRowTitle">(Series)</div>'
vzorec_povprecna_ocena = r'<span itemprop="ratingValue">\n*\s*(?P<povprecna_ocena>.+)\n*</span>'

vzorec_zalozba = r'<div class="row">\s*Published\s*.*\d{4}\s*by (?P<zalozba>.*)\s+'
vzorec_st_ocen = r'<meta itemprop="ratingCount" content="(?P<ratings>\d*)"\s*/>'
vzorec_st_reviewov = r'<meta itemprop="reviewCount" content="(?P<reviews>\d*)"\s*/>'
vzorec_zanr = r'people shelved this book as &#39;(?P<zanr>.+)&#39;'
vzorec_st_ocen_zanra = r'(?P<st_ocen_zanra>\d+) people shelved this book as &#39;'
vzorec_nagrade = r'award\/show\/.*?>(?P<nagrade>.+?)(?:\(|<)'
vzorec_leto_nagrade = r'award/show/.*?>.+?\((?P<leto_nagrade>\d*)\)</a>'

#ta vzorec je za prvo leto izida (first published in _)saj so nekatere knjige izdali večkrat
vzorec_leto1 = r'<div class="row">\s*Published\s*<nobr class="greyText">\s*\(.*(?P<leto>\d{4})\)\s*<\/nobr>'
#splošen vzorec za leto izida
vzorec_leto2 = r'<div class="row">\s*Published\s*.*(?P<leto>\d{4})\s*by'

#Opisi knjig so različno dolgi, zato so nekateri v celoti zapisani v okvirčku, pri drugih pa moramo klikniti "more"
#če uporabimo le vzorec za krajše besedilo, na koncu daljšega zapisa dobimo "..."
#če uporabimo le vzorec za daljše besedilo, pa pri krajšem zapisu preskoči v komentarje in kot opis zajame
#prvi komentar
#Zato z zgornjima regularnima izrazoma preverimo ali je opis dolg ali kratek, 
#nato pa uporabimo ustreznega od spodnjih opisov.
vzorec_st_opisa = r'<span id="freeTextContainer(\d+)">'
vzorec_podrobnega_opisa = '<span id="freeText{}" style=".*">'

vzorec_opis_navaden = r'<span id="freeTextContainer\d+">(.*?)</span>'
vzorec_opis_podroben = r'<span id="freeText\d+" style=".*?">(?:Alternate.*?<br \/>)*(.*?)<\/span>'

#--------------------------------------------------------------------------------------------------
#FUNKCIJE za pripravo/prenos/zapis datotek:
#Funkcije: pripravi_imenik, zapisi_json in zapisi_csv so vzete iz 
#https://github.com/matijapretnar/programiranje-1/tree/master/02-zajem-podatkov/predavanja iz datoteke orodja.py.

def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)


def zapisi_json(objekt, ime_datoteke):
    '''Iz danega objekta ustvari JSON datoteko.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as json_datoteka:
        json.dump(objekt, json_datoteka, indent=4, ensure_ascii=False)


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


def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)


#--------------------------------------------------------------------------------------------------
#FUNKCIJE za zajem opisa in olepšavo/popravek zajetega besedila:


#funkcija,ki ugotovi ali moramo vzeti izraz za kratek ali dolg opis
def izloci_opis(html_text):
    stevke = re.findall(vzorec_st_opisa, html_text)[0]
    podroben_opis = re.findall(vzorec_podrobnega_opisa.format(stevke), html_text)

    #če nismo našli podrobnega opisa(ni nam treba klikniti na more-ze vidimo celoten opis) nam regularni izraz
    #za podroben opis ne bo našel ničesar
    if podroben_opis == []:
        opis = re.findall(vzorec_opis_navaden, html_text)[0]

    #našli smo gumb "more", torej moramo vzeti podrobnejši opis
    else:
        opis = re.findall(vzorec_opis_podroben, html_text)[0]

    return opis


#spletna stran pri opisu knjige včasno vključi tudi podatke o naslovici
#(npr. alternative cover, You can find the redesigned cover of this edition HERE, ISBN...)
#poleg tega vpis vkljucuje tudi html oznake za presledke med vrsticami, poševno pisavo...
#čim več teh "nepravilnosti" želimo odpraviti z naslednjo funkcijo
#(seveda pa ne moremo odpraviti vseh, saj ne moremo le z regularnimi izrazi vedeti ali zadnji stavek "You can also read part 2"
# še opisuje knjigo ali ne)
def predelaj_opis(opis, naslov):
    """Funkcija sprejme besedilo, ki ga dobimo z regularnim izrazom,
    in ga predela v uporabniku lepo obliko, torej odstrani <b>,<i>...in nezeljene podatke"""

    opis = opis.replace("<em>", "").replace("</em>", "").replace("<br>", " ").replace("<b>", "").replace("</b>", "").replace("<br />", " ").replace("<br/>", " ")
    opis = opis.replace("<a>", "").replace("</a>", "").replace('\"', "").replace("<p>", "").replace("</p>", "").replace("(back cover)","")
    
    while "<i>" in opis:
        zacetek = opis.find("<i>")
        konec = opis.find("</i>")
        opis = opis[:zacetek] + opis[konec + 4:]

    #vcasih v besedilu vseeno ostane se kaksen </i> zakljucek-ga odstranimo
    opis = opis.replace("</i>", "") 

    #Problem: vcasih se v <i>...</i> skrivajo informacije, ki nimajo zveze z opisom(npr. alternative cover),
    #drugic pa naslov. Zato po odstranitvi preverimo, če se opis sedaj začne s presledkom, is, was...
    #To pomeni, da smo izbrisali posevno zapisan naslov, torej ga spet dodamo.
    if (opis[:3] == " is" or opis[:4] == " was" or opis[:4] == " has" or opis[:5] == " have"):
        opis = naslov + opis

    return opis


def seznam_kljucev(slovar):
    """funkcija da kljuce slovarja v seznam, ki ga lahko uporabimo za poimenovanje
    stolpcev v csv filu"""
    sez = []
    for key in slovar.keys():
        sez.append(key)
    return sez


def spremeni_v_apostrof(seznam):
    """nekatere nagrade imajo v imenu apostrof, ki je v html oblike &#39;
    ta zapis spremenimo v ' """

    sez = []
    for i in seznam:
        i = i.replace("&#39;", "'")
        sez.append(i)

    return sez


#--------------------------------------------------------------------------------------------------
#GLAVNA FUNKCIJA:

def main(redownload=True, reparse=True):
    #spletna stran ima vsake toliko časa "sesuto" podstran knjige
    #(npr. https://www.goodreads.com/book/show/18765.I_Claudius)
    #opomba:pri zadnjem pregledu sem ugotovila, da spletna stran spet obstaja, vendar pa
    #ne škodi, da še vedno preverim za morebitne napake
    #te knjige moramo izlociti(to naredimo, ko ugotovimo da "knjiga nima naslova")

    # Najprej v lokalno datoteko shranimo eno od glavnih strani
    for i in range(1,ST_STRANI + 1):
        print("koncal {} stran".format(i-1))
        #vse podatke o knjigah(shranjeni so v slovarju) shranimo v sezname:
        #seznam, uporabljen za json file
        vse_knjige = []
        #seznami, uporabljeni za csv file
        knjige = []
        zanri = []
        nagrade = []

        
        id = (i-1)*ST_KNJIG_NA_STRAN + 1
        

        #shranimo eno od strani, ki jih moramo analizirati
        save_frontpage(book_frontpage_url.format(i), book_directory, frontpage_filename)

        #Iz te strani poberemo podatke, ki jih ne najdemo na podstrani posamezne knjige in url, ki
        #nas bo peljal na podstran vsake knjige, da dobimo ostale podatke.
        #Ko poberemo podatke z vseh podstrani naložimo novo stran in pri tem povozimo staro datoteko, 
        #saj je več ne potrebujemo.
    
        with open(r"C:\Users\Ana Julija\Documents\Najbolj-e-knjige-vseh-asov\Pridobivanje_podatkov\best_books.html", "r", encoding="utf-8") as s:    
            string = s.read()

            #podatke o avtorju, scoru in id-ju bomo potrebovali za csv, zato jih shranimo v list:
            id_avtor, score, st_glasov = [], [], []

            id_avtor.extend(re.findall(vzorec_id_avtor, string))
            score.extend(re.findall(vzorec_score, string))
            st_glasov.extend(re.findall(vzorec_st_glasov, string))

            #url vsake podstrani se ponovi 2x, zato bomo pri delu z njimi šli za 2 naprej.
            urlji = re.findall(vzorec_url, string)
        
        #sedaj moramo prenesti podstran vsake knjige:
        #v datoteko shranimo podstran ene knjige, pridobimo podatke in jih nekam shranimo, 
        #nato pa shranimo naslednjo podstran in povozimo prejsnjo datoteko
        k=0
        
        for j in range(0,len(urlji),2):
            
            slovar_knjige = {}
            save_frontpage(book_subpage_url.format(urlji[j]), book_directory, subpage_filename)
            with open(r"C:\Users\Ana Julija\Documents\Najbolj-e-knjige-vseh-asov\Pridobivanje_podatkov\book_subpage.html", "r", encoding="utf-8") as sub:
                besedilo = sub.read()
                
                #v slovar posamezne knjige moramo shraniti podatke, ki smo jih pridobili na glavni strani
                # (id_avtor, score, st_glasov, te podatke bom zaradi lepsega izgleda slovarja vrinila med ostale

                #KNJIGE
                knjiga = re.findall(vzorec_knjiga, besedilo)
                if knjiga != []:#tu zaznamo podstrani z napako in jih preskocimo
                    slovar_knjige["knjiga"] = knjiga[0]
                    slovar_knjige["id_knjige"] = id 
                    slovar_knjige["avtor"] = re.findall(vzorec_avtor, besedilo)[0]
                    slovar_knjige["id_avtor"] = int(id_avtor[k])
                    slovar_knjige["serija"] = re.findall(vzorec_serija, besedilo) != []
                    slovar_knjige["opis"] = predelaj_opis(izloci_opis(besedilo),slovar_knjige["knjiga"])
                    leto = re.findall(vzorec_leto1, besedilo)

                    if leto != []:
                        slovar_knjige["leto"] = int(leto[0])
                    else:
                        leto = re.findall(vzorec_leto2, besedilo)
                        if leto != []:
                            slovar_knjige["leto"] = int(leto[0])
                        else:
                            #tu sem naredila napako, saj sem namesto None zapisala "unknown", 
                            #kar mi je povzročalo težavo pri delu z letom(vse je oblike string)
                            slovar_knjige["leto"] = "unknown"
                            #bolje:
                            #slovar_knjige["leto"] = None

                    zalozba = re.findall(vzorec_zalozba, besedilo)
                    if zalozba != []:
                        slovar_knjige["zalozba"] = zalozba[0]
                    else:
                        #Tudi tu bi bilo morda bolje vzeti None
                        slovar_knjige["zalozba"] = "unknown"
                        #slovar_knjige["zalozba"] = None
                    
                    slovar_knjige["povprecna_ocena"] = float(re.findall(vzorec_povprecna_ocena, besedilo)[0])
                    slovar_knjige["score"] = int(score[k].replace(",", ""))
                    slovar_knjige["st_glasov"] = int(st_glasov[k].replace(",", ""))
                    slovar_knjige["st_ocen"] = int(re.findall(vzorec_st_ocen, besedilo)[0].replace(",", ""))
                    slovar_knjige["st_reviewov"] = int(re.findall(vzorec_st_reviewov, besedilo)[0].replace(",", ""))
                    slovar_knjige["nagrade"] = spremeni_v_apostrof(re.findall(vzorec_nagrade, besedilo))
                    slovar_knjige["zanri"] = re.findall(vzorec_zanr, besedilo)[:3]
                    vse_knjige.append(slovar_knjige)
                    ima_nagrade = (slovar_knjige["nagrade"] != [])

                    #naredimo slovar knjig brez zanrov in nagrad(uporabili ga bomp pri pisanju csv datoteke)
                    #zanre in nagrade izkljucimo, saj sta seznama z vec elementi
                    knjige_bzn = slovar_knjige.copy()
                    knjige_bzn.pop("zanri")
                    knjige_bzn.pop("nagrade")
                    knjige.append(knjige_bzn)
                    #Dodamo stolpec "nagrade", da bomo pri analizi takoj ločili med knjigami brez/z nagradami.
                    knjige_bzn["nagrade"]=ima_nagrade


                    #ŽANRI
                    for zanr in slovar_knjige["zanri"]:
                        zanri.append({"id_knjige": id, "zanr" : zanr})
                        
                    #NAGRADE
                    for nagrada in slovar_knjige["nagrade"]:
                        nagrade.append({"id_knjige": id, "nagrada" : nagrada})
  
                        
                id += 1
                k += 1

            #naredimo json file (json datotek na koncu nisem uporabljala, bom pa pustila kodo, 
            #če jo bom potrebovala kdaj kasneje)             
            #zapisi_json(vse_knjige, 'PODATKI/vse_knjige{}.json'.format(i))

            #NAREDIMO CSV FILE
            #Vsakih sto knjig podatke shranimo v csv datoteke.
            #Tako računalniku ni potrebno držati vseh podatkov v nekem seznamu/slovarju +
            #Spletna stran pri prevelikem prenosu strani neha servirati podatke.
            #Takrat lahko proces ustavimo, pri "for i in range(1,ST_STRANI + 1):" spremenimo 1 v številko strani,
            #kjer smo končali (vidiš po končnici csv datotek) in nadaljujemo.
            #Vse csv datoteke lahko kasneje združimo s pogonom "zdruzi_csv.py"
    
            #naredimo "glavni file" knjige, ki vsebuje vse podatke razen zanrov in nagrad(to sta seznama z vec podatki)
            zapisi_csv(knjige, seznam_kljucev(knjige[0]), 'PODATKI/knjige{}.csv'.format(i))

            #naredimo še fila za zanre in nagrade, kjer zanr in nagrado priredimo id-ju knjige
            zapisi_csv(zanri, seznam_kljucev(zanri[0]), 'PODATKI/zanri{}.csv'.format(i))

            zapisi_csv(nagrade, ["id_knjige", "nagrada"], 'PODATKI/nagrade{}.csv'.format(i))



if __name__ == '__main__':
    main()