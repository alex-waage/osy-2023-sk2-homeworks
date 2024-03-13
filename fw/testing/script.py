"""Tento modul obsahuje definici testovacích scénářů, které lze použít pro
testování jednotlivých elementů v rámci testovaného modulu."""

import inspect
from typing import Iterable, Type

from fw.plugins.plugin import Plugin
from fw.testing.case import TestCase, FunctionExistenceTest, \
    FunctionDocstringTest, FunctionReturnValueTest, FunctionParameterTest, \
    TestResult, FunctionSignatureTest, FunctionSignatureReturnType
from fw.testing.comparison import Comparator, ExactComparator


class TestScript:
    """Obecný testovací scénář, který má za cíl poskytovat základní služby
    sdružení testovacích případů."""

    def __init__(self, name: str):
        """Initor, který přijímá název testovacího scénáře."""
        self._test_cases: list[TestCase] = []
        self._test_script_name = name

    @property
    def test_cases(self) -> tuple[TestCase]:
        """Všechny evidované testovací případy"""
        return tuple(self._test_cases)

    @property
    def test_script_name(self) -> str:
        """Název testovacího scénáře"""
        return self._test_script_name

    def add_test_case(self, new_test_case: TestCase):
        """Funkce přidává dodaný testovací případ do seznamu evidovaných
        testovacích případů."""
        self._test_cases.append(new_test_case)

    def add_all_test_cases(self, tcs: Iterable[TestCase]):
        """Funkce přidává dodané testovací případy, o které již evidované
        rozšíří."""
        self._test_cases.extend(tcs)

    def execute(self) -> tuple[tuple[TestResult, TestCase]]:
        """Funkce, která poskytuje vyhodnocení testovacích případů a vrátí
        ntici dvojic výsledku a testovacícho případu."""
        return tuple([(tc.execute_test(), tc) for tc in self.test_cases])


class ModuleLevelFunctionTestScript(TestScript):
    """Testovací scénář, který se specializuje na testování funkcí."""

    def __init__(
            self,
            plugin: Plugin,
            function_name: str,
            function_purpose: str,
            param_defs: Iterable[tuple[str, Type, object]],
            bb_defs: Iterable[tuple[object, tuple[object]]],
            declared_return_type: Type = inspect._empty,
            comp: Comparator = ExactComparator()):
        """Initor, který přijímá referenci na plugin (obal modulu), název
        testované funkce (kterou si dále testovací případy dohledají),
        definici parametrů funkce (pro každý parametr se očekává jeho název,
        deklarovaný typ a případnou výchozí hodnotu), a testovací data pro
        black-box testování. Každá sada má podobu (return_val, (p1, p2, ...,))
        """

        # Iniciace předka
        TestScript.__init__(self, f"Testy funkce '{function_name}' "
                                  f"v modulu {plugin.module_path} "
                                  f"({function_purpose})")

        # Formální kontrola
        self.add_all_test_cases([
            FunctionExistenceTest(plugin, function_name),
            FunctionDocstringTest(plugin, function_name)
        ])

        # Kontrola pořadí a počtu vstupních parametrů
        self.add_test_case(FunctionSignatureTest(
            plugin, function_name, tuple(map(lambda p: p[0], param_defs))
        ))

        # Kontrola vstupních parametrů
        for parameter_definition in param_defs:
            self.add_test_case(
                FunctionParameterTest(
                    plugin, function_name, *parameter_definition))

        # Kontrola deklarace typu návratové funkce
        self.add_test_case(FunctionSignatureReturnType(
            plugin, function_name, declared_return_type))

        # Definice black-box test hodnot
        for bb_def in bb_defs:
            self.add_test_case(
                FunctionReturnValueTest(plugin, function_name, *bb_def, comp))
