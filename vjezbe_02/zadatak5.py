import asyncio

async def secure_data(podaci):
    await asyncio.sleep(3)

    return {
        "prezime": podaci["prezime"],
        "broj_kartice": hash(str(podaci["broj_kartice"])),
        "CVV": hash(str(podaci["CVV"]))
    }

async def main():
    osjetljivi_podaci = [
        {"prezime": "Ivić", "broj_kartice": 1234567890123456, "CVV": 123},
        {"prezime": "Perić", "broj_kartice": 9876543210987654, "CVV": 456},
        {"prezime": "Kovačić", "broj_kartice": 5555555555554444, "CVV": 789}
    ]

    zadaci = [
        asyncio.create_task(secure_data(podaci)) for podaci in osjetljivi_podaci
    ]
    rezultati = await asyncio.gather(*zadaci)
    for rezultat in rezultati:
        print(rezultat)

asyncio.run(main())