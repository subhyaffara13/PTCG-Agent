
def test_subclass_respected():
    # GH#49579
    class MyCustomTimedelta(Timedelta):
        pass

    td = MyCustomTimedelta("1 minute")
    assert isinstance(td, MyCustomTimedelta)

