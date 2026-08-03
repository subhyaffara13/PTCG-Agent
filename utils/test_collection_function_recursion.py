import copy

def test_collection_function_recursion():
    g = copy(collection_function_recursion())
    assert g()['g'] is g

