
def create_errors(error_tuples: list[ErrorTuple]) -> list[MypyError]:
    errors: list[MypyError] = []
    latest_error_at_location: dict[_ErrorLocation, MypyError] = {}

    for error_tuple in error_tuples:
        file_path, line, column, end_line, end_column, severity, message, errorcode = error_tuple
        if file_path is None:
            continue

        assert severity in ("error", "note")
        if severity == "note":
            error_location = (file_path, line, column)
            error = latest_error_at_location.get(error_location)
            if error is None:
                # This is purely a note, with no error correlated to it
                error = MypyError(
                    file_path,
                    line,
                    column,
                    end_line,
                    end_column,
                    message,
                    errorcode,
                    severity="note",
                )
                errors.append(error)
                continue

            error.hints.append(message)

        else:
            error = MypyError(
                file_path, line, column, end_line, end_column, message, errorcode, severity="error"
            )
            errors.append(error)
            error_location = (file_path, line, column)
            latest_error_at_location[error_location] = error

    return errors

