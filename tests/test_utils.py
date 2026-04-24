import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from src.utils import add, multiply  # noqa: E402


def test_add_two_positive_numbers():
    assert add(2, 3) == 5


def test_add_with_zero():
    assert add(10, 0) == 10


def test_add_negative_numbers():
    assert add(-4, -6) == -10


def test_multiply_two_numbers():
    assert multiply(3, 4) == 12


def test_multiply_by_zero():
    assert multiply(7, 0) == 0


def test_multiply_by_one():
    assert multiply(5, 1) == 5
