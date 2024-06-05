# Splňování podmínek - rozvrh hodin
Tato úloha se zabývá implementací problému automatického vytváření rozvrhu.

## Spuštění úlohy

Pro spuštění úlohy je nejdříve nutné nainstalovat požadované knihovny, to se provede za spuštění následujícího příkazu (předpokládá se však již nainstalovaný správce balíčků pip).

```shell
pip install -r requirements.txt
```

Následně je možné spustit program "*tvorba-rozvrhu.py*". Program interaktivně nabídně výběr parametrického souboru (popis, viz. níže) a vygeneruje rozvrh dle následujících parametrů:
* třída nemůže být na více místech najednou
* učitel nemůže být na více místech najednou
* v učebně nemůže probíhat více, než jedna výuka najednou
* výuka probíhá vždy za přítomnosti jedné třídy a jednoho učitele v jedné učebně
* každá třída má omezenou dobu výuky (tj. po-pá, 8:00 - 17:00)
* každý den má každá třída alespoň 4 hodiny
* každá třída má hodiny přesně od 8:00 do 12:00, pak již volitelně

Rozvrh se následně vygeneruje do adresáře "*output*" ve formě PDF (PDF část programu jsem vytvořil za pomocí ChatGPT).

## Parametrický .json soubor

Pro využití programu je nutné nadefinovat podmínky a prostředí pro které rozvrh vytváříme. Musím říct, že mě nenapadla lepší forma, než využít strukturovaného .json souboru (viz. následující popis).

* při vytváření .json souboru je nutné definovat třídu s předměty a jejich časovými dotacemi
```
{
  "classes": [
    {
      "name": "1A", # zde definujeme název třídy
      "subjects": [
        {"name": "CZE", "hours": 5}, # název předmětů, týdenní časová dotace
        {"name": "MAT", "hours": 4},
        {"name": "ANG", "hours": 3},
        {"name": "DEJ", "hours": 2},
        {"name": "ZEM", "hours": 2},
        {"name": "BIO", "hours": 2},
        {"name": "CHE", "hours": 2},
        {"name": "FYZ", "hours": 2},
        {"name": "TV", "hours": 2},
        {"name": "INF", "hours": 1}
      ]
    }
  ] 
}
```

* dále je nutné definovat místnosti, které máme (**!typ učebny musí být přesně dle typu níže**)
```
{
    "rooms": [
    {"name": "PC1", "type": "PC"}, # název účebny a typ učebny
    {"name": "PC2", "type": "PC"},
    {"name": "T1", "type": "kmenová"},
    {"name": "T2", "type": "kmenová"},
    {"name": "T3", "type": "kmenová"},
    {"name": "T4", "type": "kmenová"},
    {"name": "JAZ1", "type": "jazyková"},
    {"name": "JAZ2", "type": "jazyková"},
    {"name": "TV1", "type": "tělocvična"},
    {"name": "TV2", "type": "tělocvična"},
    {"name": "DIL2", "type": "dílna"}
  ],
}
```

* definice učitelů a jejich předmětů
```
{
  "teachers": [
    {"name": "Novak", "subjects": ["MAT"]},
    {"name": "Otrubova", "subjects": ["MAT", "BIO"]},
    {"name": "Svobodova", "subjects": ["CZE"]},
    {"name": "Liptakova", "subjects": ["CZE"]},
    {"name": "Smith", "subjects": ["ANG"]},
    {"name": "Kral", "subjects": ["ANG"]},
    {"name": "Vacek", "subjects": ["DEJ", "ZEM"]},
  ]
}
```

Následně stačí .json soubor uložit do adresáře "*input*", následně bude k vybrání v interaktivním výběru programu.

## Testování

Pro testování jsem měl omezený čas, zkusil jsem různé kombinace a vychytal jsem alespoň největší mouchy, avšak v případě narazení na problém se může jednat o následující chyby:
* Nedostatek učitelů pro předměty
* Nedostatek místností pro předměty
* další chybové stavy jsem již bohužel nestihl pokrýt, avšak v jejich případě by se měla objevit generická chybová hláška