# Ker vseh potrebnih informacij ne moremo dobiti direktno z naše strani, moramo obiskati vseh 10000 podstrani.
# To storimo tako, da z regularnimi izrazi poberemo urlje podstrani in nato prenesemo htmlje teh podstrani

#regularni izraz za zajem urlja:
import re

# with open(r"C:\Users\Ana Julija\Documents\Najbolj-e-knjige-vseh-asov\Pridobivanje_podatkov\best_books.html", "r", encoding="utf-8") as s:    
#     string = s.read()
#     urls = list(set(re.findall(r'href=[\'"]?\/book\/show\/([^\'" >]+)', string))) #vsak link se podvoji 2x, s spremembo v mnozico odstranim ponovitve

# print(urls)


#želim narediti slovar slovarjev oblike:
#{naslov_knjige1:{mesto:"", avtor:"",...}, naslov_knjige2:{...},...}

#regularni izrazi za zajem podatkov:

with open(r"C:\Users\Ana Julija\Documents\Najbolj-e-knjige-vseh-asov\Pridobivanje_podatkov\best_books.html", "r", encoding="utf-8") as s:    
    string = s.read()
    avtorji_ime = re.findall(r'itemprop="name">(.+)<\/span>', string)
    avtorji_id = re.findall(r'author\/show\/(\d+)', string)
    score = re.findall(r'score: (.+)<\/a>', string)
    st_glasov = re.findall(r'false;">(.+) people voted<\/a>', string)
    urlji = list(set(re.findall(r'href=[\'"]?\/book\/show\/([^\'" >]+)', string)))

print(len(urlji))
#DELA
#avtor:
#<span itemprop="name">(?P<avtor>.+)<\/span>

#naslov:
#<h1 id="bookTitle".*itemprop="name">\s*(?P<naslov>.*)\s*<\/h1>

#id knjige
#ISBN13: <span itemprop=\'isbn\'>(\d{13})

#naslov serije TO DO:ce ne najde ti sporoci, da ves, da ni serija(stevilko v seriji nekam zapise)
#<a class="greyText" href="\/series\/.*\s*\((?P<naslov_serije>.*)\)\s*<\/a>

#ocena od 1 do 5
#<span itemprop="ratingValue">\n*\s*(?P<ocena1do5>.+)\n*<\/span>

#datum izdaje in zalozba 
#<div class="row">\s*Published\s*.*(?P<datum>\d{4})\s*by\s*(?P<zalozba>.*)\s*<\/div>
#ven vrze v obliki:[('2008', 'Scholastic Press')]

#stevilo ratingov(ocen)
#<meta itemprop="ratingCount" content="(?P<ratings>\d*)"\s*\/>

#stevilo reviewov
#<meta itemprop="reviewCount" content="(?P<reviews>\d*)"\s*\/>

#zanri + st glasov za ta zanr
#(?P<st_ocen_zanra>\d+) people shelved this book as &#39;(?P<zanr>.+)&#39;

#nagrade(+leto)
#award\/show\/.*?>(.+?)\((\d*)\)<\/a>

#---------------------------------------------------------------------------------------------------
#NE DELA
#ID KNJIGE IN AVTORJA??-ne piše nikjer na strani, knjigo bi mogoče lahko uredili po ISBN
#avtorju bi mi dodelili id_preverili bi ali avtor z istim imenom že obstaja in mu dodelili isti id, 
#če ne obstaja pa id+1, PROBLEM: kaj če imata avtorja isto ime a nista ista oseba?



#POBERI Z GLAVNE STRANI
#skupna ocena bralcev + koliko bralcev je glasovalo

#ID
#author\/show\/(\d+)
#AVTOR  
#itemprop="name">(.+)<\/span>
#SCORE
#score: (.+)<\/a>
#VRSTNI RED KNJIGE
#<td valign="top" class="number">(\d+)<\/td>
#ST LJUDI, KI SO GLASOVALI
#false;">(.+) people voted<\/a>
#URL
#href=[\'"]?\/book\/show\/([^\'" >]+)

#IDEJA:
#naredimo sezname za vsako zadevo in nato povezemo vse skupaj po vrstnem redu(3.zadeva z vsakega seznama gre skupaj)

# avorji_ime = re.findall(r'itemprop="name">(.+)<\/span>', string)
# avtorji_id = re.findall(r'author\/show\/(\d+)', string)
# score = re.findall(r'score: (.+)<\/a>', string)
# st_glasov = re.findall(r'false;">(.+) people voted<\/a>', string)
# urlji = re.findall(r'href=[\'"]?\/book\/show\/([^\'" >]+)', string)

slovar = [{'vrsta':'macka','govor':'mjav', 'hrana':'meso'}, {'vrsta':'pes','govor':'hov', 'hrana':'briketi'}]

import csv

with open('mycsvfile.csv','w', encoding="utf-8") as f:
    w = csv.DictWriter(f,slovar.keys())
    w.writerows(slovar)
