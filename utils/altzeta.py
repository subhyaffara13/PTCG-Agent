
def altzeta(ctx, s, **kwargs):
    try:
        return ctx._altzeta(s, **kwargs)
    except NotImplementedError:
        return ctx._altzeta_generic(s)

