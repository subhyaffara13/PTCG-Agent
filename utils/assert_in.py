
def assert_in(member, collection, msg=None):
    message = msg if msg is not None else f"{member!r} not found in {collection!r}"
    assert_(member in collection, msg=message)

