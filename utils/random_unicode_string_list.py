
def random_unicode_string_list():
    """Returns an array of 10 100-character strings containing random text"""
    chars = list(string.ascii_letters + string.digits)
    chars = np.array(chars, dtype="U1")
    ret = np.random.choice(chars, size=100 * 10, replace=True)
    return ret.view("U100")

