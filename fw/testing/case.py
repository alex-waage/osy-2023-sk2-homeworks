"""V tomto modulu je uvedena definice testovacích případů, které ověřují
jeden konkrétní aspekt nedělitelného elementu.
"""

import inspect
from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Iterable, Type

from fw.plugins.plugin import Plugin
from fw.testing.comparison import Comparator, ExactComparator


class TestResult(Enum):
    """Tento výčtový typ reprezentuje možné výsledky testů.

    - SUCCESS značí úspěšné splnění testu
    - FAILURE značí neúspěšné splnění testu
    - NOT_TST značí, že test nebyl proveden (nesplněné předpoklady)
    """
    SUCCESS, FAILURE, NOT_TST = range(3)


def importability_check(function: Callable) -> Callable:
    """Vrací True, je-li možné ho importovat. Jinak False.

    Typickými důvody, proč nelze modul importovat, jsou syntaktické
    chyby nebo neošetřené výjímky při načítání modulu."""
    def wrapper(*args) -> TestResult:
        self = args[0]
        if self.plugin.can_be_imported(self.plugin.absolute_path):
            return function(self)
        return TestResult.NOT_TST
    return wrapper


class TestCase(ABC):
    """Instance této abstraktní třídy deklarují, že mají obecné prostředky
    pro provedení automatizovaného testovacího případu.

    Každý taková Test Case musí mít název, popis a schopnost být proveden.
    """

    def __init__(self, name: str, description: str, plugin: Plugin):
        """"""
        self._name = name
        self._description = description
        self._plugin = plugin

    @property
    def name(self) -> str:
        """Člověku čitelný název testu."""
        return self._name

    @property
    def description(self) -> str:
        """Člověku čitelný popis testu."""
        return self._description

    @property
    def plugin(self) -> Plugin:
        """Plugin, který je testován."""
        return self._plugin

    @importability_check
    @abstractmethod
    def execute_test(self) -> TestResult:
        """Metoda, která se pokusí test spustit."""


class ModuleImportability(TestCase):
    """Tato třída definuje, zda-li daný modul existuje."""

    def __init__(self, plugin: Plugin):
        """"""
        super().__init__(
            name=f"KONTROLA, ŽE LZE MODUL NAČÍST", plugin=plugin,
            description=f"Test, že modul {plugin.module_path} lze načíst. "
                        f"To znamená, že modul existuje a že při načítání "
                        f"nevyhazuje výjimky (např. SyntaxError).")

    def execute_test(self) -> TestResult:
        """Test, který dostane-li se až sem, automaticky projde."""
        if self.plugin.can_be_imported(self.plugin.absolute_path):
            return TestResult.SUCCESS
        return TestResult.FAILURE


class ModuleLevelFunctionTest(TestCase, ABC):
    """Abstraktní testovací případ, který sdružuje prostředky pro testování
    funkcí na úrovni modulu."""

    def __init__(self, name: str, description: str,
                 plugin: Plugin, function_name: str):
        super().__init__(name, description, plugin)
        self._function_name = function_name

    @property
    def function_name(self) -> str:
        """Název funkce, která má být otestována."""
        return self._function_name

    @property
    def has_function(self) -> bool:
        """Jestli má či nemá plugin funkci daného názvu."""
        return self.plugin.has_function(self.function_name)

    @property
    def function(self) -> Callable:
        """Funkce, která se má ověřovat."""
        return self.plugin.get_function(self.function_name)


class FunctionExistenceTest(ModuleLevelFunctionTest):
    """Testovací případ, kdy se ověřuje, že dodaný plugin obsahuje"""

    def __init__(self, plugin: Plugin, function_name: str):
        super().__init__(
            f"PLUGIN OBSAHUJE FUNKCI",
            f"Test, že plugin '{plugin.module_path}' obsahuje funkci "
            f"'{function_name}'", plugin, function_name)

    @importability_check
    def execute_test(self) -> TestResult:
        """Metoda se pokusí zjistit, zda má daný plugin funkci daného názvu."""
        try:
            if self.plugin.has_function(self.function_name):
                return TestResult.SUCCESS
            return TestResult.FAILURE
        except:
            return TestResult.NOT_TST


class FunctionDocstringTest(ModuleLevelFunctionTest):
    """Testovací případ, který ověřuje, že daná funkce má dokumentační
    komentář."""

    def __init__(self, plugin: Plugin, function_name: str):
        super().__init__(
            f"FUNKCE MÁ DOKUMENTAČNÍ KOMENTÁŘ",
            f"Test, že funkce '{function_name}' obsahuje "
            f"dokumentační komentář", plugin, function_name)

    @importability_check
    def execute_test(self) -> TestResult:
        """Test, který ověřuje, že funkce obsahuje dokumentačná komentář.

        Pokud daná funkce není platná, je vráceno NOT_TST, pokud má docstring
        složený z neprázdných znaků o délce větší, než 0, pak SUCCESS. Jinak
        vrací FAILURE.
        """
        try:
            if not self.function.__doc__:
                return TestResult.FAILURE
            elif not len(self.function.__doc__.strip()):
                return TestResult.FAILURE
            else:
                return TestResult.SUCCESS
        except:
            return TestResult.NOT_TST


