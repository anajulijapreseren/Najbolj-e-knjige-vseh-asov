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

with open(r"C:\Users\Ana Julija\Documents\Najbolj-e-knjige-vseh-asov\Pridobivanje_podatkov\best_books_subpage_example.html", "r", encoding="utf-8") as s:    
    string = s.read()
    ratings = re.findall(r'(?P<st_ocen_zanra>\d+) people shelved this book as &#39;(?P<zanr>.+)&#39;', string) 

print(ratings)
#DELA
#avtor:
#<span itemprop="name">(?P<avtor>.+)<\/span>

#naslov:
#<h1 id="bookTitle".*itemprop="name">\s*(?P<naslov>.*)\s*<\/h1>

#ocena od 1 do 5
#<span itemprop="ratingValue">\n*\s*(?P<ocena1do5>.+)\n*<\/span>

#naslov serije TO DO:ce ne najde ti sporoci, da ves, da ni serija(stevilko v seriji nekam zapise)
#<a class="greyText" href="\/series\/.*\s*\((?P<naslov_serije>.*)\)\s*<\/a>

#datum izdaje in zalozba TO DO:spremeniti mesec in dan v stevilo + a pustim v (,) ali drugace?
#<div class="row">\s*Published\s*(?P<datum>.*)\s*by\s*(?P<zalozba>.*)\s*<\/div>
#ven vrze v obliki:[('September 14th 2008', 'Scholastic Press')]

#stevilo ratingov(ocen)
#<meta itemprop="ratingCount" content="(?P<ratings>\d*)"\s*\/>

#stevilo reviewov
#<meta itemprop="reviewCount" content="(?P<reviews>\d*)"\s*\/>

#zanri + st glasov za ta zanr
#(?P<st_ocen_zanra>\d+) people shelved this book as &#39;(?P<zanr>.+)&#39;

#---------------------------------------------------------------------------------------------------
#NE DELA

#nagrade(+leto)

#POBERI Z GLAVNE STRANI
#skupna ocena bralcev + koliko bralcev je glasovalo