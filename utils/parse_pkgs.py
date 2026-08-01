
def parse_pkgs(comment: str) -> tuple[list[str], list[str]]:
    if not comment.startswith("# pkgs:"):
        return ([], [])
    else:
        pkgs_str, *args = comment[7:].split(";")
        return ([pkg.strip() for pkg in pkgs_str.split(",")], [arg.strip() for arg in args])

