
def codegen_per_backend_entries() -> str:
    r: list[str] = []
    for fk in FUNCTIONALITY_KEYS:
        r.extend(f"    {fk}{bc} = auto()" for bc in BACKEND_COMPONENTS)
    return "\n".join(r)

