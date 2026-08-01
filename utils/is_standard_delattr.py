
def is_standard_delattr(val: object) -> bool:
    return val in (object.__delattr__, BaseException.__delattr__)

