import asyncio

async def dohvati_korisnike():
    await asyncio.sleep(3)
    return[
        {"id": 1, "ime": "Ana"},
        {"id": 2, "ime": "Ivan"}
    ]

async def dohvati_proizvode():
    await asyncio.sleep(5)
    return [
        {"id": 1, "naziv": "Laptop", "cijena":800},
        {"id": 2, "naziv": "Telefon", "cijena":500}
    ]

async def main():
    korisnici, proizvodi = await asyncio.gather(dohvati_korisnike(), dohvati_proizvode())

    print("korisnici:", korisnici)
    print("proizvodi:", proizvodi)

asyncio.run(main())
    