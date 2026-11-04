# Problemi 2: Sudoku Solver (BFS me backtracking)

> **Kërkesa:** Shkruani programin që zgjidh një Sudoku. Programi duhet t'i parashohë tri nivele:
> *Easy*, *Medium*, *Hard*. Modeloni problemin, tregoni reprezentimin (variablat, domenet etj.),
> formuloni funksionin objektiv, kalkuloni *landscape* dhe implementoni **BFS me Backtracking**.

Kodi: [`uninformed_search/sudoku.py`](../uninformed_search/sudoku.py) ·
Enigmat: [`data/sudoku/`](../data/sudoku/) ·
Testet: [`tests/test_sudoku.py`](../tests/test_sudoku.py) ·
Rezultatet: [`results/02-sudoku.md`](../results/02-sudoku.md)

---

## 1. Modelimi

Rrjeta 9×9 ka 9 rreshta, 9 kolona dhe 9 kuti 3×3, pra **27 njësi**. Disa qeliza janë të dhëna
(*dhënat*), të tjerat duhet të plotësohen.

**Kufizimet (të gjitha të forta):**

* çdo rresht, çdo kolonë dhe çdo kuti 3×3 përmban shifrat 1-9 secilën saktësisht një herë;
* dhënat nuk ndryshohen.

## 2. Reprezentimi

| Elementi | Përmbajtja |
|---|---|
| **Variablat** | qelizat bosh të enigmës (`k` variabla; p.sh. `k = 49` kur ka 32 dhëna) |
| **Domeni** | `{1, 2, …, 9}` për çdo qelizë bosh |
| **Kufizimet** | në asnjë rresht, kolonë apo kuti nuk përsëritet një shifër |

Në kod rrjeta është një **string me 81 karaktere**, rresht pas rreshti; `.` është qelizë bosh.
P.sh. rreshti i parë i `euler-01` është `..3.2.6..`. Funksionet `row_of`, `column_of` dhe
`box_of` japin rreshtin, kolonën dhe kutinë e një qelize, ndërsa `allowed_digits(grid, cell)`
kthen shifrat që nuk gjenden në asnjërën prej tyre.

**Nivelet Easy / Medium / Hard.** Niveli përcaktohet nga numri i dhënave (`level_of()`):

| Niveli | Dhëna | Qeliza bosh `k` |
|---|---|---|
| easy | 30 ose më shumë | 51 ose më pak |
| medium | 26 deri në 29 | 52 deri në 55 |
| hard | 25 ose më pak | 56 ose më shumë |

