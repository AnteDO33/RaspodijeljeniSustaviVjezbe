import asyncio
import random

async def provjeri_parnost(broj):
    await asyncio.sleep(2)

    if broj % 2 == 0:
        return f"{broj} je paran"
    return f"{broj} je neparan"

async def main():
    brojevi = [random.randint(1, 100) for _ in range(10)]

    zadaci = [
        asyncio.create_task(provjeri_parnost(broj)) for broj in brojevi
    ]

    rezultati = await asyncio.gather(*zadaci)
    for rezultat in rezultati:
        print(rezultat)

asyncio.run(main())