
def extract_static_func_decls(funcs):
    """Get declarations for static functions that are called across sub-files."""
    # funcs is list of (name, start, end, text, is_static)
    # We need to know which static functions are called by non-static functions
    # For simplicity, declare all static functions in the internal header
    decls = []
    for f in funcs:
        if f[4]:  # is_static
            # Extract signature (first line up to {)
            text = f[3]
            first_line = text.split('\n')[0]
            # Remove { at end
            sig = first_line.rstrip()
            if sig.endswith('{'):
                sig = sig[:-1].strip()
            # Replace leading 'static ' with nothing
            sig = re.sub(r'^static\s+', '', sig)
            decls.append((f[0], sig + ';'))
    return decls

