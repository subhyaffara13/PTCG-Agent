
def prettify_frame_locals(
    loc: str, locals: dict[str, Any], symbols: dict[str, Any]
) -> str:
    local_str = "\n".join(f"            {k}: {v}" for k, v in locals.items())
    res = f"""
        Locals:
{local_str}
"""
    if any(v is not None for v in symbols.values()):
        symbol_str = "\n".join(
            f"           {k}: {v}" for k, v in symbols.items() if v is not None
        )
        res += f"""
        Symbols:
{symbol_str}
"""
    return res

