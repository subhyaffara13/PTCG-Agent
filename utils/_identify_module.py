
def _identify_module(file, main=None):
    """identify the name of the module stored in the given file-type object"""
    from pickletools import genops
    UNICODE = {'UNICODE', 'BINUNICODE', 'SHORT_BINUNICODE'}
    found_import = False
    try:
        for opcode, arg, pos in genops(file.peek(256)):
            if not found_import:
                if opcode.name in ('GLOBAL', 'SHORT_BINUNICODE') and \
                        arg.endswith('_import_module'):
                    found_import = True
            else:
                if opcode.name in UNICODE:
                    return arg
        else:
            raise UnpicklingError("reached STOP without finding main module")
    except (NotImplementedError, ValueError) as error:
        # ValueError occours when the end of the chunk is reached (without a STOP).
        if isinstance(error, NotImplementedError) and main is not None:
            # file is not peekable, but we have main.
            return None
        raise UnpicklingError("unable to identify main module") from error

