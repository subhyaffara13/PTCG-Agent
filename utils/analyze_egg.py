
def analyze_egg(egg_dir, stubs):
    # check for existing flag in EGG-INFO
    for flag, fn in safety_flags.items():
        if os.path.exists(os.path.join(egg_dir, 'EGG-INFO', fn)):
            return flag
    if not can_scan():
        return False
    safe = True
    for base, dirs, files in walk_egg(egg_dir):
        for name in files:
            if name.endswith(('.py', '.pyw')):
                continue
            elif name.endswith(('.pyc', '.pyo')):
                # always scan, even if we already know we're not safe
                safe = scan_module(egg_dir, base, name, stubs) and safe
    return safe

