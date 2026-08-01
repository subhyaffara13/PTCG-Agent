
def condition_as_parse_action(
    fn: ParseCondition, message: typing.Optional[str] = None, fatal: bool = False
) -> ParseAction:
    """
    Function to convert a simple predicate function that returns ``True`` or ``False``
    into a parse action. Can be used in places when a parse action is required
    and :meth:`ParserElement.add_condition` cannot be used (such as when adding a condition
    to an operator level in :class:`infix_notation`).

    Optional keyword arguments:

    :param message: define a custom message to be used in the raised exception
    :param fatal: if ``True``, will raise :class:`ParseFatalException`
                  to stop parsing immediately;
                  otherwise will raise :class:`ParseException`

    """
    msg = message if message is not None else "failed user-defined condition"
    exc_type = ParseFatalException if fatal else ParseException
    fn = _trim_arity(fn)

    @wraps(fn)
    def pa(s, l, t):
        if not bool(fn(s, l, t)):
            raise exc_type(s, l, msg)

    return pa


def conditionAsParseAction(fn, message=None, fatal=False):
    msg = message if message is not None else "failed user-defined condition"
    exc_type = ParseFatalException if fatal else ParseException
    fn = _trim_arity(fn)

    @wraps(fn)
    def pa(s, l, t):
        if not bool(fn(s, l, t)):
            raise exc_type(s, l, msg)

    return pa