Më pak dhëna do të thotë më shumë qeliza bosh, pra pema e kërkimit është më e thellë (zgjidhja
është në thellësinë `k`) dhe zakonisht më e gjerë. Enigmat në `data/sudoku/` janë dy rrjetat e
para të secilit nivel nga [Project Euler, problemi 96](https://projecteuler.net/problem=96), plus
enigma e Arto Inkala (2012) si shembull i njohur i nivelit hard. Programi pranon edhe një enigmë
tjetër me `--puzzle` dhe e klasifikon sipas të njëjtit rregull.

## 3. Funksioni objektiv

Për një rrjetë të plotë `X`:

```
f(X) = Σ  (9 − numri i shifrave të ndryshme në njësinë u)      (shuma mbi 27 njësitë u)
```

Çdo shifër e përsëritur në një njësi e rrit `f`. **`f(X) = 0` atëherë dhe vetëm atëherë kur `X`
është zgjidhje** (dhe ruan dhënat). Funksioni `objective()` e llogarit `f`, ndërsa
`is_solution()` kontrollon që rrjeta është e plotë, `f = 0` dhe dhënat janë ruajtur.

## 4. Landscape (hapësira e kërkimit)

Për një enigmë me `k` qeliza bosh:

| Reprezentimi | Madhësia | euler-01 (`k = 49`) | inkala-2012 (`k = 60`) |
|---|---|---|---|
| çdo qelizë bosh merr çdo shifër | `9^k` | 5.73e46 | 1.80e57 |
| çdo rresht plotësohet me një renditje të shifrave që i mungojnë | `Π (qeliza bosh në rresht)!` | 7.80e21 | 6.99e30 |
| zgjidhje | 1 | 1 | 1 |

Për krahasim, një rrjetë krejt bosh ka `9^81 ≈ 1.97 · 10^77` mbushje të mundshme, ndërsa rrjeta të
vlefshme Sudoku ka vetëm `6 670 903 752 021 072 936 960 ≈ 6.67 · 10^21` (Felgenhauer & Jarvis, 2005).

Në hapësirën e kërkimit ka vetëm **një** rrjetë me `f = 0`. Prandaj nuk mund të provohen të gjitha
rrjetat: kufizimet duhet të kontrollohen gjatë ndërtimit, dhe kjo është detyra e backtracking-ut.

## 5. Algoritmi: BFS me backtracking

**Formulimi si problem kërkimi:**

* **Gjendja:** rrjetë e pjesërisht e plotësuar, pa asnjë shifër të përsëritur;
* **Gjendja fillestare:** enigma;
* **Veprimi:** shkruaj një shifër të lejuar në **qelizën e parë bosh** (rresht pas rreshti);
* **Testi i qëllimit:** nuk ka më qeliza bosh;
* **Thellësia e zgjidhjes:** `d = k`, numri i qelizave bosh.

BFS e eksploron pemën **nivel pas niveli** me një radhë FIFO: së pari të gjitha gjendjet me një
qelizë të plotësuar, pastaj ato me dy, e kështu me radhë.

**Backtracking në BFS:** fëmijët krijohen vetëm për shifrat që nuk shkelin asnjë kufizim. Nëse
qeliza e parë bosh e një gjendjeje nuk ka asnjë shifër të lejuar, gjendja është *dead end*: nuk
krijon fëmijë dhe dega braktiset, kurse BFS vazhdon me gjendjen tjetër në radhë. Pa këtë kontroll
BFS do të ndërtonte të gjitha `9^k` rrjetat dhe do ta testonte `f` vetëm në fund.

```text
BFS-Sudoku(enigma):
    radha ← [enigma]
    derisa radha nuk është bosh:
        s ← merre të parën nga radha
        i ← qeliza e parë bosh në s
        për çdo shifër v të lejuar në i (jo në rresht, kolonë, kuti):
            fëmija ← s me v në qelizën i
            nëse fëmija nuk ka qeliza bosh:  kthe fëmijën       # qëllimi
            shtoje fëmijën në fund të radhës
        (nëse s nuk ka asnjë shifër të lejuar, ajo është dead end dhe braktiset)
    kthe "pa zgjidhje"
```

Testi i qëllimit bëhet kur fëmija krijohet, si te BFS në AIMA (kap. 3). Programi ndalon edhe nëse
radha kalon 2 000 000 gjendje (kufiri i memories) ose nëse kalon kufiri i kohës.

## 6. Kompleksiteti

* **Koha:** `O(b^d)`, me `d = k` (qelizat bosh) dhe `b ≤ 9`.
* **Hapësira:** `O(b^d)`: BFS mban në radhë një nivel të tërë të pemës. Kjo është dobësia kryesore
  e BFS për Sudoku: zgjidhja është gjithmonë në nivelin më të thellë `k`, kështu që BFS nuk përfiton
  nga vetia e saj kryesore (gjen zgjidhjen më të cekët), por paguan me memorie. Për enigmën
  inkala-2012 radha arrin 356 812 gjendje.
* **Plotësia:** BFS është e plotë: nëse ka zgjidhje e gjen, nëse radha zbrazet enigma s'ka zgjidhje.
* **Optimaliteti:** BFS gjen zgjidhjen më të cekët, por këtu të gjitha zgjidhjet kanë thellësi `k`.

## 7. Rezultatet

Nga `python -m uninformed_search bench`; tabela e plotë është në
[`results/02-sudoku.md`](../results/02-sudoku.md).

| Niveli | Enigma | Dhëna | Bosh `k` | Nyje të gjeneruara | Dead ends | Radha max | Koha (s) |
|---|---|---|---|---|---|---|---|
| easy | euler-01 | 32 | 49 | 928 | 274 | 146 | 0.001 |
| easy | euler-02 | 30 | 51 | 2 169 | 658 | 235 | 0.003 |
| medium | euler-03 | 28 | 53 | 22 918 | 6 674 | 3 616 | 0.036 |
| medium | euler-07 | 26 | 55 | 16 164 | 4 867 | 2 212 | 0.025 |
| hard | euler-06 | 24 | 57 | 181 883 | 65 346 | 49 303 | 0.311 |
| hard | euler-26 | 24 | 57 | 12 876 | 3 704 | 1 395 | 0.020 |
| hard | inkala-2012 | 21 | 60 | 2 068 780 | 705 261 | 356 812 | 3.249 |

Vërejtje:

* Të 7 enigmat zgjidhen. Mesatarisht puna e BFS rritet nga easy (rreth 1 500 nyje) te medium
  (rreth 20 000) dhe hard (deri në 2 milion).
* Numri i dhënave është masë e përafërt: `euler-26` (hard, 24 dhëna) kërkon më pak nyje se
  `euler-03` (medium, 28 dhëna). Puna e BFS varet edhe nga sa shifra lejohen në qelizat e para
  bosh, sepse ato përcaktojnë sa e gjerë bëhet pema në nivelet e para.
* Rreth një e treta e nyjeve janë dead ends: aty backtracking-u e ndërpret degën.

## 8. Ekzekutimi

```bash
python -m uninformed_search sudoku                          # të gjitha nivelet
python -m uninformed_search sudoku --level hard             # vetëm një nivel
python -m uninformed_search sudoku --level easy --landscape # edhe madhësia e hapësirës
python -m uninformed_search sudoku --puzzle "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."
```

## 9. Përfundime

* Me backtracking BFS nuk e ndërton hapësirën `9^k` (deri në `10^57`), por vetëm gjendjet pa
  shkelje: nga disa qindra nyje (easy) deri në rreth 2 milion (inkala-2012).
* BFS është e plotë, por shpenzon shumë memorie sepse zgjidhja është në nivelin më të thellë.
  Kjo është arsyeja pse për probleme të tilla zakonisht preferohet DFS.
