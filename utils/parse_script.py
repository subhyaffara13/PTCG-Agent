
def parse_script(input: list[str]) -> list[list[str]]:
    """Parse testcase.input into steps.

    Each command starts with a line starting with '$'.
    The first line (less '$') is sent to the shell.
    The remaining lines are expected output.
    """
    steps = []
    step: list[str] = []
    for line in input:
        if line.startswith("$"):
            if step:
                assert step[0].startswith("$")
                steps.append(step)
                step = []
        step.append(line)
    if step:
        steps.append(step)
    return steps

