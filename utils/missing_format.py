
def missing_format(Validator):
    def missing_format(test):  # pragma: no cover
        schema = test.schema
        if (
            schema is True
            or schema is False
            or "format" not in schema
            or schema["format"] in Validator.FORMAT_CHECKER.checkers
            or test.valid
        ):
            return

        return f"Format checker {schema['format']!r} not found."
    return missing_format

