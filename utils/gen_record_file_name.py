
def gen_record_file_name(exc: Exception, code: CodeType) -> str:
    return f"{get_debug_dir()}/error_recordings/\
{code.co_name}_{type(exc).__name__}_{code.co_firstlineno}.rec"

