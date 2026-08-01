
def _ext_modules(dist: Distribution, val: list[dict]) -> list[Extension]:
    existing = dist.ext_modules or []
    args = ({k.replace("-", "_"): v for k, v in x.items()} for x in val)
    new = [Extension(**kw) for kw in args]
    return [*existing, *new]

