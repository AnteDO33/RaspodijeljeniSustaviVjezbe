import asyncio
import random
from pprint import pprint

#1. Dohvaćanje predložaka zadataka

async def dohvati_predloske_zadataka(vrijeme_cekanja):
    print("Početak dohvaćanja predložaka zadataka...")

    await asyncio.sleep(vrijeme_cekanja)

    predlosci = [
        {"id": 1, "Naziv": "Naučiti Python", "prioritet": "visok"},
        {"id": 2, "Naziv": "Naučiti JavaScript", "prioritet": "srednji"},
        {"id": 3, "Naziv": "Naučiti Java", "prioritet": "nizak"}
    ]
    pprint("Dohvaćeni predlošci zadataka:")
    return predlosci

#2. Dohvaćanje kategorija

async def dohvati_kategorije(vrijeme_cekanja):
    print("Početak dohvaćanja kategorija...")

    await asyncio.sleep(vrijeme_cekanja)

    kategorije = [
        {"id": 1, "naziv": "Fakultet", "boja": "plava"},
        {"id": 2, "naziv": "Osobno", "boja": "zeleno"},
        {"id": 3, "naziv": "Posao", "boja": "crvena"}
    ]
    print("Zavrseno dohvacanje kategorija.")
    return kategorije

#3. Dohvacanje savjeta
async def dohvati_savjete(vrijeme_cekanja):
    print("Pocetak dohvacanja savjeta...")

    await asyncio.sleep

    savjeti = [
        {"id": 1, "savjet": "Planirajte unaprijed"},
        {"id": 2, "savjet": "Prvo rijesi najvaznije zadatke"},
        {"id": 3, "savjet": "Redovito gledaj popis"}
        ]
    print("Zavrseno dohvacanje savjeta.")
    return savjeti

