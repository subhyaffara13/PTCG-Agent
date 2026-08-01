
def random_string() -> str:
    return binascii.hexlify(os.urandom(8)).decode("ascii")


def random_string(length=10):
    """
    Returns a random N character long string.
    """
    return "".join(  # nosec
        random.choice(string.ascii_lowercase) for x in range(length)
    )


def random_string(L=15, seed=None):
    return "".join([seed.choice(string.ascii_letters) for n in range(L)])

