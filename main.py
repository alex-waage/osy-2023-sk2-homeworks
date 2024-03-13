from fw.testing.test_evaluation import run_tests
from fw.utils.logging import beautify
from test.test_definition import build_package_level_tests

"""Pokud to Váš terminál podporuje, lze použít barevné zvýraznění. Defaultně
je zapnuté. Pokud ne, je doporučeno toto vypnout (odkomentováním tohoto volání
funkce 'beautify(False)').

Některé konzole toto nepodporují a řídící znaky pro označení barvy pak 
vypisují jako součást řádku, čímž zásadně snižují čitelnost."""
# beautify(False)

# Iniciuje vybudování a spuštění testů
run_tests(build_package_level_tests)
