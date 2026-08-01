
def extract_globals(lines, first_func_line):
    """Extract global variable declarations from the preamble."""
    globals_list = []
    for line in lines[:first_func_line]:
        stripped = line.strip()
        # Match: [static] type name = ... ;
        if stripped.startswith('static ') and '=' in stripped and stripped.rstrip().endswith(';'):
            # Get text before '='
            before_eq = stripped.split('=')[0].strip()
            # Remove 'static'
            if before_eq.startswith('static '):
                before_eq = before_eq[7:].strip()
            # Split into words - last word is the variable name
            words = before_eq.split()
            if len(words) >= 2:
                name = words[-1].rstrip('*&')
                type_str = ' '.join(words[:-1])
                globals_list.append((type_str, name, stripped))
    return globals_list

