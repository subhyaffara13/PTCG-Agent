
def get_default_capabilities(func_name, delegator):
    if delegator is None or func_name in untested:
        return xp_capabilities(np_only=True)
    return xp_capabilities()

