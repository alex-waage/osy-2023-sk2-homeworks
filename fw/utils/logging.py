from fw.testing.case import TestResult

_BEAUTIFY = True

_COLOURS = {
    "RED": '\033[91m',
    "GREEN": '\033[92m',
    "BLUE": '\033[94m',
    "CYAN": '\033[96m',
    "YELLOW": '\033[93m',
    "MAGENTA": '\033[95m',
    "GREY": '\33[90m',
    "BOLD": '\033[1m',
    "ENDC": '\033[0m',
    "UNDERLINE": '\033[4m',
    "ITALIC": '\33[3m'
}


def green_text(text: str) -> str:
    """Vrací vstupní text s úvodní a koncovou sekvencí pro obarvení zelenou
    barvou."""
    return f"{_COLOURS['GREEN']}{text}{_COLOURS['ENDC']}"


def red_text(text: str) -> str:
    """Vrací vstupní text s úvodní a koncovou sekvencí pro obarvení červenou
    barvou."""
    return f"{_COLOURS['RED']}{text}{_COLOURS['ENDC']}"


def yellow_text(text: str) -> str:
    """Vrací vstupní text s úvodní a koncovou sekvencí pro obarvení žlutou
    barvou."""
    return f"{_COLOURS['YELLOW']}{text}{_COLOURS['ENDC']}"


def blue_text(text: str) -> str:
    """Vrací vstupní text s úvodní a koncovou sekvencí pro obarvení modrou
    barvou."""
    return f"{_COLOURS['BLUE']}{text}{_COLOURS['ENDC']}"


def cyan_text(text: str) -> str:
    """Vrací vstupní text s úvodní a koncovou sekvencí pro obarvení tyrkysovou
    barvou."""
    return f"{_COLOURS['CYAN']}{text}{_COLOURS['ENDC']}"


def magenta_text(text: str) -> str:
    """Vrací vstupní text s úvodní a koncovou sekvencí pro obarvení tyrkysovou
    barvou."""
    return f"{_COLOURS['MAGENTA']}{text}{_COLOURS['ENDC']}"


def grey_text(text: str) -> str:
    """Vrací vstupní text s úvodní a koncovou sekvencí pro obarvení šedou
    barvou."""
    return f"{_COLOURS['GREY']}{text}{_COLOURS['ENDC']}"


def bold_text(text: str) -> str:
    """Vrací vstupní text s úvodní a koncovou sekvencí pro ztučnění písma."""
    return f"{_COLOURS['BOLD']}{text}{_COLOURS['ENDC']}"


def underline_text(text: str) -> str:
    """Vrací vstupní text s úvodní a koncovou sekvencí pro podtržení písma."""
    return f"{_COLOURS['UNDERLINE']}{text}{_COLOURS['ENDC']}"


def italic_text(text: str) -> str:
    """Vrací vstupní text s úvodní a koncovou sekvencí pro zkosení písma."""
    return f"{_COLOURS['ITALIC']}{text}{_COLOURS['ENDC']}"


def error_text(text: str) -> str:
    """Vrací vstupní text zformátovaný jako chybové hlášení."""
    return red_text(bold_text(text))


def warning_text(text: str) -> str:
    """Vrací vstupní text zformátovaný jako upozornění."""
    return yellow_text(underline_text(text))


def secondary_text(text: str) -> str:
    """Vrací vstupní text zformátovaný jako druhořadé sdělení."""
    return grey_text(text)


def success_text(text: str) -> str:
    """Vrací vstupní text zformátovaný jako sdělení o úspěchu."""
    return green_text(text)


def resolve_info(info_text: str) -> str:
    """Funkce přeformuluje dané informativní sdělení do zvýrazněné podoby
    (je-li povolena)."""
    if _BEAUTIFY:
        return bold_text(warning_text(info_text))
    else:
        return info_text


def resolve_test_result(result: TestResult, name: str, desc: str) -> str:
    """Funkce přeformuluje daný výraz se zvýrazněním. Pokud je nastaveno
    zvýraznění jako True, pak úspěšné testy jsou označeny zeleně, neprovedené
    šedě a neúspěšné červeně."""

    # Základní text bez zvýraznění a popisu
    string = f"[{str(result).split('.')[1]}]: {name:33} "

    # Pokud zvýraznit, pak popis je italikou, jinak bez italiky
    string = f"{string}{italic_text(desc)}" if _BEAUTIFY else f"{string}{desc}"

    # Pokud nezvýrazňovat, pak
    if not _BEAUTIFY:
        return string

    # Jinak
    elif result == TestResult.SUCCESS:
        return success_text(string)
    elif result == TestResult.NOT_TST:
        return secondary_text(string)
    elif result == TestResult.FAILURE:
        return error_text(string)


def beautify(beautify: bool):
    """Přístupová funkce, která globálně povoluje nebo zakazuje zvýraznění
    textu. Pokud je stanovena hodnota True, pak text zvyrazněn dle vnitřních
    pravidel bude."""
    global _BEAUTIFY
    _BEAUTIFY = beautify
