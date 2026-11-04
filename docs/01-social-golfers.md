# Problemi 1: Social Golfers Problem (DFS me backtracking)

> **Kërkesa:** 32 lojtarë golfi luajnë një herë në javë, gjithmonë në grupe me nga 4. Për sa
> javë mund të luajnë ashtu që dy lojtarë të mos luajnë së bashku në të njëjtin grup më shumë se
> një herë? Modeloni problemin, tregoni reprezentimin (variablat, domenet etj.), formuloni
> funksionin objektiv, kalkuloni *landscape* dhe implementoni **DFS me Backtracking**.

Kodi: [`uninformed_search/social_golfers.py`](../uninformed_search/social_golfers.py) ·
Testet: [`tests/test_social_golfers.py`](../tests/test_social_golfers.py) ·
Rezultatet: [`results/01-social-golfers.md`](../results/01-social-golfers.md)

---

## 1. Modelimi

Instanca e përgjithshme shënohet **g-p-w**: `n = g·p` lojtarë luajnë çdo javë në `g` grupe me nga
`p` lojtarë, për `w` javë. Detyra kërkon **8-4-w**: 32 lojtarë, 8 grupe me nga 4.

**Kufizimet (të gjitha të forta, nuk ka kufizime të buta):**

* **C1:** çdo javë secili lojtar luan saktësisht një herë (grupet e një jave e ndajnë grupin e
  lojtarëve pa mbetje dhe pa përsëritje);
* **C2:** dy lojtarë luajnë në të njëjtin grup më së shumti një herë gjatë të gjitha javëve.

**Kufiri i sipërm për numrin e javëve.** Çdo javë një lojtar takon `p − 1 = 3` lojtarë të rinj,
ndërsa gjithsej ka `n − 1 = 31` lojtarë të tjerë. Prandaj `3·w ≤ 31`, pra **`w ≤ 10`**. E njëjta
gjë del edhe nga numri i çifteve: çdo javë "përdor" `8 · C(4,2) = 48` çifte nga `C(32,2) = 496`
gjithsej, pra `48·w ≤ 496`.

