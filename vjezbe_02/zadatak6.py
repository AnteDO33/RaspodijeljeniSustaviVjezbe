#Pitanje:

#Kako možete unutar main korutine natjerati event loop da obuhvati ispis unutar korutine
#fetch_data(2) bez da ju awaitate unutar main funkcije? Preciznije, dokažite kako se može ispisati
#tekst Dovršio sam s 2. unutar korutine fetch_data(2) bez da eksplicitno pozivate await task2
#unutar main() funkcije.

import asyncio, time
async def fetch_data(param):
	print(f"Nešto radim s {param}...")
	await asyncio.sleep(param)
	print(f'Dovršio sam s {param}.')
	return f"Rezultat za {param}"

async def main():
	task1 = asyncio.create_task(fetch_data(1)) # schedule
	task2 = asyncio.create_task(fetch_data(2)) # schedule
	result1 = await task1
	print("Fetch 1 uspješno završen.")
	await asyncio.wait({task2})  # wait without explicitly awaiting task2
	return [result1]

t1 = time.perf_counter()
results = asyncio.run(main()) # pokretanje event loop-a
t2 = time.perf_counter()
print(results)
print(f"Vrijeme izvođenja {t2 - t1:.2f} sekunde")

#U korutinu main() nakon await task1, dodajemo
#await asyncio.sleep(2). Time privrmeno pauziramo
#main(), dok event loop nastavlja izvršavati ostale zadatke.
#Zato task2 stigne završiti i ispiati "Dovršio sam s 2." unutar korutine fetch_data(2) bez eksplicitnog poziva await task2.

#Izmijena izgleda ovako:

async def main():
    task1 = asyncio.create_task(fetch_data(1))
    task2 = asyncio.create_task(fetch_data(2))

    result1 = await task1
    print("Fetch 1 uspješno završen.")

    await asyncio.sleep(2)

    return [result1]

#task2 završva nakon približno 2 sekunde, a cijeli
#program nakon 3 sekunde.