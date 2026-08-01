
def _disable_interpreter():
    global RUN_WITH_INTERPRETER
    old_flag = RUN_WITH_INTERPRETER
    RUN_WITH_INTERPRETER = False
    try:
        yield
    finally:
        RUN_WITH_INTERPRETER = old_flag

