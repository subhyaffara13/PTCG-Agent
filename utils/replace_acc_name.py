
def replace_acc_name(buffer: IndentedBuffer, name: str, new_name: str):
    for i, line in enumerate(buffer._lines):
        assert isinstance(
            line,
            (
                str,
                DeferredLine,
            ),
        )
        if isinstance(line, DeferredLine):
            line.line = re.sub(r"\b" + f"{name}" + r"\b", f"{new_name}", line.line)
        else:
            buffer._lines[i] = re.sub(r"\b" + f"{name}" + r"\b", f"{new_name}", line)

