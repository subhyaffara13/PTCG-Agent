import re

def replace_cascade_sum_with_add(buffer: IndentedBuffer):
    """
    Replaces `acc = cascade_sum_combine(value, ...)` with `acc = acc + value;`
    """

    pattern = r"(.*?)\s*=\s*cascade_sum_combine\(([^,]+),.*?\);"
    for i, line in enumerate(buffer._lines):
        assert isinstance(
            line,
            (
                str,
                DeferredLine,
            ),
        )
        content = line.line if isinstance(line, DeferredLine) else line
        match = re.search(pattern, content)
        if match:
            acc, value = match.groups()
            new_content = re.sub(pattern, f"{acc} = {acc} + {value};", content)
            if isinstance(line, DeferredLine):
                line.line = new_content
            else:
                buffer._lines[i] = new_content

