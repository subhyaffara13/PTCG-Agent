
def get_numversion_from_version(v: str) -> tuple[int, int, int]:
    """Kept for compatibility reason.

    See https://github.com/pylint-dev/pylint/issues/4399
    https://github.com/pylint-dev/pylint/issues/4420,
    """
    version = v.replace("pylint-", "")
    result_version = []
    for number in version.split(".")[0:3]:
        try:
            result_version.append(int(number))
        except ValueError:
            current_number = ""
            for char in number:
                if char.isdigit():
                    current_number += char
                else:
                    break
            try:
                result_version.append(int(current_number))
            except ValueError:
                result_version.append(0)
    while len(result_version) != 3:
        result_version.append(0)

    return tuple(result_version)  # type: ignore[return-value] # mypy can't infer the length

