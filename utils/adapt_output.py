
def adapt_output(testcase: DataDrivenTestCase) -> list[str]:
    """Translates the generic _program.py into the actual filename."""
    program = "_" + testcase.name + ".py"
    return [program_re.sub(program, line) for line in testcase.output]

