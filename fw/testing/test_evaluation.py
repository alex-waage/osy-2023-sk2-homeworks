"""Tento modul obsahuje především funkci pro automatické otestování a vypsání
výsledků dle dodaných test targetů."""

from typing import Callable

from fw.testing.case import TestResult
from fw.utils import fs
from fw.utils.logging import resolve_test_result, resolve_info


def evaluate_tests(results: tuple) -> tuple:
    """Funkce vyhodnotí počty úspěšných, netestovaných a neúspěšných
    testovacích případů.

    Vrací ntici v uspořádání (úspěšné, netestované, neúspěšné).
    """

    def prefilter(res):
        return tuple(map(lambda r: r[0], res[1]))

    results = prefilter(results)

    success = len([t for t in results if t == TestResult.SUCCESS])
    not_tst = len([t for t in results if t == TestResult.NOT_TST])
    failure = len([t for t in results if t == TestResult.FAILURE])

    return success, not_tst, failure


def run_tests(build_function: Callable):
    """Sputstí všechny testy všech balíčků a na konec vypíše agregované
    výsledky."""

    # Připrav si všechny podadresáře adresáře 'src'
    package_names = fs.list_directories_without_pycache(
        fs.join_path_in_project("src"))

    # Připrav si seznam na všechny kumulované výsledky
    results = []

    # Pro každý podadresář
    for package_name in package_names:

        # Udělej hlavičku test targetu
        print(f"\n{200 * '*'}")
        print("*", fs.basename(package_name).upper().replace("_", ", "))
        print(200 * "*")

        # Úložiště výsledků všech testovacích případů
        test_cases = []

        # Pro každý test target z vybudovaných test targetů pro daný balíček
        for target in build_function(package_name):

            # Pro každý testovací scénář
            for test_script in target.test_scripts:

                # Vypiš úvodní informační sdělení o příslušnosti
                print(resolve_info(f"\n# - {test_script.test_script_name}"))

                # Spusť testovací případy daného testovacího scénáře
                for test_case_result in test_script.execute():

                    # Ulož si výsledky
                    test_cases.append(test_case_result)

                    # Vypiš hodnocení
                    print(resolve_test_result(
                        test_case_result[0],
                        test_case_result[1].name,
                        test_case_result[1].description))

        # Připoj výsledky daného balíčku
        results.append((package_name, test_cases))

    print(f"\n{150 * '#'}\n")

    # Pro každý kumulovaný výsledek
    for result in results:
        # Přepočti si výsledný rating
        evaluated = evaluate_tests(result)
        success = evaluated[0]
        all_tests = sum(evaluated)

        # Vypiš název balíčku a úspěšnost
        print(f"{fs.basename(result[0]).upper().replace('_', ', ')} - "
              f"Úspěšnost: {success} ze {all_tests} testů")
