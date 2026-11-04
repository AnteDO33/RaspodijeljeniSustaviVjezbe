import asyncio


async def timer(name, delay):
    for i in range(delay, 0, -1):
        print(f"{name}: {i} sekundi preostalo...")

        # Korutina čeka jednu sekundu i prepušta izvršavanje event loopu.
        # Za to vrijeme event loop može izvršavati druge spremne zadatke.
        await asyncio.sleep(1)

    # Ovaj se ispis izvršava nakon završetka cijele petlje.
    print(f"{name}: Vrijeme je isteklo!")


async def main():
    # create_task stvara zadatke i raspoređuje ih za izvršavanje.
    timers = [
        asyncio.create_task(timer("Timer 1", 3)),
        asyncio.create_task(timer("Timer 2", 5)),
        asyncio.create_task(timer("Timer 3", 7))
    ]

    # main čeka dovršetak sva tri zadatka.
    # Event loop za to vrijeme izvršava korutine timer.
    await asyncio.gather(*timers)


# Pokreće event loop i korutinu main.
asyncio.run(main())


# OBJAŠNJENJE IZVRŠAVANJA:
# 1. asyncio.run(main()) pokreće event loop i započinje main.
# 2. create_task stvara tri zadatka koji su spremni za izvršavanje.
# 3. Na await asyncio.gather(*timers), main prelazi u čekanje.
# 4. Event loop izvršava svaki timer do njegova await asyncio.sleep(1).
#    Timer tada prelazi u čekanje, a drugi spremni zadaci mogu se izvršavati.
# 5. Nakon isteka čekanja timer ponovno postaje spreman za izvršavanje.
#    Kad dobije priliku, nastavlja nakon await izraza i prelazi u sljedeći
#    krug petlje. To se ponavlja dok petlja ne završi.
# 6. Nakon petlje timer ispisuje završnu poruku i zadatak je završen.
# 7. Kada sva tri zadatka završe, main nastavlja nakon gather i završava.
#    asyncio.run potom zatvara event loop.
#
# OČEKIVANI TIJEK (vremena su približna):
# 0 s: Timer 1 ispisuje 3, Timer 2 ispisuje 5, Timer 3 ispisuje 7.
# 1 s: Timer 1 ispisuje 2, Timer 2 ispisuje 4, Timer 3 ispisuje 6.
# 2 s: Timer 1 ispisuje 1, Timer 2 ispisuje 3, Timer 3 ispisuje 5.
# 3 s: Timer 1 završava, Timer 2 ispisuje 2, Timer 3 ispisuje 4.
# 4 s: Timer 2 ispisuje 1, Timer 3 ispisuje 3.
# 5 s: Timer 2 završava, Timer 3 ispisuje 2.
# 6 s: Timer 3 ispisuje 1.
# 7 s: Timer 3 završava. Nakon toga završava i main.
#
# Faze zadatka: spreman -> izvršava se -> čeka -> ponovno spreman.
# Nakon posljednjeg čekanja korutina se nastavlja i završava.
# Dok se zadatak izvršava ili čeka, task.done() vraća False.
# Nakon dovršetka task.done() vraća True.
# Korutine se izvršavaju konkurentno; event loop ih izmjenjuje pri čekanju.
# Ukupno trajanje programa je približno 7 sekundi.