class FunctionReturnValueTest(ModuleLevelFunctionTest):
    """Testovací případ, který ověřuje, že funkce funguje správně."""

    def __init__(self, plugin: Plugin, function_name: str, expected: object,
                 params: Iterable[object] = (),
                 comp: Comparator = ExactComparator()):
        super().__init__(
            f"SPRÁVNÁ NÁVRATOVÁ HODNOTA FUNKCE",
            f"Test, že funkce '{function_name}' po zavolání s parametry "
            f"{params} vrací hodnotu '{expected}'.",
            plugin, function_name)

        self._expected = expected
        self._params = params
        self._comp = comp

    @property
    def expected_value(self) -> object:
        return self._expected

    @property
    def params(self) -> tuple[object]:
        return tuple(self._params)

    @property
    def comparator(self) -> Comparator:
        return self._comp

    @importability_check
    def execute_test(self) -> TestResult:
        """Funkce ověřuje, že jsou očekávaná a skutečná návratová hodnota
        dodané funkce srovnatelné."""
        try:
            if not self.has_function:
                return TestResult.NOT_TST
            elif self.comparator.compare(
                    self.function(*self._params), self._expected):
                return TestResult.SUCCESS
            return TestResult.FAILURE
        except:
            return TestResult.FAILURE


class FunctionSignatureReturnType(ModuleLevelFunctionTest):
    """Test kontrolující, že má funkce na úrovni modulu v rámci signatury
    správnou návratovou hodnotu."""

    def __init__(self, plugin: Plugin, function_name: str, return_type: Type):
        super().__init__(
            f"KONTROLA TYPU NÁVRATOVÉ HODNOTY",
            f"Kontrola, že funkce '{function_name}' má v rámci signatury "
            f"deklarovánu návratovou hodnotu '{return_type.__name__}'.",
            plugin, function_name)
        self._return_type = return_type

    @property
    def return_type(self) -> Type:
        """Očekávaný typ návratové hodnoty v signatuře funkce"""
        return self._return_type

    @importability_check
    def execute_test(self) -> TestResult:
        """Test kontroluje, že pořadí a počet vstupních parametrů funkce
        odpovídá očekávání."""
        try:
            # Pokud funkce neexistuje
            if not self.has_function:
                return TestResult.NOT_TST

            # Připravení skutečné anotace návratové hodnoty
            return_an = inspect.signature(self.function).return_annotation

            if return_an.__name__ == self.return_type.__name__:
                return TestResult.SUCCESS

            return TestResult.FAILURE
        except:
            return TestResult.NOT_TST


class FunctionSignatureTest(ModuleLevelFunctionTest):
    """Test kontrolující, že má funkce na úrovni modulu správnou podobu
    signatury."""

    def __init__(self, plugin: Plugin, function_name: str,
                 parameter_names: Iterable[str]):
        super().__init__(
            f"KONTROLA SIGNATURY FUNKCE",
            f"Kontrola, že funkce '{function_name}' má správný počet "
            f"parametrů v očekávaném pořadí {tuple(parameter_names)}.",
            plugin, function_name)
        self._parameter_names = tuple(parameter_names)

    @property
    def parameter_names(self) -> tuple[str]:
        """Očekávané názvy parametrů"""
        return self._parameter_names

    @importability_check
    def execute_test(self) -> TestResult:
        """Test kontroluje, že pořadí a počet vstupních parametrů funkce
        odpovídá očekávání."""
        try:
            # Pokud funkce neexistuje
            if not self.has_function:
                return TestResult.NOT_TST

            # Připravení signatury funkce
            signature = inspect.signature(self.function)

            # Pokud se pořadí či počet parametrů shoduje s očekáváním
            if tuple(signature.parameters.keys()) == self.parameter_names:
                return TestResult.SUCCESS

            # Jinak
            else:
                return TestResult.FAILURE
        except:
            return TestResult.NOT_TST


class FunctionParameterTest(ModuleLevelFunctionTest):
    """Test kontrolující, že daná funkce na úrovni modulu obsahuje
    parametr daného názvu a je k němu přiřazen očekávaný typ. Dále umožňuje
    testovat výchozí hodnotu.
    """

    def __init__(self, plugin: Plugin,
                 function_name: str, parameter_name: str, expected_type: Type,
                 default_value: object = None):
        super().__init__(
            f"KONTROLA PARAMETRU FUNKCE",
            f"Kontrola, že funkce '{function_name}' má parametr "
            f"'{parameter_name}', který očekáva typ vstupní hodnoty "
            f"'{expected_type.__name__}' a s výchozí hodnotou "
            f"'{default_value}'", plugin, function_name)
        self._parameter_name = parameter_name
        self._expected_type = expected_type
        self._default_value = default_value

    @property
    def parameter_name(self) -> str:
        return self._parameter_name

    @property
    def expected_type(self) -> Type:
        return self._expected_type

    @property
    def def_val(self) -> object:
        return self._default_value

    @importability_check
    def execute_test(self) -> TestResult:
        """Meoda se pokusí ověřit, že daná funkce v daném modulu obsahuje
        parametr specifikovaného názvu a typu a případně (je-li dostupné) i
        defaultní hodnotu parametru.
        """
        try:
            if not self.has_function:
                return TestResult.NOT_TST
            signature = inspect.signature(self.function)

            # Obsahuje parametr s daným názvem
            if self.parameter_name not in signature.parameters.keys():
                return TestResult.FAILURE

            parameter = signature.parameters[self.parameter_name]

            # Daný parametr je daného typu
            if parameter.annotation != self.expected_type:
                return TestResult.FAILURE

            # Daný parametr má přidělenu
            elif self.def_val and parameter.default != self.def_val:
                return TestResult.FAILURE

            # Jinak úspěšné splnění testu
            return TestResult.SUCCESS
        except:
            return TestResult.NOT_TST
