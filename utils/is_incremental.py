
def is_incremental(testcase: DataDrivenTestCase) -> bool:
    return "incremental" in testcase.name.lower() or "incremental" in testcase.file

