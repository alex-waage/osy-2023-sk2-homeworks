"""Tento modul obsauje definici pluginu, který lze použít jako obal modulu
pro potřeby jeho zpětné (reflexivní) analýzy a k dynamickému importu (za běhu
programu a na základě vnitřní logiky programu)."""

import importlib
from inspect import getmembers, isfunction, isclass
from types import ModuleType
from typing import Callable, Type

from fw.utils.fs import exists, is_file, module_path_from_abs


class Plugin:
    """Instance třídy plugin jsou abstrakcí nad dynamicky načtíanými moduly.
    Tyto moduly mohou reprezentovat kód k otestování.
    """

    def __init__(self, filepath: str):
        """Initor třídy, který přijímá absolutní cestu k souboru, který má
        být dynamicky načten.

        Lze vytvořit plugin i neexistujícího či nevalidního modulu.
        """

        self._absolute_path = filepath

        # Převedení absolutní cesty na 'balíčkovou'
        self._module_path = module_path_from_abs(filepath)

    @property
    def absolute_path(self) -> str:
        """Absolutní cesta k souboru, který je dynamicky načítán."""
        return self._absolute_path

    @property
    def module_path(self) -> str:
        """Balíčková cesta k modulu, který reprezentuje daný plugin."""
        return self._module_path

    @property
    def module_name(self) -> str:
        """Funkce vrací samotný název modulu."""
        return self.module.__name__.split(".")[-1]

    @property
    def module(self) -> "ModuleType":
        """Vlastnost se pokusí načíst modul, kterým je plugin reprezentován.
        Pokud se načíst modul nepovede (typicky z důvodu syntaktické chyby),
        je vyhozena výjimka PluginError."""
        try:
            return importlib.import_module(self.module_path)
        except Exception as e:
            raise PluginError(
                f"Při načítání modulu '{self.module_path}' na cestě "
                f"'{self.absolute_path}' došlo k chybě: "
                f"'{type(e).__name__}': '{str(e)}'", self)

    @property
    def all_attributes(self) -> "tuple[tuple[str, object]]":
        """Vlastnost vrací ntici všech atributů, které plugin má.

        Tyto jsou vráceny v ntici ntic, které obsahují:
            [0]: název atributu
            [1]: objekt skrytý v atributu (např. string nebo funkce)
        """
        attrs = dir(self.module)
        return tuple(map(
            lambda key: (str(key), attrs.key,), attrs))

    @property
    def all_classes(self) -> tuple[tuple[str, Type]]:
        """Vlastnost vrací ntici všech tříd, které plugin má."""
        return tuple(getmembers(self.module, isclass))

    @property
    def all_functions(self) -> "tuple[tuple[str, Callable]]":
        """Tato funkce vrátí všechny funkce, kterými je modul pluginu opatřen.
        Vrací je v podobě ntice ntic, přičemž každá vnitřní obsahuje textový
        řetězec reprezentující název funkce a referenci na danou funkci.
        """
        return tuple(getmembers(self.module, isfunction))

    @property
    def all_function_names(self) -> "tuple[str]":
        """Vlastnost vrací ntici utvořenou ze seznamu názvů všech funkcí,
        které jsou v modulu pluginu.
        """
        return tuple(map(lambda funcs: str(funcs[0]), self.all_functions))

    @property
    def all_class_names(self) -> tuple[str]:
        """Vlastnost vrací názvy všech tříd, které jsou v daném modulu
        definovány."""
        return tuple(map(lambda clazz: str(clazz[0]), self.all_classes))

    @property
    def docstring(self) -> str:
        """Vlastnost vrací dokumentační komentář modulu, který reprezentuje
        plugin."""
        return self.module.__doc__

    def has_attribute(self, attr_name: str) -> bool:
        """Funkce vrací informaci o tom, zda-li daný plugin má nebo nemá
        atribut daného názvu.
        """
        return hasattr(self.module, attr_name)

    def has_function(self, fun_name: str) -> bool:
        """Funkce vrací informaci o tom, zda-li daný obsahuje funkci daného
        názvu."""
        for func_desc in self.all_functions:
            if func_desc[0] == fun_name:
                return True
        return False

    def has_class(self, class_name: str) -> bool:
        """Funkce vrací, zda-li je přítomna funkce daného jména či nikoliv."""
        for c in self.all_classes:
            if c[0] == class_name:
                return True
        return False

    def get_attribute(self, attr_name: str) -> object:
        """Funkce vrací atribut (resp. jeho hodnotu), kterým je daný modul
        opatřen. Pokud daný atribut nemá, je vyhozena výjimka.
        """
        if self.has_attribute(attr_name):
            return self.module.__getattribute__(attr_name)
        else:
            raise PluginError(f"Plugin atribut '{attr_name}' nemá", self)

    def get_function(self, fun_name: str) -> Callable:
        """Tato funkce se pokusí vyhledat funkci daného názvu uvnitř modulu
        pluginu.

        Pokud není taková funkce nalezena, je vyhozena příslušná výjimka.
        """
        for fun_description in self.all_functions:
            if fun_description[0] == fun_name:
                return fun_description[1]
        raise PluginError(
            f"Funkce názvu '{fun_name}' nebyla nalezena", self)

    @staticmethod
    def can_be_imported(filepath: str) -> bool:
        """Statická funkce, která dokáže zjistit, zda-li je modul uvnitř
        tohoto projektu na zadané absolutní cestě validním pluginem. Tato
        funkce je prvotním rozlišovacím indikátorem nepoužitelného pluginu.

        Samotné ověření je provedeno na základě:

            - existence souboru na zadané cestě
            - že je daný soubor uvnitř projektu
            - že je možné daný soubor (modul) dynamicky naimportovat
        """
        try:
            if exists(filepath) and is_file(filepath):
                module_path = module_path_from_abs(filepath)
                importlib.import_module(module_path)
                return True
        except:
            return False
        else:
            return False


class PluginError(Exception):
    """Třída PluginError definuje výjimky, které jsou vyhazovány, dojde-li
    k chybě v kontextu pluginu."""

    def __init__(self, message: str, plugin: Plugin = None):
        Exception.__init__(self, message)
        self._plugin = plugin

    @property
    def plugin(self) -> Plugin:
        """Plugin, v jehož kontextu došlo k chybě."""
        return self._plugin
