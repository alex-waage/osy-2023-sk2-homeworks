"""Modul má za cíl ověřit schopnosti řešení jednoduchých problémů z domény
práce s kolekcemi."""


def get_length(lst: list) -> int:
    """Funkce vrací celé číslo reprezentující délku dodaného seznamu."""
    return len(lst)

def has_item(item: str, lst: list[str]) -> bool:
    """Funkce vrací, zda-li dodaný seznam textových řetězců obsahuje téže
    dodaný textový řetězec. Tuto hodnotu vrací jako hodnotu `bool`.
    """
    return item in lst

def add_if_not_in(item: str, lst: list[str]) -> list[str]:
    """Funkce zjišťuje, zda-li není v daném seznamu textový řetězec, který
    chce přidat. Pokud není, přidá ho. V každém případě tento seznam vrací.
    """
    if item not in lst:
        lst.append(item)
    return lst

def get_last_item(lst: list[str]) -> str:
    """Funkce vrací poslední položku v dodaném seznamu."""
    return lst[-1] if lst else ''

def all_but_last(lst: list) -> list:
    """Funkce vrací celý dodaný seznam bez posledního prvku."""
    return lst[:-1]

def concat_lists(lst1: list, lst2: list) -> list:
    """Funkce spojuje dva dodané seznamy do jednoho. Ten pak vrací."""
    return lst1 + lst2

def to_tuple(lst: list) -> tuple:
    """Funkce vrací dodaný seznam převedený na ntici."""
    return tuple(lst)

def in_between(start: int, end: int) -> list[int]:
    """Funkce má za cíl vytvořit seznam číslic v rozmezí `start` a `end`
    (včetně)."""
    return list(range(start, end + 1))

def evens_in_between(start: int, end: int) -> list[int]:
    """Funkce má za cíl vytvořit seznam výhradně sudých číslic v rozmezí
    `start` a `end` (včetně)."""
    return [x for x in range(start, end + 1) if x % 2 == 0]

def count_uniques_only(lst: list) -> int:
    """Funkce má za cíl spočítat všechny unikátní hodnoty a tento počet
    vrátit.

    Nápověda: Lze řešit jednoduše for cyklem a ukládáním unikátních hodnot, ale
    lze použít i elegantnější řešení - podívejte se na množiny (kolekce typu
    `set`)."""
    return len(set(lst))

def split_into_words(sentence: str) -> tuple[str]:
    """Funkce má za cíl rozdělit dodanou větu na ntici samostatných slov.
    Parametrem funkce je tedy textový řetězec obsahující slova oddělená
    mezerami. Očekávaným výstupem je ntice.

    Nápověda: Python umožňuje použití metody `split(separator: str)`, která
    dokáže textový řetězec rozdělit. Způsob použití je následující:

    >>> "To be split".split(" ")
    ['To', 'be', 'split']
    """
    return tuple(sentence.split())

def split_and_capitalize(sentence: str) -> tuple[str]:
    """Funkce má za cíl rozdělit dodanou větu na ntici samostatných slov,
    která dále převede na velká písmena.

    Parametrem funkce je tedy textový řetězec obsahující slova oddělená
    mezerami. Očekávaným výstupem je ntice slov napsaných velkými písmeny.

    Nápověda: Python umožňuje použití metody `split(separator: str)`, která
    dokáže textový řetězec rozdělit. Způsob použití je následující:

    >>> "To be split".split(" ")
    ['To', 'be', 'split']
    """
    words = sentence.split()
    capitalized_words = [word.upper() for word in words]
    return tuple(capitalized_words)

def count_unique_words(sentence: str) -> int:
    """Funkce má za cíl spočítat počet unikátních slov v dodané větě. Funkce
    nerozlišuje velikost písmen (textové řetězce "x" a "X" musí být chápány
    jako zaměnitelné - neunikátní).

    Nápověda 1: Python umožňuje použití metody `split(separator: str)`, která
    dokáže textový řetězec rozdělit. Způsob použití je následující:

    >>> "To be split".split(" ")
    ['To', 'be', 'split']

    --------------------------------------------------------------------------

    Nápověda 2: Lze řešit jednoduše for cyklem a ukládáním unikátních hodnot,
    ale lze použít i elegantnější řešení - podívejte se na množiny (kolekce
    typu `set`).

    --------------------------------------------------------------------------

    Nápověda 3: Je nám jedno, jestli budeme upravovat velikost písmen celého
    řetězce, nebo pak až každé slovo zvlášť. Ale pozor, seznam sám o sobě
    příslušné dvě metody nemá, na něm je tedy nezavoláte.
    """
    words = sentence.lower().split()
    return len(set(words))
