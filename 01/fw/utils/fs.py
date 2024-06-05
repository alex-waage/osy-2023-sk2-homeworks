"""Tento modul sdružuje funkcionalitu pro interakci se souborovým systémem.
"""

import os


def sep() -> str:
    """Funkce vrací separátor instancí v cestě souborového systému.
    Pro Unix-based systémy dopředné lomítko (`/`), pro systémy na bázi Windows
    pak jedno lomítko zpětné (`\\\`).
    """
    return os.path.sep


def join_paths(*paths) -> str:
    """Funkce vrací spojení objektů do jednoho řetězce reprezentující danou
    cestu v souborovém systému.
    """
    return os.path.join(*paths)


def exists(filepath: str) -> bool:
    """Funkce vrací informaci o tom, zda-li je daná cesta platná a existující.
    """
    return os.path.exists(filepath)


def is_directory(filepath: str) -> bool:
    """Funkce vrací informaci o tom, zda-li je na dané cestě adresář.
    """
    if not exists(filepath):
        raise FilePathError(f"Cesta '{filepath}' neexistuje", filepath)
    return os.path.isdir(filepath)


def is_file(filepath: str) -> bool:
    """Funkce vrací informaci o tom, zda-li je na dané cestě soubor.
    """
    if not exists(filepath):
        raise FilePathError(f"Cesta '{filepath}' neexistuje", filepath)
    return os.path.isfile(filepath)


def basename(filepath: str, extension: bool = True) -> str:
    """Funkce vrací název souboru, na který ukazuje dodaná cesta.
    Volitelným parametrem je i možnost zahrnutí koncovky, je-li v případě
    souboru dostupná.

    Funkce dokáže pracovat i s neexistujícím souborem.
    """
    b_name = os.path.basename(filepath)
    return b_name if extension else os.path.splitext(b_name)[0]


def list_files(filepath: str,
               incl_dirs: bool = True,
               deep: bool = False) -> list[str]:
    """Funkce vrací absolutní cesty ke všem potomkům obsaženým ve složce. Pokud
    neukazuje dodaná cesta na adresář, je vyhozena výjimka. Stejně tak pokud
    na dodaná cesta neexistuje.

    Funkce umožňuje obsáhnout či ignorovat adresáře; v závislosti na parametru
    `incl_dirs`.

    Dále funkce umožňuje prohledávání do hloubky (`deep`), tedy budou obsaženy
    i soubory v podadresářích adresáře dodaného v parametru.
    """
    if not exists(filepath):
        raise FilePathError(f"Dodaná cesta '{filepath}' neexisuje", filepath)
    elif not is_directory(filepath):
        raise FilePathError(f"'{filepath}' není adresář", filepath)

    contents = []

    # Pro všechny názvy souborů v daném adresáři
    for file in os.listdir(filepath):
        file = join_paths(filepath, file)
        if is_file(file):
            contents.append(file)
        elif is_directory(file):
            if incl_dirs:
                contents.append(file)
            if deep:
                contents.extend(list_files(file, incl_dirs, deep))
    return contents


def list_directories(filepath: str, deep_search: bool = False) -> list[str]:
    """Funkce sloužící pro vrácení všech adresářů uvnitř dodaného adresáře.
    Cesta musí ukazovat na existující adresář.

    Pokud na zadané cestě není existující adresář, je vyhozena výjimka.
    """
    return list(filter(
        lambda f: is_directory(f),
        list_files(filepath, True, deep_search)))


def list_directories_without_pycache(
        filepath: str, deep_search: bool = False) -> list[str]:
    """Funkce sloužící pro vrácení všech adresářů uvnitř dodaného adresáře.
    Přitom jsou filtrovány adresáře s názvem __pycache__.
    Cesta musí ukazovat na existující adresář.

    Pokud na zadané cestě není existující adresář, je vyhozena výjimka.
    """
    return list(filter(lambda f: basename(f) != "__pycache__",
                       list_directories(filepath, deep_search)))


def list_files_with_extension(filepath: str, ext: str) -> list[str]:
    """Funkce slouží k vrácení seznamu všech souborů, které mají na konci
    danou koncovku.

    Pokud na zadané cestě není existující adresář, je vyhozena výjimka.
    """
    ext = ext if ext and ext[0] == "." else f".{ext}"
    return list(filter(
        lambda f: os.path.splitext(f)[-1] == ext, list_files(filepath, False)))


def contains_file(filepath: str, name: str, ignore_ext: bool = False,
                  deep: bool = False) -> bool:
    """Funkce vrací informaci o tom, zda-li daný adresář obsahuje soubor
    daného názvu. Vrací tak i v případě adresářů.

    Funkce dokáže prohledávat i do hloubky, což lze ovládat parametrem `deep`.

    Funkce dále dokáže ignorovat u souborů koncovky (param. `ignore_ext`).

    Pokud na zadané cestě není existující adresář, je vyhozena výjimka.
    """
    if not is_directory(filepath):
        raise FilePathError(f"'{filepath}' není existující soubor", filepath)

    # Remove extension of given name if ignore_ext
    name = basename(name, False) if ignore_ext else name

    return len(tuple(filter(lambda f: basename(f, not ignore_ext) == name,
                            list_files(filepath, True, deep)))) != 0


