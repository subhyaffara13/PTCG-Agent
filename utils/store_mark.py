
def store_mark(obj, mark: Mark) -> None:
    """Store a Mark on an object.

    This is used to implement the Mark declarations/decorators correctly.
    """
    assert isinstance(mark, Mark), mark

    from ..fixtures import getfixturemarker

    if getfixturemarker(obj) is not None:
        fail(
            "Marks cannot be applied to fixtures.\n"
            "See docs: https://docs.pytest.org/en/stable/deprecations.html#applying-a-mark-to-a-fixture-function"
        )

    # Always reassign name to avoid updating pytestmark in a reference that
    # was only borrowed.
    obj.pytestmark = [*get_unpacked_marks(obj, consider_mro=False), mark]

