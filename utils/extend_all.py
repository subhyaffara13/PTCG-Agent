
def extend_all(module):
    existing = set(__all__)
    mall = module.__all__
    for a in mall:
        if a not in existing:
            __all__.append(a)

