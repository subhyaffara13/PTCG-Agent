from pathlib import Path


def get_docdir():
    parents = Path(__file__).resolve().parents
    try:
        # Assumes that spin is used to run tests
        nproot = parents[8]
    except IndexError:
        docdir = None
    else:
        docdir = nproot / "doc" / "source" / "f2py" / "code"
    if docdir and docdir.is_dir():
        return docdir
    # Assumes that an editable install is used to run tests
    return parents[3] / "doc" / "source" / "f2py" / "code"

