import re
import numpy as np
import os
import pandas as pd



def is_chapter_heading(paragraph: str) -> bool:
    # Regex: "Chapter" + razmak + broj (1 ili više cifara)
    return bool(re.search(r"^Chapter \d+", paragraph.strip()))

# funkcija koja vraca sve raw paragrafe iz text-a ne ukljucujuci chapter i chapter nazive..
def load_paragraphs(path : str) -> list:

    brisi = [
        "HP 1 - Harry Potter and the Sorcerer's Stone",
        "HP 2 - Harry Potter and The Chamber of Secrets",
        "Harry Potter And The Prisoner of Azkaban",
        "HP 4 - Harry Potter and The Goblet of Fire",
        "Harry Potter and the Order of the Phoenix",
        "Harry Potter and the Half-Blood Prince",
        "Harry Potter and the Deathly Hallows"
    ]

    with open(path, 'r') as f:
        text = f.read()

        raw_paragraphs = [p.strip() for p in text.split("\n\n")]
        paragraphs = []

        for para in raw_paragraphs:
            if not para or (para.upper() == para and len(para.split()) < 10) or para in brisi or is_chapter_heading(para):
                continue
            
            paragraphs.append(para)

    return paragraphs


# spaaj prekratke paragrafe....
def combine_short_paragraphs(paragraphs, min_len=40, max_len=240):
    combined_paragraphs = []
    buffer = ""
    buffer_len = 0

    for paragraph in paragraphs:
        para_len = len(paragraph.split())

        # Ako pasus ima dovoljno reči (>= 60 i <= 240), dodaj ga direktno
        if min_len <= para_len <= max_len:
            if buffer:  # Ako postoji preostali buffer koji nije dodan, dodaj ga
                combined_paragraphs.append(buffer.strip())
                buffer = ""  # Resetuj buffer
            combined_paragraphs.append(paragraph.strip())
            buffer_len = 0  # Resetuj duzinu

        # Ako je pasus prekratak (manji od 60 reči), dodaj ga u buffer
        elif para_len < min_len:
            buffer += " " + paragraph.strip()
            buffer_len += para_len

            # Kada buffer dostigne minimalnu duzinu, dodaj ga u finalnu listu
            if buffer_len >= min_len:
                combined_paragraphs.append(buffer.strip())
                buffer = ""  # Resetuj buffer
                buffer_len = 0

    if buffer_len >= min_len:
        combined_paragraphs.append(buffer.strip())

    return combined_paragraphs

def save_paragraphs_to_csv(paragraphs, file_name, save_path):
    # Kreira DataFrame sa pasusima i njihovom dužinom (broj reči)
    df = pd.DataFrame(paragraphs, columns=["text"])
    df['length'] = df['text'].apply(lambda x: len(x.split()))

    # Osiguraj da folder postoji
    os.makedirs(save_path, exist_ok=True)

    # Kreiraj punu putanju
    full_path = os.path.join(save_path, f"{file_name}.csv")

    # Sačuvaj CSV
    df.to_csv(full_path, index=False, encoding='utf-8')

    print(f"CSV fajl je uspešno sačuvan na: {full_path}")




if __name__ == '__main__':
    putanja = '../data/raw_data'

    txt_fajlovi = [f for f in os.listdir(putanja) if f.endswith('.txt')]
    
    for fajl in txt_fajlovi:

        naziv = fajl[:-4]



        paragrafi = load_paragraphs(os.path.join(putanja,fajl))

        paragrafi = combine_short_paragraphs(paragrafi)

        save_paragraphs_to_csv(paragrafi, naziv, '../data/processed_paragraphs')


        # duzine = [len(x.split(' ')) for x in paragrafi]

        # print(f"{naziv} : max = {np.max(duzine)}, mean = {np.mean(duzine)}")
        
 

    # duzine =  [len(x.split(' ')) for x in load_paragraf('../data/raw_data/01 Harry Potter and the Sorcerers Stone.txt')]
    # print(np.max(duzine))