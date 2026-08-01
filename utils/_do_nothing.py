
def _do_nothing():
    """This does nothing at all, yet it helps turn ``_dispatchable`` into functions.

    Use this with the ``argmap`` decorator to turn ``self`` into a function. It results
    in some small additional overhead compared to calling ``_dispatchable`` directly,
    but ``argmap`` has the property that it can stack with other ``argmap``
    decorators "for free". Being a function is better for REPRs and type-checkers.
    """

