
def _remove_nested(pkg_roots: dict[str, str]) -> dict[str, str]:
    output = dict(pkg_roots.copy())

    for pkg, path in reversed(list(pkg_roots.items())):
        if any(
            pkg != other and _is_nested(pkg, path, other, other_path)
            for other, other_path in pkg_roots.items()
        ):
            output.pop(pkg)

    return output

