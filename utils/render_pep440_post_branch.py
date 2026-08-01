
def render_pep440_post_branch(pieces):
    """TAG[.postDISTANCE[.dev0]+gHEX[.dirty]] .

    The ".dev0" means not master branch.

    Exceptions:
    1: no tags. 0.postDISTANCE[.dev0]+gHEX[.dirty]
    """
    if pieces["closest-tag"]:
        rendered = pieces["closest-tag"]
        if pieces["distance"] or pieces["dirty"]:
            rendered += f".post{pieces['distance']}"
            if pieces["branch"] != "master":
                rendered += ".dev0"
            rendered += plus_or_dot(pieces)
            rendered += f"g{pieces['short']}"
            if pieces["dirty"]:
                rendered += ".dirty"
    else:
        # exception #1
        rendered = f"0.post{pieces['distance']}"
        if pieces["branch"] != "master":
            rendered += ".dev0"
        rendered += f"+g{pieces['short']}"
        if pieces["dirty"]:
            rendered += ".dirty"
    return rendered

