
def is_standard_setattr(val: object) -> bool:
    return val in (object.__setattr__, BaseException.__setattr__)

