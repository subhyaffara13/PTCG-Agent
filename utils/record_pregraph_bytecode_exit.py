
def record_pregraph_bytecode_exit(cm: AbstractContextManager[None]) -> None:
    cm.__exit__(None, None, None)

