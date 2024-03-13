"""Tento modul obsahuje definici třídy PluginLoader, jejíž instance se starají
o vyhotovení instance třídy Plugin, jež slouží pro potřeby dynamického načítání
a reflexivní analýzy modulu."""

from fw.plugins.plugin import Plugin
from fw.utils.fs import exists, is_directory, list_files, basename, join_paths


class PluginLoader:
    """Instance této třídy slouží jako továrny pro instance třídy Plugin."""

    def __init__(self, destination: str, plugin_name: str):
        """Initor, který přijímá adresář, ve kterém by se kýžený plugin měl
        nacházet, a název daného pluginu. Předpokládá se název i s koncovkou.
        """
        self._destination = destination
        self._name = plugin_name

        if not exists(destination):
            raise Exception(f"Dodaná cesta '{destination}' neexistuje!")
        elif not is_directory(destination):
            raise Exception(f"Na dodané cestě '{destination}' není adresář")

    @property
    def destination(self) -> str:
        """Absolutní cesta k adresáři, ve kterém by měl být plugin daného
        názvu."""
        return self._destination

    @property
    def plugin_name(self) -> str:
        return self._name

    @property
    def plugin_name(self) -> str:
        """Název pluginu, který má být hledán."""
        return self._name

    @property
    def has_plugin(self) -> bool:
        """Informace o tom, zda-li dodaný adresář obsahuje hledaný plugin."""
        return (self.plugin_name in [basename(file, True)
                for file in list_files(self.destination, False, True)])

    @property
    def plugin(self) -> Plugin:
        """Načtený plugin z dodané cesty."""
        return Plugin(join_paths(self.destination, self.plugin_name))



