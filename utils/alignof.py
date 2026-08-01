
def alignof(arg):
    """ Generate of FunctionCall instance for calling 'alignof' """
    return FunctionCall('alignof', [String(arg) if isinstance(arg, str) else arg])

