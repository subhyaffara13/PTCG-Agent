
def si(ctx, z):
    try:
        return ctx._si(z)
    except NotImplementedError:
        return ctx._si_generic(z)


def si(width):
    return IntegerType.get_signed(width)

