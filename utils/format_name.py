
def format_name(project: NormalizedName, extras: frozenset[NormalizedName]) -> str:
    if not extras:
        return project
    extras_expr = ",".join(sorted(extras))
    return f"{project}[{extras_expr}]"

