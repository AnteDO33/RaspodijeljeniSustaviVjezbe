import asyncio

baza_korisnika = [
    {"korisnicko_ime": "mirko123", "email": "mirko123@gmail.com"},
    {"korisnicko_ime": "ana_anic", "email": "aanic@gmail.com"},
    {"korisnicko_ime": "maja_0x", "email": "majaaaaa@gmail.com"},
    {"korisnicko_ime": "zdeslav032", "email": "deso032@gmail.com"}
]

baza_lozinka = [
    {"korisnicko_ime": "mirko123", "lozinka": "lozinka123"},
    {"korisnicko_ime": "ana_anic", "lozinka": "super_teska_lozinka"},
    {"korisnicko_ime": "maja_0x", "lozinka": "s324SDFfdsj234"},
    {"korisnicko_ime": "zdeslav032", "lozinka": "deso123"}
]

async def autorizacija(korisnik, lozinka):
    await asyncio.sleep(2)
    ime = korisnik["korisnicko_ime"]

    for zapis in baza_lozinka:
        if zapis["korisnicko_ime"] == ime and zapis["lozinka"] == lozinka:
            return f"korisnik {ime} je autoriziran"

    return f"korisnik {ime} nije autoriziran"

async def autentifikacija(korisnik):
    await asyncio.sleep(3)
    ime = korisnik["korisnicko_ime"]

    for zapis in baza_korisnika:
        if (
            zapis["korisnicko_ime"] == ime and zapis["email"] == korisnik["email"]
        ):
            return await autorizacija(zapis, korisnik["lozinka"])

    return f"korisnik {ime} nije pronađen"

async def main():
    korisnik = {
        "korisnicko_ime": "mirko123",
        "email": "mirko123@gmail.com",
        "lozinka": "lozinka123"
    }

    rezultat = await autentifikacija(korisnik)
    print(rezultat)

asyncio.run(main())