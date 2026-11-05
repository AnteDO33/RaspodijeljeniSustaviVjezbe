
import asyncio
import random
import time
import json
from pathlib import Path
from pprint import pprint


# 1. Dohvacanje predlozaka zadataka
async def dohvati_predloske_zadataka(vrijeme_cekanja):
    print("Pocetak dohvacanja predlozaka zadataka...")

    await asyncio.sleep(vrijeme_cekanja)

    predlosci = [
        {"id": 1, "naziv": "Nauciti Python", "prioritet": "Visok"},
        {"id": 2, "naziv": "Napraviti projekt", "prioritet": "Srednji"},
        {"id": 3, "naziv": "Procitati knjigu", "prioritet": "Nizak"}
    ]

    print("Zavrseno dohvacanje predlozaka zadataka.")
    return predlosci


# 2. Dohvacanje kategorija
async def dohvati_kategorije(vrijeme_cekanja):
    print("Pocetak dohvacanja kategorija...")

    await asyncio.sleep(vrijeme_cekanja)

    kategorije = [
        {"id": 1, "naziv": "Fakultet", "boja": "plava"},
        {"id": 2, "naziv": "Posao", "boja": "crvena"},
        {"id": 3, "naziv": "Osobno", "boja": "zelena"}
    ]

    print("Zavrseno dohvacanje kategorija.")
    return kategorije


# 3. Dohvacanje savjeta
async def dohvati_savjete(vrijeme_cekanja):
    print("Pocetak dohvacanja savjeta...")

    await asyncio.sleep(vrijeme_cekanja)

    savjeti = [
        {"id": 1, "tekst": "Prvo rijesi najvaznije zadatke."},
        {"id": 2, "tekst": "Velike zadatke podijeli na manje."},
        {"id": 3, "tekst": "Redovito pregledavaj svoj popis."}
    ]

    print("Zavrseno dohvacanje savjeta.")
    return savjeti


# Glavna funkcija

# ZADATAK 2 - Sekvencijalno izvodenje
async def sekvencijalno(vremena):
    print("\n--- SEKVENCIJALNO IZVODENJE ---")

    t1 = time.perf_counter()

    predlosci = await dohvati_predloske_zadataka(
        vremena["predlosci"]
    )

    kategorije = await dohvati_kategorije(
        vremena["kategorije"]
    )

    savjeti = await dohvati_savjete(
        vremena["savjeti"]
    )

    podaci = {
        "predlosci": predlosci,
        "kategorije": kategorije,
        "savjeti": savjeti
    }

    t2 = time.perf_counter()

    print(f"Sekvencijalno vrijeme: {t2 - t1:.2f} sekundi")

    return podaci, t2 - t1


# ZADATAK 2 - Konkurentno izvodenje
async def konkurentno(vremena):
    print("\n--- KONKURENTNO IZVODENJE ---")

    t1 = time.perf_counter()

    predlosci, kategorije, savjeti = await asyncio.gather(
        dohvati_predloske_zadataka(vremena["predlosci"]),
        dohvati_kategorije(vremena["kategorije"]),
        dohvati_savjete(vremena["savjeti"])
    )

    podaci = {
        "predlosci": predlosci,
        "kategorije": kategorije,
        "savjeti": savjeti
    }

    t2 = time.perf_counter()

    print(f"Konkurentno vrijeme: {t2 - t1:.2f} sekundi")

    return podaci, t2 - t1


# ZADATAK 2 - Test redoslijeda asyncio.gather()
async def test_gather(vremena):
    print("\n--- TEST REDOSLIJEDA GATHER ---")

    rezultati = await asyncio.gather(
        dohvati_savjete(vremena["savjeti"]),
        dohvati_predloske_zadataka(vremena["predlosci"]),
        dohvati_kategorije(vremena["kategorije"])
    )

    print("\nRedoslijed vracenih rezultata:")
    print("1. Savjeti:", rezultati[0])
    print("2. Predlosci:", rezultati[1])
    print("3. Kategorije:", rezultati[2])


# Glavna funkcija
async def main():
    random.seed(42)

    vremena = {
        "predlosci": random.uniform(1, 3),
        "kategorije": random.uniform(1, 3),
        "savjeti": random.uniform(1, 3)
    }

    print("--- VREMENA CEKANJA ---")
    for naziv, vrijeme in vremena.items():
        print(f"{naziv}: {vrijeme:.2f} sekundi")

    # Sekvencijalna obrada
    podaci_sek, vrijeme_sek = await sekvencijalno(vremena)

    # Konkurentna obrada
    podaci_kon, vrijeme_kon = await konkurentno(vremena)

    # Usporedba
    print("\n--- USPOREDBA ---")
    print(f"Sekvencijalno: {vrijeme_sek:.2f} sekundi")
    print(f"Konkurentno: {vrijeme_kon:.2f} sekundi")
    print(f"Ubrzanje: {vrijeme_sek / vrijeme_kon:.2f}x")

    print("Rezultati jednaki:", podaci_sek == podaci_kon)

    # Objedinjeni podaci
    print("\n--- PRIPREMLJENI PODACI ---")
    pprint(podaci_kon, sort_dicts=False)

    #Zadatak 3 - Spremanje podataka u JSON datoteku
    putanja = Path(__file__).parent / "podaci.json"

    with open(putanja, "w", encoding="utf-8") as datoteka:
        json.dump(podaci_kon, datoteka, ensure_ascii=False, indent=4)

    print(f"\nPodaci su spremljeni u datoteku: {putanja}")

    # Test redoslijeda
    await test_gather(vremena)


if __name__ == "__main__":
    asyncio.run(main())
