
import asyncio
import random
import time
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
async def main():
    random.seed(42)

    vremena = {
        "predlosci": random.uniform(1, 3),
        "kategorije": random.uniform(1, 3),
        "savjeti": random.uniform(1, 3)
    }

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

    print("\nPripremljeni podaci:")
    pprint(podaci, sort_dicts=False)


if __name__ == "__main__":
    asyncio.run(main())

t1 = time.perf_counter()
results = asyncio.run(main())
t2 = time.perf_counter()

print(f"\nVrijeme izvrsavanja: {t2 - t1:.2f} sekundi")
