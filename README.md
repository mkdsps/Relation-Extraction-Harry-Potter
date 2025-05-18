
# 🧙‍♂️ Projekat: Ekstrakcija Relacija u Domenu Harry Pottera

## 🎯 Cilj projekta

Cilj ovog projekta je razvoj modela za ekstrakciju relacija između entiteta u tekstu, u okviru fiktivnog domena Harry Potter univerzuma.

Za dati paragraf, model identifikuje entitete (likove, kuće, predmete, čini, lokacije) i relacije među njima. Rezultat se može opcionalno vizualizovati kao graf.

Primer:

Input:
"Magix is using broom to fly, to his house Gryffindor."

Output:
```json
{
  "tokens": ["Magix", "is", "using", "broom", "to", "fly,", "to", "his", "house", "Gryffindor."],
  "entities": [
    { "id": 1, "text": "Magix", "type": "CHARACTER", "token_start": 0, "token_end": 0 },
    { "id": 2, "text": "broom", "type": "MAGIC_ITEM", "token_start": 3, "token_end": 3 },
    { "id": 3, "text": "Gryffindor", "type": "HOUSE", "token_start": 9, "token_end": 9 }
  ],
  "relations": [
    { "type": "uses", "head": 1, "tail": 2 },
    { "type": "member-of-house", "head": 1, "tail": 3 }
  ]
}
```
(+ opcioni prikaz kao graf pomoću `networkx`)


## ⚡ Zašto Harry Potter?

Harry Potter univerzum je idealan za ovakav tip zadatka jer:
- Tekstovi su lako dostupni i poznati
- Semantika relacija je jasna
- Omogućava fokus na NLP tehniku umesto borbe sa "messy" podacima


## 🧩 Entiteti i relacije

Entiteti:
- CHARACTER – likovi (Harry, Hermione, Dumbledore...)
- HOUSE – Hogwarts kuće (Gryffindor, Slytherin...)
- MAGIC_ITEM – magični predmeti (wand, broomstick...)
- SPELL – čarolije (Expelliarmus, Expecto Patronum...)
- LOCATION – lokacije (Hogwarts, Forbidden Forest...)

Relacije:
CHARACTER – CHARACTER:
- friend-of, enemy-of, mentor-of, student-of, parent-of, sibling-of, rival-of, ally-of

CHARACTER – HOUSE:
- member-of-house, founder-of-house

CHARACTER – MAGIC_ITEM:
- uses, owns, acquires, gives

CHARACTER – SPELL:
- casts, knows, teaches

CHARACTER–LOCATION:
  - located_in

## 📚 Prikupljanje i priprema podataka

- Dataset: Kaggle Harry Potter knjige (TXT)
- Uklonjeni su naslovi poglavlja i spojeni najkraći paragrafe da bi se dobio bolji kontekst
- Tekst nije dodatno čišćen jer su LLM modeli već obučeni na ovom korpusu  
→ scripts/utils.py

Moguće poboljšanje:  
Dodavanje enciklopedijskih rečenica sa Harry Potter Wiki stranica (koje često eksplicitno sadrže relacije) radi proširenja domene i pokrivenosti.


## 🔍 Odabir pasusa

Koristi se cluster-based sampling:
- Svakom pasusu se dodeljuje vektorska reprezentacija (npr. SentenceTransformer)
- Primena KMeans klasterizacije
- Nasumični odabir iz svakog klastera obezbeđuje raznovrsnost  
→ scripts/odabir_paragrafa


## ✍️ Anotacija podataka

- Anotacija pomoću LLM-a (GPT-4.1-mini) putem OpenAI API-ja  
  (trošak ~600 RSD za celu bazu)

- Prompt uključuje numerisanje tokena, što rešava većinu problema sa token_start i token_end

- Dobijeni anotirani JSON se čuva kao jedan data point  
→ scripts/llm_anotation.py, scripts/helper_classes.py

### 🟡 Token checker-i  
Implementirani su jednostavni token checkeri koji proveravaju:
- Da li su token_start i token_end u ispravnom opsegu
- Da li je text entiteta tačno isečen iz tokens
- Da li head i tail u relacijama odgovaraju postojećim entitetima  


## ✅ Ručna validacija – Golden Set

