
def assert_asserts(x):
    try:
        x()
    except AssertionError:
        return True
    return False

