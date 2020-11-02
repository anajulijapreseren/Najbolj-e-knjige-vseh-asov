# Ker vseh potrebnih informacij ne moremo dobiti direktno z naše strani, moramo obiskati vseh 10000 podstrani.
# To storimo tako, da z regularnimi izrazi poberemo urlje podstrani in nato prenesemo htmlje teh podstrani

#regularni izraz za zajem urlja:
import re
with open(r"C:\Users\Ana Julija\Documents\Najbolj-e-knjige-vseh-asov\Pridobivanje_podatkov\best_books.html", "r", encoding="utf-8") as s:    
    string = s.read()
    urls = list(set(re.findall(r'href=[\'"]?\/book\/show\/([^\'" >]+)', string))) #vsak link se podvoji 2x, s spremembo v mnozico odstranim ponovitve

print(urls)
