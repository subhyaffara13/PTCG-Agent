
def has_managed_dict(cl: ClassIR, emitter: Emitter) -> bool:
    """Should the class get the Py_TPFLAGS_MANAGED_DICT flag?"""
    # On 3.11 and earlier the flag doesn't exist and we use
    # tp_dictoffset instead.  If a class inherits from Exception, the
    # flag conflicts with tp_dictoffset set in the base class.
    return (
        emitter.capi_version >= (3, 12)
        and cl.has_dict
        and cl.builtin_base != "PyBaseExceptionObject"
    )

