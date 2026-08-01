
def _ensure_exports_in_init(filepath, top_defs, pkg_init):
    """Ensure __init__.py exports everything from the refactored file."""
    if not pkg_init.exists():
        return
    
    init_text = pkg_init.read_text(encoding='utf-8')
    stem = filepath.stem
    
    # Add import if missing
    for defn in top_defs:
        imp_line = f"from .{stem} import {defn.name}"
        if imp_line not in init_text:
            init_text += imp_line + '\n'
    
    pkg_init.write_text(init_text, encoding='utf-8')

