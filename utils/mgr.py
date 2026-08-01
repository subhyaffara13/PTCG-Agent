
def mgr():
    return create_mgr(
        "a: f8; b: object; c: f8; d: object; e: f8;"
        "f: bool; g: i8; h: complex; i: datetime-1; j: datetime-2;"
        "k: M8[ns, US/Eastern]; l: M8[ns, CET];"
    )

