# Prednost domačega terena in boj za vrh v Premier League (1992–2026)

Projektna naloga pri predmetu **Uvod v programiranje** (FMF, Univerza v Ljubljani).

Analiziral sem lestvice angleške Premier League od sezone 1992/93 do 2025/26 (34 sezon).
Zanimalo me je, koliko prednosti prinaša domači teren, kaj se je zgodilo, ko so zaradi
covida-19 tekme igrali brez gledalcev, ter kateri klubi so najpogosteje na vrhu in na dnu
lestvice. Podatke sem pridobil s strani [11v11.com](https://www.11v11.com/league-tables/),
analiziral pa sem jih v Jupyter zvezku.

## Pridobivanje in obdelava podatkov

V datoteki `prenos_strani.py` je funkcija, ki s knjižnico `requests` za vsako sezono prenese
tri lestvice: skupno lestvico, lestvico samo tekem doma in lestvico samo tekem v gosteh.
Za sezono 2019/20 prenese še lestvici doma in v gosteh na dan 13. 3. 2020, ko so ligo
prekinili zaradi covida-19. Vseh 104 strani shrani v mapo `html_strani/`.

Datoteka `izlusci_podatke.py` s knjižnico BeautifulSoup iz vsake strani prebere tabelo
z lestvico in vse lestvice zapiše v `podatki/lestvice.csv`. Vsaka vrstica je en klub na
eni lestvici, stolpci pa so:

| Stolpec | Pomen |
|---|---|
| `sezona` | sezona, npr. `1992-93` |
| `vrsta` | `skupaj`, `doma`, `v_gosteh`, `doma_do_prekinitve` ali `v_gosteh_do_prekinitve` |
| `mesto` | mesto kluba na lestvici |
| `klub` | ime kluba |
| `tekme`, `zmage`, `remiji`, `porazi` | število odigranih tekem, zmag, remijev in porazov |
| `dani_goli`, `prejeti_goli` | dani in prejeti goli |
| `tocke` | točke |

Pri lestvicah doma in v gosteh so točke izračunane kot 3 × zmage + remiji, ker 11v11
odvzete točke (Middlesbrough 1996/97) odšteje v obeh lestvicah hkrati. Pri skupni lestvici
so uporabljene uradne točke.

## Analiza

V zvezku `analiza.ipynb` sem s knjižnicama Pandas in Matplotlib uvozil podatke in iz njih
naredil grafe:

* **Graf 1:** Izidi tekem po sezonah (zmage domačih, remiji, zmage gostov)
* **Graf 2:** Povprečno število golov na tekmo za domače in goste
* **Graf 3:** Izidi tekem pred covidom in med njim (tekme brez gledalcev)
* **Graf 4:** Razlika v točkah na tekmo doma in v gosteh po klubih
* **Graf 5:** Kdo je največkrat končal med prvimi tremi
* **Graf 6:** Kdo je največkrat končal na zadnjih treh mestih
* **Graf 7:** Točke na tekmo prvih treh in zadnjih treh klubov po sezonah

## Ugotovitve

Domači teren prinaša jasno prednost: domači zmagajo na 45,7 % tekem, gostje le na 28,7 %,
doma pa dajo približno tretjino golov več (1,53 proti 1,16 gola na tekmo). Vsi klubi, ki so
v ligi igrali vsaj 10 sezon, osvojijo doma več točk kot v gosteh. Prednost prinašajo predvsem
navijači: v sezoni 2020/21, ko so tekme igrali brez gledalcev, so gostje zmagali celo
pogosteje kot domači (40,3 % proti 37,9 %).

Vrh lige je zelo zaprt, saj je bilo v 34 sezonah le 7 različnih prvakov, dno pa je odprto,
saj je na zadnjih treh mestih končalo 43 različnih klubov. Liga postaja vse bolj neenakomerna:
razlika med prvimi tremi in zadnjimi tremi klubi je narasla z 1,09 točke na tekmo v prvih
10 sezonah na 1,48 v zadnjih 10 sezonah.

## Navodila za zagon

Potrebujete Python 3. Ukazi so napisani za Windows (`py`); na macOS in Linuxu namesto `py`
uporabite `python3`.

**1. Prenos repozitorija**

```
git clone https://github.com/aljazzorc/project_uvp.git
cd project_uvp
```

**2. Namestitev knjižnic**

```
py -m pip install requests beautifulsoup4 pandas matplotlib jupyter
```

**3. Prenos HTML strani**

```
py prenos_strani.py
```

Program v mapo `html_strani/` shrani 104 strani. Med prenosi počaka 3 sekunde, zato traja
približno 6 minut. Že shranjene strani preskoči, zato ga lahko kadarkoli prekinete in
ponovno zaženete.

**4. Izluščanje podatkov**

```
py izlusci_podatke.py
```

Program ustvari datoteko `podatki/lestvice.csv` in na koncu izpiše
`Zapisano: podatki\lestvice.csv (2098 vrstic)`.

Ta korak in prejšnjega lahko preskočite, saj je datoteka `podatki/lestvice.csv` že v repozitoriju.

**5. Analiza**

```
py -m jupyter notebook analiza.ipynb
```

V brskalniku se odpre zvezek; zaženite vse celice (*Run → Run All Cells*). Zvezek lahko
odprete tudi v VS Code in kliknete *Run All*.