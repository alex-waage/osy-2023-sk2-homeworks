"""Tento modul obsahuje tzv. Test Targety. Jejich cílem je v tomto pojetí
snaha umožnit strukturovat testy, ale také zaměřit se na testy na úrovni
modulu."""


from typing import Iterable

from fw.plugins.plugin import Plugin
from fw.testing.case import TestResult, TestCase, ModuleImportability
from fw.testing.script import TestScript


class TestTarget:
    """Instance této třídy umožňují sdruživat testovací scénáře a provádět
    testy na úrovni modulu."""

    def __init__(self, plugin: Plugin, test_scripts: Iterable[TestScript]):
        """Initor, který přijímá plugin (obal modulu) a sadu testovacích
        scénářů."""

        # Existence modulu
        ts = TestScript(f"Test použitelnosti modulu {plugin.module_path}")
        ts.add_test_case(ModuleImportability(plugin))

        self._test_scripts = [ts]
        self._test_scripts.extend(list(test_scripts))

    @property
    def test_scripts(self) -> tuple[TestScript]:
        """Sada testovacích scénářů, které mají být provedeny nad daným
        test targetem."""
        return tuple(self._test_scripts)

    def execute(self) -> tuple[tuple[TestResult, TestCase]]:
        """Metoda, která se pokusí provést všechny testovací scénáře, které
        tato instance eviduje. Výstupem je ntice výsledků a testovacích
        případů."""
        all_results = []
        for script in self.test_scripts:

            # Rozšiř dosavadní výsledky o výsledky daného testovacího scénáře
            all_results.extend(script.execute())

        # Vrať výsledky jako ntici
        return tuple(all_results)




