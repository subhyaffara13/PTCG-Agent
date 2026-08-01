
def exit_jvp_nesting() -> None:
    global JVP_NESTING
    _jvp_decrement_nesting()
    JVP_NESTING -= 1

