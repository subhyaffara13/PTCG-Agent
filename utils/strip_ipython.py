
def strip_ipython(code):
    return '\n'.join(
        [line for line in code.split('\n') if not line.startswith('%')]
    )

