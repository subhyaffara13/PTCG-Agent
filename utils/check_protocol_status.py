
def check_protocol_status(info: TypeInfo, errors: Errors) -> None:
    """Check that all classes in MRO of a protocol are protocols"""
    if info.is_protocol:
        for type in info.bases:
            if not type.type.is_protocol and type.type.fullname != "builtins.object":
                errors.report(
                    info.line,
                    info.column,
                    "All bases of a protocol must be protocols",
                    severity="error",
                )

