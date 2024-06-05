from abc import ABC, abstractmethod
from typing import Iterable, Sized


def secure_testing(function):
    """Funkce, která má za cíl sloužit jako dekorátor coby obalující funkce
    pro ověřování v bezpečném režimu. Odchycené výjimky jsou zahozeny a je
    vrácena hodnota False.
    """
    def wrapper(*args):
        """Interní wrapper, který obaluje dodanou funkci blokem try-except."""
        try:
            return function(*args)
        except:
            return False
    # Funkce vrácena zpět
    return wrapper


class Comparator(ABC):

    @abstractmethod
    @secure_testing
    def compare(self, actual: object, expected: object) -> bool:
        """Metoda poskytující službu porovnávání skutečné a očekávané hodnoty.
        """


class ExactComparator(Comparator):
    """Služebník porovnávající očekávaný a skutečný vstup co do přesné
    shodnosti.
    """

    @secure_testing
    def compare(self, actual: object, expected: object) -> bool:
        return actual == expected


class CompareTypes(Comparator):
    """Služebník porovnávající typy vstupních hodnot; přesně."""

    @secure_testing
    def compare(self, actual: object, expected: type) -> bool:
        return type(actual) == expected


class CompareTypesAndSubtypes(Comparator):
    """Služebník poskytující službu porovnání, zda-li je vstupní hodnota
    daného typu či subtypu."""

    @secure_testing
    def compare(self, actual: object, expected: type) -> bool:
        return isinstance(actual, expected)


class CompareStrings(Comparator):
    """Porovnává textové řetězce; dokáže abstrahovat od velikosti písmen i od
    počátečních a koncových mezer."""

    def __init__(self, ignore_casing: bool = False, strip: bool = False):
        self._ic = ignore_casing
        self._strip = strip

    def prepare_string(self, to_be_prepared: str) -> str:
        if self._ic:
            to_be_prepared = to_be_prepared.lower()
        if self._strip:
            to_be_prepared = to_be_prepared.strip()
        return to_be_prepared

    @secure_testing
    def compare(self, actual: str, expected: str) -> bool:
        return self.prepare_string(actual) == self.prepare_string(expected)


class CompareIterablesLengths(Comparator):

    @secure_testing
    def compare(self, actual: Sized, expected: int) -> bool:
        return len(actual) == expected


class CompareContainsAll(Comparator):

    @secure_testing
    def compare(self, actual: Iterable, expected: Iterable) -> bool:
        for expected_value in expected:
            if expected_value not in actual:
                return False
        return True


class CompareOrder(Comparator):

    @secure_testing
    def compare(self, actual: Iterable, expected: Iterable) -> bool:
        actual = list(actual)
        for index, value in enumerate(expected):
            if actual[index] != value:
                return False
        return True
