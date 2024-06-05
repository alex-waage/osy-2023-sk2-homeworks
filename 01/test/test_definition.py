from typing import Iterable

from fw.testing.target import TestTarget
from fw.utils import fs
from test.collections import test_collections
from test.function import test_function
from test.numbers import test_numbers
from test.strings import test_strings


def build_package_level_tests(package_name: str) -> Iterable[TestTarget]:
    """Základní přístupová funkce, která se stará o poskytování služby
    budování test targetu pro každý jeden balíček."""
    abs_path = fs.join_path_in_project(fs.join_paths("src", package_name))
    test_targets = [
        test_numbers(abs_path),
        test_strings(abs_path),
        test_collections(abs_path),
        test_function(abs_path)
    ]

    return test_targets

