import os
import time

import requests

OSNOVNI_URL = "https://www.11v11.com/league-tables/premier-league"


def shrani_strani(prvo_leto, zadnje_leto):
    """
    Za vsako sezono prenese tri lestvice s strani 11v11.com (skupno, doma in
    v gosteh), za sezono 2019/20 pa še lestvici doma in v gosteh na dan
    prekinitve zaradi covida-19 (13. 3. 2020). Strani shrani v mapo html_strani.
    Leto pomeni konec sezone: 1993 je sezona 1992/93.
    """
    mapa = "html_strani"
    if not os.path.exists(mapa):
        os.makedirs(mapa)
        print(f"Ustvaril sem mapo: {mapa}")

    strani = []
    for leto in range(prvo_leto, zadnje_leto + 1):
        strani.append((f"{leto}_skupaj", f"{OSNOVNI_URL}/{leto}/"))
        strani.append((f"{leto}_doma", f"{OSNOVNI_URL}/{leto}/home/"))
        strani.append((f"{leto}_v_gosteh", f"{OSNOVNI_URL}/{leto}/away/"))
    strani.append(("2020_doma_do_prekinitve", f"{OSNOVNI_URL}/13-march-2020/home/"))
    strani.append(("2020_v_gosteh_do_prekinitve", f"{OSNOVNI_URL}/13-march-2020/away/"))

    for ime, url in strani:
        pot_do_datoteke = os.path.join(mapa, f"{ime}.html")

        if os.path.exists(pot_do_datoteke):
            print(f"Stran {ime} že obstaja. Preskakujem...")
            continue

        print(f"Prenašam {ime}...")
        odgovor = requests.get(url, timeout=30)

        if odgovor.status_code == 200 and 'id="table-league"' in odgovor.text:
            with open(pot_do_datoteke, "w", encoding="utf-8") as f:
                f.write(odgovor.text)
            print(f"Shranjeno: {pot_do_datoteke}")
        else:
            print(f"Napaka pri prenosu {ime}. Koda napake: {odgovor.status_code}")
        time.sleep(3)


if __name__ == "__main__":
    print("Začenjam prenos...")
    shrani_strani(1993, 2026)
    print("Konec prenosa!")