**Përgjigjja e pyetjes "për sa javë?":** maksimumi është **10 javë**. Kufiri tregon që 11 javë
janë të pamundura, ndërsa një orar konkret me 10 javë njihet në literaturë
([CSPLib prob010](https://www.csplib.org/Problems/prob010/results/)). DFS jonë gjen menjëherë
**5 javë**; për 6 javë nuk mbaron brenda 60 sekondave (shih §6 pse).

## 2. Reprezentimi

| Elementi | Përmbajtja |
|---|---|
| **Variablat** | `x[t][j][k]`: lojtari në javën `t`, grupin `j`, vendin `k` (`w · g · p = 32·w` variabla) |
| **Domeni** | `{0, 1, …, 31}` (numri i lojtarit) |
| **Kufizimet** | C1 dhe C2 nga §1 |

Në kod (`social_golfers.py`):

* `schedule[t][j]`: lista e lojtarëve të grupit `j` në javën `t`;
* `playing[t]`: bashkësia e lojtarëve që janë vendosur tashmë në javën `t` (për C1);
* `met[a]`: bashkësia e lojtarëve me të cilët `a` ka luajtur tashmë (për C2).

Dy rregulla të thjeshta e bëjnë reprezentimin më të vogël pa humbur asnjë zgjidhje:

* brenda një grupi lojtarët shkruhen në rend rritës (grupi `{3, 0, 2, 1}` është i njëjtë me `{0, 1, 2, 3}`);
* çdo grup fillon me lojtarin më të vogël që nuk luan ende atë javë (renditja e grupeve nuk ka rëndësi).

Kështu çdo javë ndërtohet vetëm një herë si ndarje e lojtarëve në grupe. Shembulli i javës 1 në
detyrë (`0 1 2 3 | 4 5 22 23 | …`) është vetëm një nga ndarjet e mundshme; DFS jonë fillon me
`0 1 2 3 | 4 5 6 7 | …`.

## 3. Funksioni objektiv

```
m(a, b) = numri i javëve kur a dhe b janë në të njëjtin grup
f(S)    = Σ  max(0, m(a, b) − 1)      (shuma mbi të gjitha çiftet a < b)
```

`f(S)` numëron takimet e tepërta. Për një orar ku çdo javë është ndarje e lojtarëve (C1),
**`S` është zgjidhje atëherë dhe vetëm atëherë kur `f(S) = 0`**. Funksioni `objective()` e
llogarit `f`, ndërsa `is_valid()` kontrollon C1 dhe `f = 0`.

## 4. Landscape (hapësira e kërkimit)

Madhësia e hapësirës varet nga reprezentimi. Le të jetë `P` numri i mënyrave për t'i ndarë 32
lojtarë në 8 grupe me nga 4 (pa rëndësi renditja e grupeve dhe renditja brenda grupit):

```
P = 32! / ((4!)^8 · 8!) = 59 287 247 761 257 140 625 ≈ 5.93 · 10^19
```

| Reprezentimi | Formula | w = 5 | w = 10 |
|---|---|---|---|
| çdo vend merr çdo lojtar (as C1 nuk vlen) | `32^(32·w)` | 6.67e240 | 4.45e481 |
| çdo javë është një permutacion i 32 lojtarëve (C1 vlen) | `(32!)^w` | 1.26e177 | 1.59e354 |
| çdo javë është një ndarje në grupe (C1 vlen, pa renditje) | `P^w` | 7.32e98 | 5.37e197 |

Reprezentimi i mirë e zvogëlon hapësirën me qindra rende madhësie, por edhe `P^10 ≈ 10^197` është
shumë më e madhe se sa mund të kërkohet plotësisht. Zgjidhjet janë shumë të rralla në këtë
hapësirë, prandaj kontrolli i kufizimeve gjatë ndërtimit (backtracking) është i domosdoshëm.

## 5. Algoritmi: DFS me backtracking

**Formulimi si problem kërkimi:**

* **Gjendja:** orar i pjesshëm, i plotësuar vend pas vendi (java → grupi → vendi në grup);
* **Gjendja fillestare:** orari bosh;
* **Veprimi:** vendos një lojtar në vendin e radhës;
* **Testi i qëllimit:** të gjitha `32·w` vendet janë plotësuar (atëherë `f = 0`);
* **Thellësia e zgjidhjes:** `d = 32·w` (p.sh. 160 për 5 javë).

**Backtracking:** një lojtar vendoset vetëm nëse nuk luan ende atë javë (C1) dhe nuk ka luajtur
më parë me asnjë anëtar të grupit (C2). Nëse për një vend nuk ka asnjë lojtar të lejuar, nyja
është *dead end*: DFS e zhbën vendosjen e fundit dhe provon lojtarin tjetër në vendin paraprak.

```text
DFS(vendi):
    nëse të gjitha vendet janë plotësuar:  kthe SUKSES
    kandidatët ← lojtarët e lejuar për këtë vend (C1, C2, rendi rritës në grup)
    për çdo lojtar në kandidatët (nga më i vogli):
        vendose lojtarin; shëno takimet e reja në met[]
        nëse DFS(vendi + 1) == SUKSES:  kthe SUKSES
        hiqe lojtarin; fshi takimet                      # backtracking
    kthe DËSHTIM                                         # asnjë lojtar nuk funksionoi
```

Për pyetjen "sa javë?" programi provon `w = 1, 2, 3, …` me DFS (`--max-weeks`) derisa DFS të
dështojë ose të arrijë kufirin e kohës.

## 6. Kompleksiteti

* **Koha:** `O(b^d)`, me `d = 32·w` (thellësia) dhe `b ≤ 32` (lojtarë të mundshëm për një vend).
* **Hapësira:** `O(d)`: DFS mban në kujtesë vetëm shtegun aktual (për 5 javë 160 nyje) plus
  bashkësitë `met`. Kjo është përparësia kryesore e DFS kundrejt BFS.
* **Plotësia:** pema është e fundme, prandaj DFS është e plotë: nëse mbaron pa zgjidhje,
  instanca është e pamundur (p.sh. 2-4-2 në §7).
* **Optimaliteti:** nuk ka rëndësi, sepse të gjitha zgjidhjet janë në të njëjtën thellësi.

**Pse DFS ngec te java e 6-të.** Me lojtarët e provuar nga më i vogli, DFS ndërton javët 2-5 ashtu
që lojtarët 0-15 takohen vetëm me njëri-tjetrin dhe po ashtu lojtarët 16-31. Pas 5 javësh lojtari 0
i ka takuar të gjithë lojtarët 1-15, prandaj në javën 6 duhet të luajë me tre lojtarë nga 16-31,
por ata janë takuar tashmë të gjithë me njëri-tjetrin. Java 6 është e pamundur me këto 5 javë, por
DFS e zbulon këtë vetëm thellë në pemë dhe duhet të provojë shumë kombinime të javëve 2-5 para
se ta ndryshojë gabimin e hershëm. Kjo është dobësia e njohur e DFS me backtracking kronologjik:
një vendim i keq në fillim zbulohet shumë vonë.

## 7. Rezultatet

Nga `python -m uninformed_search bench` (kufiri 60 s); tabelat e plota janë në
[`results/01-social-golfers.md`](../results/01-social-golfers.md).

**32 lojtarë (8-4-w):**

| w | Rezultati | Nyje të gjeneruara | Dead ends | Koha (s) |
|---|---|---|---|---|
| 1 | zgjidhje | 32 | 0 | 0.000 |
| 2 | zgjidhje | 64 | 0 | 0.000 |
| 3 | zgjidhje | 96 | 0 | 0.000 |
| 4 | zgjidhje | 128 | 0 | 0.000 |
| 5 | zgjidhje | 160 | 0 | 0.000 |
| 6 | kufiri i kohës | 55 530 000 | 26 096 103 | 60.0 |

Rreshti për `w = 6` varet nga shpejtësia e kompjuterit: brenda 60 sekondave DFS gjeneron rreth 55
milion nyje, nga të cilat gati gjysma janë dead ends, dhe nuk zbret më thellë se vendi 163 (java 6).

**Instanca të vogla:**

| Instanca | Lojtarë | Kufiri i sipërm | Rezultati | Nyje të gjeneruara |
|---|---|---|---|---|
| 2-2-3 | 4 | 3 | zgjidhje | 12 |
| 3-2-5 | 6 | 5 | zgjidhje | 36 |
| 3-3-4 | 9 | 4 | zgjidhje | 37 |
| 4-3-4 | 12 | 5 | zgjidhje | 407 |
| 4-4-5 | 16 | 5 | zgjidhje | 80 |
| 5-5-6 | 25 | 6 | zgjidhje | 2 246 |
| 2-4-2 | 8 | 2 | **e pamundur** (DFS e shterron pemën) | 519 |

Te instancat e vogla DFS e arrin kufirin e sipërm të javëve. Te 2-4-2 kufiri lejon 2 javë, por DFS
vërteton se nuk ka orar: në javën e dytë secili grup do të kishte dy lojtarë nga i njëjti grup i
javës së parë.

Orari me 5 javë i gjetur nga DFS:

```text
Java  1:   0  1  2  3  |   4  5  6  7  |   8  9 10 11  |  12 13 14 15  |  16 17 18 19  |  20 21 22 23  |  24 25 26 27  |  28 29 30 31
Java  2:   0  4  8 12  |   1  5  9 13  |   2  6 10 14  |   3  7 11 15  |  16 20 24 28  |  17 21 25 29  |  18 22 26 30  |  19 23 27 31
Java  3:   0  5 10 15  |   1  4 11 14  |   2  7  8 13  |   3  6  9 12  |  16 21 26 31  |  17 20 27 30  |  18 23 24 29  |  19 22 25 28
Java  4:   0  6 11 13  |   1  7 10 12  |   2  4  9 15  |   3  5  8 14  |  16 22 27 29  |  17 23 26 28  |  18 20 25 31  |  19 21 24 30
Java  5:   0  7  9 14  |   1  6  8 15  |   2  5 11 12  |   3  4 10 13  |  16 23 25 30  |  17 22 24 31  |  18 21 27 28  |  19 20 26 29
```

## 8. Ekzekutimi

```bash
python -m uninformed_search golfers -w 5                  # 8-4-5 me DFS
python -m uninformed_search golfers --max-weeks           # w = 1, 2, ... derisa DFS të ndalet
python -m uninformed_search golfers -g 3 -p 3 -w 4        # instancë tjetër
python -m uninformed_search golfers -w 10 --landscape     # madhësia e hapësirës së kërkimit
```

## 9. Përfundime

* Përgjigjja është **10 javë** (kufi i vërtetuar me numërim + orar i njohur në literaturë).
* DFS me backtracking përdor shumë pak memorie dhe gjen menjëherë 5 javë, por për 6 javë ngec,
  sepse vendimet e javëve të para nuk ndryshohen derisa të provohen shumë kombinime të javëve
  pasuese. Hapësira (`10^98` deri në `10^197`) është shumë e madhe për kërkim të painformuar.
* Te instancat e vogla DFS e arrin kufirin e sipërm ose vërteton që nuk ka zgjidhje.