- Ručno pregledano 225 anotiranih primera formira golden set
- Ručna validacija je obavljena kroz jednostavnu checker aplikaciju sa GUI-em, koja omogućava:
  - pregled tokenizovanih pasusa
  - izmenu entiteta i relacija
  - brzo označavanje grešaka  
→ anotation_checker/checker.py  
→ anotations/golden_set_checked se koristi za validaciju modela i merenje F1 score-a


## 🤖 Model i fine-tuning

- Model: ner (fine-tuned bert-base) + re (fine-tuned bert-base) 
- Zadaci: Named Entity Recognition (NER) i Relation Extraction (RE)
- Okruženje: Google Colab GPU (T4).
- Dataset format je kompatibilan sa većinom popularnih RE frameworka
- Fine-tuning pristup:
    - Model je treniran na ~2000 anotiranih primera (većina uz pomoć LLM-a, deo ručno verifikovan).
    - Goldenset (225 primera) koristi se za validaciju i testiranje.
    - Tokom treniranja koriste se klasične metrike: precision, recall, F1-score, posebno za relacije.
    - Trening je jednostavan nakon što je dataset pravilno formatiran.

| Model   | F1 Test | F1 Val |
|---------|---------|--------|
| RE      |  0.93   |  0.93  |
| NER     |  0.87   |  0.85  |


## 📊 Vizualizacija

- Korišćenje networkx + matplotlib za prikaz relacija u formi grafa
- Svaki pasus može biti prikazan kao entitetska mreža sa obojenim čvorovima i strelicama


## 💸 Troškovi

| Stavka                 | Cena (RSD) |
|------------------------|------------|
| LLM anotacija          | ~600       |
| Golden set ručno       | ~2000      |
| Ukupno                 | 2600       |


## 🛠 Način korišćenja projekta

Ovaj repozitorijum nije namenjen direktnom pokretanju, već služi kao ilustracija celog pipeline-a: od pripreme podataka, preko anotacije i obuke modela, do evaluacije i vizualizacije.

Završni model možete isprobati u interface.py fajlu, koji omogućava jednostavno testiranje i vizualizaciju rezultata.

## 🔄 Pipeline
Projekat je organizovan kao jasno definisan pipeline, od sirovog teksta do krajnjeg testiranja modela. Svaka faza je dokumentovana kroz skripte i Jupyter beležnice.

Preprocesiranje teksta
→ scripts/utils.py
Originalni tekst knjiga, spaja kraće pasuse, čisti neželjeni sadržaj (naslovi poglavlja).

Odabir pasusa za anotaciju
→ notebooks/odabir_paragrafa.ipynb
Koristi SentenceTransformer + KMeans za raznovrstan uzorak pasusa.

Automatska anotacija pomoću LLM-a
→ notebooks/anotiranje.ipynb
Slanje pasusa ka GPT API-ju i dobijanje JSON anotacija.
(pomocni fajlovi, prompt.txt, scripts/llm_anotation.py, scripts/helper_classes.py)

Ručna ispravka anotacija (Golden Set)
→ notebooks/ispravka_data.ipynb
Token_start i token_end se prilagodjavaju.

Odabir konačnih anotacija za trening/test
→ notebooks/odabir_anotacija.ipynb
Selektovanje primera za trening, validaciju i testiranje.

Checker GUI za dodatnu validaciju
→ anotation_checker/checker.py
Vizualni alat za proveru ispravnosti entiteta i relacija.

Priprema podataka za treniranje
→ notebooks/priprema_podataka_ner.ipynb
→ notebooks/priprema_podataka_re.ipynb
Formatiranje anotacija u odgovarajući oblik za NER i RE modele.

Treniranje modela
→ train
Fine-tuning BERT modela na pripremljenim podacima.

Testiranje i vizualizacija rezultata
→ notebooks/INTERFACE.ipynb
Omogućava unos teksta, prikaz predikcija i crtanje entitetskog grafa.


## Poboljsanja:

Potreban data-aug za obicne recenice tipa: Harry is killing his sworn enemy. itd...
Kada treniras re i ner zameni imena sa nekim dugim imenima kako bi model kasnije bolje generalizovao.# Relation-Extraction-Harry-Potter
# Relation-Extraction-Harry-Potter
