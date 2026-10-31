import asyncio

async def dohvati_podatke():
    podaci = [broj for broj in range (1, 11)]
    await asyncio.sleep(3)
    print("Dohvaćeni podaci:")
    return podaci

async def main():
    podaci = await dohvati_podatke()
    print(podaci)

asyncio.run(main())