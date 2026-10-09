# ATSE - Poređenje algoritama sortiranja (Java vs Python)

Projekat upoređuje performanse šest algoritama sortiranja implementiranih
paralelno u **Javi** i **Pythonu**, nad tri tipa ulaznih nizova: nasumični
(`random`), nizovi sa duplikatima (`duplicates`) i veliki nizovi (`bigdata`).
Za svaki algoritam i svaki tip niza meri se **vreme izvršavanja**, **CPU
vreme** i **memorija**, a rezultati se vizualizuju kroz grafikone.

## Algoritmi

|    Algoritmi   |                    Varijante               |
| -------------- | ------------------------------------------ |
| Selection Sort | `SelectionSort`, `ImprovedSelectionSort`   |
| Merge Sort     | `IterativeMergeSort`, `RecursiveMergeSort` |
| Insertion Sort | `InsertionSort`, `RecursiveInsertionSort`  |
| Quick Sort     | `IterativeQuickSort`, `QuickSort`          |
| Bubble Sort    | `BubbleSort`, `BasicBubbleSort`            |
| Heap Sort      | `HeapSort`, `RecursiveHeapSort`            |

## Struktura repozitorijuma

```
├── java/               Java implementacije algoritama (java/sort/) i Benchmark.java
├── python/              Python implementacije algoritama (python/sort/) i Benchmark.py
├── data/                Generatori test podataka (random, duplicates, bigdata)
├── results/             CSV rezultati merenja, po jeziku i po tipu niza
│   ├── java/{random,duplicates,bigdata}/
│   └── python/{random,duplicates,bigdata}/
├── analysis.py          Skripta koja čita results/*.csv i generiše grafikone
└── analysis/            Generisani grafikoni (PNG), po tipu niza
    ├── random/
    ├── duplicates/
    └── bigdata/
```

## Rezultati

Za svaki tip niza (`bigdata`, `duplicates`, `random`) u `analysis/<tip_niza>/`
nalaze se dve vrste grafikona:

- **`chart_JvsP_<Algoritam>_<Metrika>.png`** - poređenje Java vs Python
  implementacije _istog_ algoritma (izoluje uticaj jezika/runtime-a).
- **`chart_<Jezik>_<Porodica>_<Metrika>.png`** - poređenje dve varijante
  _istog_ algoritma unutar istog jezika, npr. `BubbleSort` vs
  `BasicBubbleSort` u Javi (izoluje uticaj algoritamske optimizacije).

Svaka od ovih kombinacija postoji za tri metrike: `Time` (vreme), `CpuTime`
(CPU vreme) i `Memory` (memorija).

## Kako reprodukovati rezultate

1. **Generisanje test podataka** - pokrenuti odgovarajuće generatore iz
   `data/` (`RandomGenerator.java`, `DataGenerator.java`,
   `DatasetGenerator.java`) da se naprave ulazni nizovi.
2. **Java benchmark** - iz foldera `java/` kompajlirati i pokrenuti
   `Benchmark.java`:
   ```
   javac Benchmark.java sort/*.java
   java Benchmark
   ```
   Rezultati se upisuju u `results/java/{random,duplicates,bigdata}/*.csv`.
3. **Python benchmark** - iz foldera `python/` pokrenuti:
   ```
   python Benchmark.py
   ```
   Rezultati se upisuju u `results/python/{random,duplicates,bigdata}/*.csv`.
   Potrebna biblioteka: `psutil`.
4. **Generisanje grafikona** - iz root foldera (`atse/`) pokrenuti:
   ```
   python analysis.py
   ```
   Potrebne biblioteke: `pandas`, `matplotlib`, `numpy`. Grafikoni se
   generišu u `analysis/<tip_niza>/`.

## Kontributori

### Katarina Marić

- Inicijalno podešavanje repozitorijuma
- Implementacija Selection Sort i Merge Sort algoritama (Java i Python)
- Generator nasumičnih (random) nizova
- Osnovna verzija benchmark harnessa (merenje vremena, CPU vremena i memorije)
- Grafikoni za Selection Sort i Merge Sort (Java vs Python, kao i poređenje
  varijanti unutar istog jezika)

### Dunja Mijalčić

- Implementacija Insertion Sort i Quick Sort algoritama (Java i Python)
- Generator nizova sa duplikatima
- Integracija Insertion Sort i Quick Sort u benchmark
- Grafikoni za Insertion Sort i Quick Sort (Java vs Python, kao i poređenje
  varijanti unutar istog jezika)

### Branislava Milovanović

- Implementacija Bubble Sort i Heap Sort algoritama (Java i Python)
- Generator velikih (bigdata) nizova
- Integracija Bubble Sort i Heap Sort u benchmark
- Grafikoni za Bubble Sort i Heap Sort (Java vs Python, kao i poređenje
  varijanti unutar istog jezika)
