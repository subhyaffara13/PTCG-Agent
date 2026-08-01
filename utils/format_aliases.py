
def format_aliases(aliases: list[str]) -> str:
    fmted = []
    for a in aliases:
        dashes = "-" if len(a) == 1 else "--"
        fmted.append(f"``{dashes}{a}``")
    return ", ".join(fmted)

