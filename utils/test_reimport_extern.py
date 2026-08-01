
def test_reimport_extern():
    packaging2 = importlib.import_module(packaging.__name__)
    assert packaging is packaging2

