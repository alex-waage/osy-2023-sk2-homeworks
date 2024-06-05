"""Modul obsahuje definici testů pro ověření pochopení definice funkcí."""
from fw.plugins.plugin_loader import PluginLoader
from fw.testing.script import ModuleLevelFunctionTestScript
from fw.testing.target import TestTarget


def test_function(package_path: str) -> TestTarget:
    """Vybuduje test target pro ověření správnosti modulu práce s kolekcemi.
    """

    plugin = PluginLoader(package_path, "function.py").plugin

    is_prime = ModuleLevelFunctionTestScript(
        plugin, "is_prime_number", "Rozhodni, jestli je číslo prvočíslem",
        (("number", int),),
        ((True, (2,)), (True, (3,)), (False, (4,)), (True, (5,)),
         (False, (6,)), (True, (7,)), (False, (8,)), (False, (9,)),
         (True, (1231,)),), bool)

    return TestTarget(
        plugin,
        [is_prime, ])
