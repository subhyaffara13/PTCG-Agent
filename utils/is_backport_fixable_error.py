
def is_backport_fixable_error(e: TypeError) -> bool:
    msg = str(e)

    return sys.version_info < (3, 10) and msg.startswith('unsupported operand type(s) for |: ')

