import pytest

def func(x):
    return x + 1

def test_answer():
    assert func(3) == 4
    
def test_answer_wrong():
    assert func(3) == 5