def filesize(filepath: str) -> int:
    """Funkce vrací velikost souboru v bytech. Pokud je na dané cestě adresář,
    je vrácen součet velikostí všech vnitřních souborů.

    Pokud není na cestě existující soubor, je vyhozena výjimka.
    """
    if not exists(filepath):
        raise FilePathError(f"Cesta '{filepath}' neexistuje", filepath)
    if is_file(filepath):
        return os.stat(filepath).st_size
    elif is_directory(filepath):
        return sum(map(
            lambda f: filesize(f), list_files(filepath, False, True)))


def count_files(filepath: str, files_only: bool = False,
                deep: bool = False) -> int:
    """Funkce vrací počet souborů v dodaném adresáři. Pokud na zadané cestě
    není existující adresář, vyhazuje výjimku.

    Funkce dokáže vyloučit adresáře (pomocí parametru `files_only`). Funkce
    dále dokáže prohledávat do hloubky (pomocí parametru `deep`)
    """
    return len(list_files(filepath, incl_dirs=not files_only, deep=deep))


def parent_dir(filepath: str) -> str:
    """Funkce vrací absolutní cestu k rodičovskému adresáři. Funkce funguje
    i pro soubory neexistující.
    """
    return os.path.dirname(filepath)


def root_directory_path() -> "str":
    """Funkce vrací absolutní cestu ke kořenové složce projektu.
    """
    return os.path.abspath(os.path.join(__file__, "..", "..", ".."))


def join_path_in_project(relative_path: str) -> str:
    """Funkce spojuje absolutní cestu ke kořeni projektu s relativní cestou
    v rámci tohoto projektu.
    """
    return join_paths(root_directory_path(), relative_path)


def abs_to_relative(abs_path: str, rel_root: str) -> str:
    """Funkce převede absolutní cestu na relativní vůči dodanému bodu.
    Relativní cesta musí být adresářem, který obsahuje absolutní cestou
    odkazovaný objekt. Je-li tedy například absolutní cestou popsán soubor,
    musí dodaná absolutní cesta ukazovat na adresář, který přímo nebo v
    některém ze svých podadresářů daný soubor obsahuje. Funkce pracuje pouze
    s přímými cestami; výhradně vztah 'rodič-potomek', žádní sourozenci.
    Pokud dodaný relativní bod (kořen, od kterého se má dále cesta popisovat)
    není počátkem absolutní cesty, je vyhozena výjimka.

    Jsou rozlišována malá a velká písmena. Počáteční a koncové mezery jsou
    ořezány.
    """
    abs_path = abs_path.strip()
    rel_root = rel_root.strip()

    # Pokud absolutní cesta není podmnožinou relativní cesty
    if not abs_path.startswith(rel_root):
        raise FilePathError(f"Relativní kořenový adresář '{rel_root}' "
                            f"neobsahuje konkrétní absolutní cestu "
                            f"'{abs_path}'")

    return abs_path[len(rel_root) + 1:]


def absolute_to_project_rel(abs_path: str) -> str:
    """Funkce převede absolutní cestu k souborovému objektu na relativní cestu
    vůči kořeni projektu.
    Pokud cesta není (byť hypoteticky; cílový objekt nemusí existovat)
    obsažena v projektu, je vyhozena výjimka.
    """
    return abs_to_relative(abs_path, root_directory_path())


def module_path_from_abs(abs_path: str) -> str:
    """Funkce se pokusí převést absolutní cestu ke zdrojovému souboru na
    absolutní cestu v kontextu balíčků projektu.
    Konkrétně funkce převede absolutní cestu k souboru na relativní vůči
    projektu, nahradí v něm defaultní separátory pohybu v souborovém systému
    (typicky zpětná a dopředná lomítka) na tečky a odstraní koncovku souboru.
    Této funkce lze použít pro dynamické importování modulů z absolutních cest
    prohledaného adresáře uvnitř projektu.
    """
    return basename(
        absolute_to_project_rel(abs_path).replace(sep(), "."), False)


class FilePathError(Exception):
    """Výjimka tohoto typu značí vznik problému při práci se souborovým
    systémem, resp. s cestou v něm.
    """

    def __init__(self, message: str, filepath: str = ""):
        """Initor, který přijímá zprávu o chybě a volitelnou cestu, v jejímž
        kontextu k chybě došlo."""
        super().__init__(message)
        self._filepath = filepath

    @property
    def filepath(self) -> str:
        """Cesta, v jejímž kontextu došlo k chybě. Může být i prázdný řetězec.
        """
        return self._filepath
