
def isvalid(nbjson, ref=None, version=None, version_minor=None):
    """Checks whether the given notebook JSON conforms to the current
    notebook format schema. Returns True if the JSON is valid, and
    False otherwise.

    To see the individual errors that were encountered, please use the
    `validate` function instead.
    """
    orig = deepcopy(nbjson)
    try:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            warnings.filterwarnings("ignore", category=MissingIDFieldWarning)
            validate(nbjson, ref, version, version_minor, repair_duplicate_cell_ids=False)
    except ValidationError:
        return False
    else:
        return True
    finally:
        if nbjson != orig:
            raise AssertionError

