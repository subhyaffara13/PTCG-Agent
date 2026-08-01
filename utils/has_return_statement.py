
def has_return_statement(fdef: FuncBase) -> bool:
    """Find if a function has a non-trivial return statement.

    Plain 'return' and 'return None' don't count.
    """
    seeker = ReturnSeeker()
    fdef.accept(seeker)
    return seeker.found

