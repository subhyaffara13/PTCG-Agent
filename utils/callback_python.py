
def callback_python(a, user_data=None):
    if a == ERROR_VALUE:
        raise ValueError("bad value")

    if user_data is None:
        return a + 1
    else:
        return a + user_data

