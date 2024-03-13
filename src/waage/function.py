"""Tento modul má za cíl ověřit schopnost navrhnout složitější funkci, 
která řeší zadaný praktičtější problém."""


def is_prime_number(number: int) -> bool:
    """Funkce vrací, zda-li je dodané číslo prvočíslem či nikoliv.

    Nápověda 1: Každé číslo je celočíselně dělitelné samo sebou a jedničkou.
    Prvočísla mají tu zvláštnost, že nejsou dělitelná ničím jiným.

    Proto když hledáme, zda není číslo prvočíslem, kontrolujeme, zda-li není
    dělitelné některým číslem, které je menší, než toto potenciální prvočíslo.
    Pokud ano, o prvočíslo nejde. Pokud takové číslo nenajdeme, číslo je
    prvočíslem.

    --------------------------------------------------------------------------

    Nápověda 2: Pro zjištění, zda-li je číslo `potential_prime` dělitelné
    číslem `divisor`, zajímá nás, zda-li není zbytek po celočíselném dělení
    (tzv. modulo) rovno nule. Pokud ano, dělitelné tímto číslem je bezezbytku,
    v opačném případě nikoliv. Dáváme pochopitelně pozor na to, aby dělitel
    nebyl roven nule. Podobně nám toho tolik neřekne, bude-li naším sledovaným
    dělitelem 1.
    """
    for divisor in range(2, int(number**0.5) + 1):
        if number % divisor == 0:
            return False  # Našli jsme dělitel, číslo není prvočíslo
    return True  # Nenašli jsme žádný dělitel, číslo je prvočíslo