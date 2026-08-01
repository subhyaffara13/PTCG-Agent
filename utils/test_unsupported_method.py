
def test_unsupported_method():
    class Base:
        def method_1(self):
            pass

        def method_2(self):
            pass

    class Child(Base):
        method_1 = _api.unsupported_method()
        method_2 = _api.unsupported_method(append_message="Sorry!")

    child = Child()
    with pytest.raises(_api.UnsupportedError,
                       match=r"^Child does not support 'method_1'\.$"):
        child.method_1()
    with pytest.raises(_api.UnsupportedError,
                       match=r"^Child does not support 'method_2'\. Sorry!$"):
        child.method_2()

