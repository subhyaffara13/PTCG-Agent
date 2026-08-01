
def log_dynamo_start(code: CodeType, skip: int = 0) -> list[str]:
    convert_frame_intern = structured.intern_string(__file__)
    captured_tb = CapturedTraceback.extract(skip=4 + skip).summary()
    frames_interned = structured.from_traceback(captured_tb)
    # Extract and filter the stack
    stack = list(
        itertools.takewhile(
            lambda f: f["filename"] != convert_frame_intern,
            frames_interned,
        )
    ) + [
        {
            "line": code.co_firstlineno,
            "name": code.co_name,
            "filename": structured.intern_string(code.co_filename),
        }
    ]
    # Initialize the ChromiumEventLogger on start
    torch._logging.trace_structured(
        "dynamo_start",
        lambda: {"stack": stack},
    )

    # Capture stack separately without using from_traceback to get the actual filenames
    stack_strings = [
        f"Line: {frame.lineno}, Name: {frame.name}, Filename: {frame.filename}"
        for frame in captured_tb
        if frame.filename != convert_frame_intern
    ] + [
        f"Line: {code.co_firstlineno}, Name: {code.co_name}, Filename: {code.co_filename}"
    ]
    return stack_strings

