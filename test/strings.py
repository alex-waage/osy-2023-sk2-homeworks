"""Modul obsahuje definici testů pro ověření správné práce s textovými
řetězci."""
from fw.plugins.plugin_loader import PluginLoader
from fw.testing.script import ModuleLevelFunctionTestScript
from fw.testing.target import TestTarget


def test_strings(package_path: str) -> TestTarget:
    """Vybuduje test target pro ověření správnosti modulu práce s textovými
    řetězci.
    """

    plugin = PluginLoader(package_path, "strings.py").plugin

    uppercase = ModuleLevelFunctionTestScript(
        plugin, "to_uppercase", "Převeď string na velká písmena",
        (("to_be_uppercase", str),),
        (("A", ("a",)), ("ABC", ("aBc",)),), str)

    lowercase = ModuleLevelFunctionTestScript(
        plugin, "to_lowercase", "Převeď text na malá písmena",
        (("to_be_lowercase", str),),
        (("a", ("a",)), ("abc", ("aBc",)),), str)

    sensitive_equal = ModuleLevelFunctionTestScript(
        plugin, "equal_texts_case_sensitive",
        "Porovnej dva texty (uvažuj velikost znaků)",
        (("s1", str), ("s2", str),),
        ((True, ("a", "a")), (False, ("a", "A")), (False, ("a", "B")),), bool)

    insensitive_equal = ModuleLevelFunctionTestScript(
        plugin, "equal_texts_case_insensitive",
        "Porovnej dva texty (neuvažuj velikost znaků)",
        (("s1", str), ("s2", str),),
        ((True, ("a", "a")), (True, ("a", "A")), (False, ("a", "B")),), bool)

    concat = ModuleLevelFunctionTestScript(
        plugin, "concat", "Spoj dva textové řetězce",
        (("s1", str), ("s2", str),),
        (("ab", ("a", "b")), ("longword", ("long", "word")), ("", ("", ""))),
        str)

    string_len = ModuleLevelFunctionTestScript(
        plugin, "string_length", "Vrať délku řetězce, mezeru a původní text",
        (("measurable", str),),
        (("1 a", ("a",)), ("2 ab", ("ab",)), ("0 ", ("",)),), str)

    cut = ModuleLevelFunctionTestScript(
        plugin, "omit_first_and_last",
        "Vrať řetězec bez prvního a posledního znaku", (("to_be_cut", str),),
        (("bc", ("abcd",)), ("Y", ("XYZ",)),), str)

    return TestTarget(
        plugin,
        [uppercase, lowercase, sensitive_equal, insensitive_equal, concat,
         string_len, cut])
