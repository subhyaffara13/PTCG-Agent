
def _find_all_over_50():
    """Find all .py files > 50 lines that have a __init__.py sibling (are in packages)."""
    results = []
    # Only target these main source dirs
    for root_dir in [ROOT / 'cb_agents', ROOT / 'factory']:
        if not root_dir.exists():
            continue
        for f in sorted(root_dir.rglob("*.py")):
            if f.name == '__init__.py' or f.name.startswith('__') and f.name.endswith('__.py'):
                continue
            # Must have __init__.py parent (be in a package)
            if not (f.parent / '__init__.py').exists():
                continue
            # Skip files in submission/ 
            if 'submission' in f.parts:
                continue
            lines = len(f.read_text(encoding='utf-8').splitlines())
            if lines > LINE_LIMIT:
                results.append((f, lines))
    return sorted(results, key=lambda x: -x[1])

