
def is_valid_for_codegen(name):
    if len(name) == 0:
        raise RuntimeError("Empty argument name for codegen")
    if name[0].isdigit():
        return False
    return True

