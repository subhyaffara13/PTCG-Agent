
def _make_mod_name(names):
    if not names: return "part"
    base = names[0] if len(names) == 1 else '_'.join(names[:3])
    base = ''.join(c for c in base if c.isalnum() or c == '_').lower()[:60]
    if not base or base[0].isdigit(): base = "part"
    return base

