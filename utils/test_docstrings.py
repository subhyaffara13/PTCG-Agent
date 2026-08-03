import re

def test_docstrings(doc):
    assert doc(UserType) == "A `py::class_` type for testing"
    assert UserType.__name__ == "UserType"
    assert UserType.__module__ == "pybind11_tests"
    assert UserType.get_value.__name__ == "get_value"
    assert UserType.get_value.__module__ == "pybind11_tests"

    assert (
        doc(UserType.get_value)
        == """
        get_value(self: m.UserType) -> int

        Get value using a method
    """
    )
    assert doc(UserType.value) == "Get/set value using a property"

    assert (
        doc(m.NoConstructor.new_instance)
        == """
        new_instance() -> m.class_.NoConstructor

        Return an instance
    """
    )


def test_docstrings():
    badones = [r',\s*,', r'\(\s*,', r'^\s*:']
    for distname in stats.__all__:
        dist = getattr(stats, distname)
        if isinstance(dist, (stats.rv_discrete | stats.rv_continuous)):
            for regex in badones:
                assert_(re.search(regex, dist.__doc__) is None)

