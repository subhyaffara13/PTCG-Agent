
def ambiguity_register_error_ignore_dup(dispatcher, ambiguities):
    """
    If super signature for ambiguous types is duplicate types, ignore it.
    Else, register instance of ``RaiseNotImplementedError`` for ambiguous types.

    Parameters
    ----------
    dispatcher : Dispatcher
        The dispatcher on which the ambiguity was detected
    ambiguities : set
        Set of type signature pairs that are ambiguous within this dispatcher

    See Also:
        Dispatcher.add
        ambiguity_warn
    """
    for amb in ambiguities:
        signature = tuple(super_signature(amb))
        if len(set(signature)) == 1:
            continue
        dispatcher.add(
            signature, RaiseNotImplementedError(dispatcher),
            on_ambiguity=ambiguity_register_error_ignore_dup
        )

