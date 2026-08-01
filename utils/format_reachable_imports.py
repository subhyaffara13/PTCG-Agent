
def format_reachable_imports(node: MypyFile) -> list[str]:
    """Format reachable imports from a MypyFile node.

    Returns a list of strings representing reachable imports with line numbers and flags.
    """
    from mypy.nodes import Import, ImportAll, ImportFrom

    output: list[str] = []

    # Filter for reachable imports (is_unreachable == False)
    reachable_imports = [imp for imp in node.imports if not imp.is_unreachable]

    for imp in reachable_imports:
        line_num = imp.line

        # Collect flags (only show when flag is False/not set)
        flags = []
        if not imp.is_top_level:
            flags.append("not top_level")
        if imp.is_mypy_only:
            flags.append("mypy_only")

        flags_str = " [" + ", ".join(flags) + "]" if flags else ""

        if isinstance(imp, Import):
            # Format: line: import foo [as bar] [flags]
            for module_id, as_id in imp.ids:
                if as_id:
                    output.append(f"{line_num}: import {module_id} as {as_id}{flags_str}")
                else:
                    output.append(f"{line_num}: import {module_id}{flags_str}")
        elif isinstance(imp, ImportFrom):
            # Format: line: from foo import bar, baz [as b] [flags]
            # Handle relative imports
            if imp.relative > 0:
                prefix = "." * imp.relative
                if imp.id:
                    module = f"{prefix}{imp.id}"
                else:
                    module = prefix
            else:
                module = imp.id

            # Group all names together
            name_parts = []
            for name, as_name in imp.names:
                if as_name:
                    name_parts.append(f"{name} as {as_name}")
                else:
                    name_parts.append(name)

            names_str = ", ".join(name_parts)
            output.append(f"{line_num}: from {module} import {names_str}{flags_str}")
        elif isinstance(imp, ImportAll):
            # Format: line: from foo import * [flags]
            # Handle relative imports
            if imp.relative > 0:
                prefix = "." * imp.relative
                if imp.id:
                    module = f"{prefix}{imp.id}"
                else:
                    module = prefix
            else:
                module = imp.id

            output.append(f"{line_num}: from {module} import *{flags_str}")

    return output

