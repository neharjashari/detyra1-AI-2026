# Problemi 3: Latin Square (IDDFS me backtracking)

> **Kërkesa:** Një katror latin është një rrjetë `n × n` e mbushur me `n` numra të ndryshëm, ku
> secili shfaqet saktësisht një herë në çdo rresht dhe çdo kolonë. Për një hyrje `n` printoni një
> matricë `n × n` me numrat 1 deri në `n`. Modeloni problemin, tregoni reprezentimin, formuloni
> funksionin objektiv, kalkuloni *landscape* dhe implementoni **IDDFS dhe Backtracking**.

Kodi: [`uninformed_search/latin_square.py`](../uninformed_search/latin_square.py) ·
Testet: [`tests/test_latin_square.py`](../tests/test_latin_square.py) ·
Rezultatet: [`results/03-latin-square.md`](../results/03-latin-square.md)

---

## 1. Modelimi

Hyrja është `n`. Duhet një matricë `n × n` me vlera nga `1` deri në `n`.

**Kufizimet (të gjitha të forta):**

* në çdo rresht vlerat janë të ndryshme;
* në çdo kolonë vlerat janë të ndryshme.

Problemi ka gjithmonë zgjidhje: p.sh. rreshti `i` mund të jetë rreshti i parë i zhvendosur për
`i` vende (si shembulli në detyrë). Këtu zgjidhja gjendet me kërkim, jo me formulë.

## 2. Reprezentimi

| Elementi | Përmbajtja |
|---|---|
| **Variablat** | `L[i][j]`, një për secilën qelizë (`n²` variabla; për `n = 5`: 25) |
| **Domeni** | `{1, 2, …, n}` |
| **Kufizimet** | `L[i][j] ≠ L[i][j']` (rreshti) dhe `L[i][j] ≠ L[i'][j]` (kolona) |

Në kod (`latin_square.py`):

* `square[i][j]`: matrica, `0` = qelizë ende bosh;
* `in_row[i]` dhe `in_column[j]`: bashkësitë e vlerave të përdorura në rreshtin `i` dhe kolonën `j`,
  që kontrolli "a lejohet vlera `v`?" të jetë i shpejtë.

Qelizat plotësohen rresht pas rreshti: qeliza numër `d` është `(d / n, d mod n)`.

## 3. Funksioni objektiv

```
f(L) = Σ (n − numri i vlerave të ndryshme në rreshtin i)  +  Σ (n − numri i vlerave të ndryshme në kolonën j)
```

Çdo vlerë e përsëritur në një rresht ose kolonë e rrit `f`. **`f(L) = 0` atëherë dhe vetëm atëherë
kur `L` është katror latin.** Funksioni `objective()` e llogarit `f` dhe programi e printon për
zgjidhjen e gjetur (`f = 0`).

## 4. Landscape (hapësira e kërkimit)

| n | qeliza `n²` | çdo qelizë çdo vlerë `n^(n²)` | çdo rresht permutacion `(n!)^n` | katrorë latinë `L(n)` | pjesa e zgjidhjeve `L(n) / n^(n²)` |
|---|---|---|---|---|---|
| 3 | 9 | 19 683 | 216 | 12 | 10^-3.2 |
| 4 | 16 | 4.29e9 | 331 776 | 576 | 10^-6.9 |
| **5** | **25** | **2.98e17** | **2.49e10** | **161 280** | **10^-12.3** |
| 6 | 36 | 1.03e28 | 1.39e17 | 8.13e8 | 10^-19.1 |
| 7 | 49 | 2.57e41 | 8.26e25 | 6.15e13 | 10^-27.6 |

