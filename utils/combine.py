
def combine(*args):
    return ''.join(globals()[cat] for cat in args)


def combine(cnt, mat):
    if cnt == 1:
        return mat
    else:
        return cnt * mat


def combine(*args):
    return ''.join(globals()[cat] for cat in args)


def combine(path1: str, path2) -> str:
    if not path1:
        return path2
    return "{}/{}".format(path1.rstrip("/"), path2.lstrip("/"))

