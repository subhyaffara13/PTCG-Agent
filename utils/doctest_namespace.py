
def doctest_namespace() -> dict[str, Any]:
    """Fixture that returns a :py:class:`dict` that will be injected into the
    namespace of doctests.

    Usually this fixture is used in conjunction with another ``autouse`` fixture:

    .. code-block:: python

        @pytest.fixture(autouse=True)
        def add_np(doctest_namespace):
            doctest_namespace["np"] = numpy

    For more details: :ref:`doctest_namespace`.
    """
    return dict()

