import os

import pandas as pd
from bs4 import BeautifulSoup


MAPA_HTML = "html_strani"
POT_CSV = os.path.join("podatki", "lestvice.csv")

PRVO_LETO = 1993
ZADNJE_LETO = 2026

VRSTE = ["skupaj", "doma", "v_gosteh"]
VRSTE_PREKINITEV = ["doma_do_prekinitve", "v_gosteh_do_prekinitve"]
LETO_PREKINITVE = 2020

KLUB, TEKME, ZMAGE, REMIJI, PORAZI, DANI, PREJETI, TOCKE = 1, 2, 3, 4, 5, 6, 7, 9


def oznaka_sezone(leto):
    return f"{leto - 1}-{leto % 100:02d}"


def stevilo(celice, indeks):
    return int(celice[indeks].get_text(strip=True))


def izlusci_lestvico(pot, sezona, vrsta):
    with open(pot, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    tabela = soup.find("table", id="table-league")
    if tabela is None:
        print(f"V datoteki {pot} ni lestvice.")
        return []

    vrstice = [v.find_all("td") for v in tabela.find("tbody").find_all("tr")]

    klubi = []
    for mesto, celice in enumerate(vrstice, start=1):
        zmage = stevilo(celice, ZMAGE)
        remiji = stevilo(celice, REMIJI)

        if vrsta == "skupaj":
            tocke = stevilo(celice, TOCKE)
        else:
            tocke = 3 * zmage + remiji

        klubi.append({
            "sezona": sezona,
            "vrsta": vrsta,
            "mesto": mesto,
            "klub": celice[KLUB].get_text(strip=True),
            "tekme": stevilo(celice, TEKME),
            "zmage": zmage,
            "remiji": remiji,
            "porazi": stevilo(celice, PORAZI),
            "dani_goli": stevilo(celice, DANI),
            "prejeti_goli": stevilo(celice, PREJETI),
            "tocke": tocke,
        })
    return klubi


def izlusci_vse(prvo_leto, zadnje_leto):
    vsi_podatki = []
    for leto in range(prvo_leto, zadnje_leto + 1):
        vrste = VRSTE + VRSTE_PREKINITEV if leto == LETO_PREKINITVE else VRSTE

        for vrsta in vrste:
            pot = os.path.join(MAPA_HTML, f"{leto}_{vrsta}.html")
            if os.path.exists(pot):
                vsi_podatki.extend(izlusci_lestvico(pot, oznaka_sezone(leto), vrsta))
            else:
                print(f"Manjka datoteka {pot}.")
    return vsi_podatki


if __name__ == "__main__":
    df = pd.DataFrame(izlusci_vse(PRVO_LETO, ZADNJE_LETO))
    os.makedirs(os.path.dirname(POT_CSV), exist_ok=True)
    df.to_csv(POT_CSV, index=False)
    print(f"Zapisano: {POT_CSV} ({len(df)} vrstic)")