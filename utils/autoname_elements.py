import sys

def autoname_elements() -> None:
    """
    Utility to simplify mass-naming of parser elements, for
    generating railroad diagram with named subdiagrams.
    """

    # guard against _getframe not being implemented in the current Python
    getframe_fn = getattr(sys, "_getframe", lambda _: None)
    calling_frame = getframe_fn(1)
    if calling_frame is None:
        return

    # find all locals in the calling frame that are ParserElements
    calling_frame = typing.cast(types.FrameType, calling_frame)
    for name, var in calling_frame.f_locals.items():
        # if no custom name defined, set the name to the var name
        if isinstance(var, ParserElement) and not var.customName:
            var.set_name(name)

