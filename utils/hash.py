import os

def hash(filename: os.PathLike, algorithm: str = "sha256") -> str:
    """
    Hash the given filename. Unavailable in `pip<8.0.0`
    """
    if incompatible:
        raise Incompatible

    if algorithm not in ["sha256", "sha384", "sha512"]:
        raise InvalidArguments("Algorithm {} not supported".format(algorithm))

    result = call("hash", "--algorithm", algorithm, filename)

    # result is of the form:
    # <filename>:\n--hash=<algorithm>:<hash>\n
    return result.strip().split(":")[-1]

