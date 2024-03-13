import math

"""Modul má za cíl ověřit schopnosti řešení jednoduchých problémů z domény
práce s čísly."""


def addition(a: float, b: float) -> float:
    """Funkce pro sčítání dvou reálných čísel.
    Funkce přijímá dva parametry - `a` a `b`. Oba přjímají reálné číslo.
    """
    return a + b

def multiplication(a: float, b: float) -> float:
    """Funkce pro násobení dvou reálných čísel.
    Funkce přijímá dva parametry - `a` a `b`. Oba přjímají reálné číslo.
    """
    return a * b

def division(dividend: float, divisor: float) -> float:
    """Funkce pro dělení dvou reálných čísel.
    Funkce přijímá dva parametry - `dividend` (dělenec) a `divisor` (dělitel).
    Oba přjímají reálné číslo.
    """
    return dividend / divisor

def equality(a: int, b: int) -> bool:
    """Funkce poskytuje službu porovnávání čísel co do rovnosti.
    Vrací True tehdy, a jen tehdy, je-li `a` stejná hodnota, jako `b`.
    V opačném případě vrací hodnotu False."""
    return a == b

def inequality_ne(a: int, b: int) -> bool:
    """Funkce poskytuje službu porovnávání čísel co do nerovnosti.
    Vrací True tehdy, a jen tehdy, je-li `a` jiné, než `b`. V opačném případě
    vrací hodnotu False."""
    return a != b

def inequality_gt(a: int, b: int) -> bool:
    """Funkce poskytuje službu porovnávání čísel co do velikosti.
    Vrací True tehdy, a jen tehdy, je-li `a` větší než `b`. V opačném případě
    vrací hodnotu False."""
    return a > b

def is_divisible(number: int, divisor: int) -> bool:
    """Funkce vrací, zda-li je dané číslo `number` celočíselně bezezbytku
    dělitelné daným dělitelem (`divisor`). Tuto informaci vrací jako boolean
    hodnotu.
    """
    return number % divisor == 0

def power(base: float, exp: float = 2.0) -> float:
    """Funkce vrací mocninu základu na dodaný exponent. Exponent je volitelný,
    není-li dodán, jeho výchozí hodnotou je 2.

    Oba parametry (`base` i `exp`) jsou typu `float`, funkce vrací také
    `float`."""
    return base ** exp

def pythagoras(a: float, b: float) -> float:
    """Funkce vypočítává délku přepony pravoúhlého trojúhelníku.
    Předpokladem funkce je, že vstupní hodnoty odpovídají sestrojitelnému
    pravoúhlému trojúhelníku.

    Vstupní parametry (`a` i `b`), stejně jako návratová hodnota jsou typu
    float."""
    return (a ** 2 + b ** 2) ** 0.5

def circumference(radius: float) -> float:
    """Funkce vypočítává obvod kružnice z dodaného poloměru.
    Funkce předpokládá, že dodaný poloměr je nezáporné číslo, tudíž není
    třeba takovou kontrolu implementovat.

    Doporučení:
    -----------
    K získání vyšší přesnosti při výpočtu použijte číslo pí (π) z interní
    implementace Pythonu. Očekává se použití z knihovny `math`, kterou si
    ale je třeba nejdříve naimportovat, to provedete pomocí příkazu
    `import math`, který můžete zahrnout buďto do těla funkce, nebo (lépe)
    na začátek tohoto modulu.
    """
    return 2 * math.pi * radius