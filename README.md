# Najboljše knjige vseh časov

V okviru predmeta programiranje 1 bom analizirala najbolj priljubljene knjige.
Podatke o knjigah bom zajela s spletne strani goodreads: https://www.goodreads.com/list/show/1.Best_Books_Ever. Preučila bom prvih 10.000 knjig, razvrščenih po oceni bralcev. Ocena sestoji iz števila bralcev, ki so knjigo ocenili, in višine njihove ocene.

Za vsako knjigo bom zajela naslednje podatke:<br/>
-naslov, avtorja in id avtorja<br/>
-založbo in leto izida<br/>
-serija / solo knjiga<br/>
-opis<br/>
-prve 3 žanre po izboru bralcev<br/>
-skupno oceno bralcev, povprečno oceno(1-5), število ocen in število "reviewov"<br/>
-morebitne literarne nagrade<br/>

CSV datoteke:<br/>
Datoteke dobimo s pogonom lepe_knjige.py. Funkcije: pripravi_imenik, zapisi_json in zapisi_csv so vzete iz https://github.com/matijapretnar/programiranje-1/tree/master/02-zajem-podatkov/predavanja iz datoteke orodja.py.

knjige.csv vsebujejo:<br/>
knjiga, id_knjige, avtor, id_avtor, serija, opis, leto, zalozba, povprecna_ocena, score,st_glasov, st_ocen,st_reviewov<br/>

zanri.csv vsebujejo:<br/>
id_knjige,zanr<br/>

nagrade.csv vsebujejo:<br/>
id_knjige,nagrada<br/>

Pri nalaganju podatkov lahko hkrati nalagamo tudi le po sto podatkov in vsako stoterico shranimo v svojo datoteko(seveda lahko hkrati sprožimo nalaganje več kot ene datoteke). Za pridobitev ustreznih podatkov moramo namreč obiskati podstran vsake knjige, za kar porabimo precej časa, s pridobivanjem podatkov po delih pa lahko proces tudi prekinemo in naslednjič nadaljujemo, ob morebitni napaki pa ohranimo vsaj podatke, ki so že zapisani v datoteke. Dobljene csv datoteke kasneje združimo s pogonom datoteke zdruzi_csv.py. Funkcija je vzeta s https://www.freecodecamp.org/news/how-to-combine-multiple-csv-files-with-8-lines-of-code-265183e0854/.
Opomba:Pri zdruzevanju csv datotek se vrstni red podatkov rahlo spremeni, zato moramo na začetku analize podatke sortirati po id_knjige/score.

Opomba: trenutno je v csv datotekah naloženih le 100 knjig. Preostale knjige bom naložila, ko se bom odločila, koliko knjig bom analizirala. Spletna stran ima namreč podstrani, kar pomeni, da je treba za 10000 knjig prenesti 10000 datotek (in še 100 za naložitev "glavnih strani")


Hipoteze<br/>
skušala bom odgovoriti na naslednja vprašanja:<br/>
-Kateri avtorji in založbe so imeli naječ uspešnic?<br/>
-Kateri žanri so najbolj priljubljeni?<br/>
-Ali so bolj priljubljene serije ali individualne knjige?<br/>
-Ali obstaja časovno obdobje(recimo 10 let), v katerem je izšla večina knjig iz vrha seznama?<br/>
-Ali so knjige z literarnimi nagradami tudi med bralci bolje ocenjene?<br/>
