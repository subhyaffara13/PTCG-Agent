import re

def expand_errors(input: list[str], output: list[str], fnam: str) -> None:
    """Transform comments such as '# E: message' or
    '# E:3: message' in input.

    The result is lines like 'fnam:line: error: message'.
    """

    for i in range(len(input)):
        # The first in the split things isn't a comment
        for possible_err_comment in input[i].split(" # ")[1:]:
            m = re.search(
                r"^([ENW]):((?P<col>\d+):)? (?P<message>.*)$", possible_err_comment.strip()
            )
            if m:
                if m.group(1) == "E":
                    severity = "error"
                elif m.group(1) == "N":
                    severity = "note"
                elif m.group(1) == "W":
                    severity = "warning"
                col = m.group("col")
                message = m.group("message")
                message = message.replace("\\#", "#")  # adds back escaped # character
                if col is None:
                    output.append(f"{fnam}:{i + 1}: {severity}: {message}")
                else:
                    output.append(f"{fnam}:{i + 1}:{col}: {severity}: {message}")

