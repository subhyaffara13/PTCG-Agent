
def on_bootstrap():
    """Called by astroid_bootstrapping()."""
    _extend_builtins(
        {
            "bytes": partial(_extend_string_class, code=BYTES_CLASS, rvalue="b''"),
            "str": partial(_extend_string_class, code=STR_CLASS, rvalue="''"),
        }
    )

