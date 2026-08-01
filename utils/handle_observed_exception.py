
def handle_observed_exception(tx: Any) -> None:
    # This is essentially exception handling code, equivalent of this pseudo code
    #
    # try:
    #     ... somebody raising StopIteration
    # except StopIteration
    #     pass
    #
    # If this was going through the python code, we would have called exception_handler method, but FOR_ITER
    # handles the exception completely in CPython. For example for 3.11, the resulting bytecode is
    #
    #
    #   6          46 LOAD_GLOBAL              2 (StopIteration)
    #              58 RAISE_VARARGS            1
    #         >>   60 PUSH_EXC_INFO

    #   7          62 LOAD_GLOBAL              2 (StopIteration)
    #              74 CHECK_EXC_MATCH
    #              76 POP_JUMP_FORWARD_IF_FALSE     3 (to 84)
    #              78 POP_TOP

    #   8          80 POP_EXCEPT
    #

    # Fortunately this translates to a simple pop from the exn_vt_stack
    tx.exn_vt_stack.clear_current_exception()