`L(n)` është numri i njohur i katrorëve latinë ([OEIS A002860](https://oeis.org/A002860)); testet e
kontrollojnë për `n ≤ 4` me numërim të plotë. Zgjidhje ka shumë, por pjesa e tyre në hapësirë bie
shumë shpejt: për `n = 5` vetëm një nga rreth 10^12 mbushje është katror latin.

## 5. Algoritmi: IDDFS me backtracking

**Formulimi si problem kërkimi:**

* **Gjendja:** matrica e pjesshme me `d` qelizat e para të plotësuara, pa asnjë përsëritje;
* **Gjendja fillestare:** matrica bosh;
* **Veprimi:** shkruaj një vlerë të lejuar në qelizën e radhës;
* **Testi i qëllimit:** të gjitha `n²` qelizat janë plotësuar;
* **Thellësia e zgjidhjes:** gjithmonë `d = n²` (25 për `n = 5`).

**IDDFS** (*Iterative Deepening DFS*) ekzekuton një DFS me kufi thellësie (`depth-limited DFS`)
për kufijtë `L = 0, 1, 2, …`. Në çdo iteracion DFS nuk zbret më thellë se `L`; nëse ka nyje që u
ndalën te kufiri (*cutoff*), kufiri rritet dhe kërkimi fillon nga e para.

**Backtracking:** një vlerë vendoset në një qelizë vetëm nëse nuk gjendet në të njëjtin rresht ose
në të njëjtën kolonë. Nëse asnjë vlerë nuk lejohet, nyja është *dead end* dhe DFS kthehet mbrapa,
e zhbën vlerën e fundit dhe provon vlerën tjetër.

```text
IDDFS(n):
    për L = 0, 1, 2, …, n²:
        rezultati ← DLS(0, L)
        nëse rezultati == ZGJIDHJE:  kthe matricën
        nëse rezultati == DËSHTIM:   kthe "pa zgjidhje"      # nuk pati asnjë cutoff

DLS(d, L):                                                   # depth-limited DFS
    nëse d == n²:  kthe ZGJIDHJE
    nëse d == L:   kthe CUTOFF
    (i, j) ← qeliza numër d
    për çdo vlerë v nga 1 te n që nuk është në rreshtin i dhe kolonën j:
        L[i][j] ← v
        r ← DLS(d + 1, L)
        nëse r == ZGJIDHJE:  kthe ZGJIDHJE
        L[i][j] ← bosh                                       # backtracking
    kthe CUTOFF nëse ndonjë fëmijë ktheu CUTOFF, përndryshe DËSHTIM
```

## 6. Kompleksiteti

* **Koha:** `O(b^d)`, me `d = n²` dhe `b ≤ n`. IDDFS e përsërit punën e niveleve të sipërme në çdo
  iteracion.
* **Hapësira:** `O(d) = O(n²)`: si DFS, mban vetëm shtegun aktual.
* **Plotësia:** IDDFS është e plotë (si BFS) dhe përdor pak memorie (si DFS).
* **Optimaliteti:** IDDFS gjen zgjidhjen më të cekët; këtu të gjitha zgjidhjet janë në thellësinë `n²`.

**Kur IDDFS është e mirë dhe kur jo.** Zakonisht IDDFS kushton pak më shumë se BFS, sepse shumica e
nyjeve janë në nivelin e fundit dhe nivelet e sipërme përsëriten lirë. Te katrori latin situata
është e kundërta:

* çdo zgjidhje është në thellësinë maksimale `n²`, prandaj të gjitha iteracionet `L < n²` dështojnë
  me siguri dhe vetëm e harxhojnë kohën;
* backtracking-u e ngushton pemën në nivelet e thella, kështu që nivelet e fundit nuk janë shumë më
  të mëdha se ato të mesit dhe përsëritja kushton shumë.

Iteracioni i fundit (`L = n²`) është vetë një DFS me backtracking, prandaj e gjen zgjidhjen shpejt.
Për `n = 5` ai gjeneron vetëm **37 nyje**, ndërsa IDDFS gjithsej gjeneron **13 505 897** nyje
(365 024 herë më shumë). Kjo nuk është gabim i implementimit, por vetia e IDDFS kur zgjidhjet janë
gjithmonë në thellësinë maksimale.

## 7. Rezultatet

Nga `python -m uninformed_search bench` (kufiri 60 s); tabelat e plota janë në
[`results/03-latin-square.md`](../results/03-latin-square.md).

| n | Rezultati | Iteracione | Nyje gjithsej | Nyje në iteracionin e fundit | Koha (s) |
|---|---|---|---|---|---|
| 1 | zgjidhje | 2 | 1 | 1 | 0.000 |
| 2 | zgjidhje | 5 | 16 | 4 | 0.000 |
| 3 | zgjidhje | 10 | 316 | 10 | 0.000 |
| 4 | zgjidhje | 17 | 24 844 | 16 | 0.011 |
| 5 | zgjidhje | 26 | 13 505 897 | 37 | 6.907 |
| 6 | kufiri i kohës | 18 të përfunduara (nga 37) | 134 620 000 | - | 60.0 |

Nyjet për çdo iteracion për `n = 5` (pjesë nga tabela e plotë në `results/`):

| Kufiri L | 0 | 1 | 5 | 10 | 15 | 20 | 24 | **25** |
|---|---|---|---|---|---|---|---|---|
| Nyje të gjeneruara | 0 | 5 | 325 | 17 845 | 316 885 | 1 507 765 | 2 152 885 | **37** |

Çdo iteracion `L < 25` përfundon me *cutoff*; vetëm iteracioni `L = 25` arrin te zgjidhja.

Zgjidhja për `n = 5`:

```text
1 2 3 4 5
2 1 4 5 3
3 4 5 1 2
4 5 2 3 1
5 3 1 2 4
```

## 8. Ekzekutimi

```bash
python -m uninformed_search latin -n 5              # IDDFS për n = 5
python -m uninformed_search latin -n 4 -v           # me nyjet e çdo iteracioni
python -m uninformed_search latin -n 5 --landscape  # madhësia e hapësirës së kërkimit
```

## 9. Përfundime

* IDDFS me backtracking e zgjidh problemin deri në `n = 5` (rreth 7 s); për `n = 6` nuk mbaron
  brenda 60 s.
* Backtracking-u e zvogëlon shumë pemën: për `n = 5` hapësira ka `10^17` mbushje, ndërsa IDDFS
  gjeneron 1.35 · 10^7 nyje.
* IDDFS kombinon plotësinë e BFS me memorien e vogël të DFS, por këtu paguan shumë për përsëritjen
  e iteracioneve, sepse zgjidhja është gjithmonë në nivelin më të thellë.
