
def get_func_call() -> str:
    return (
        "void inductor_entry_impl("
        if torch._inductor.config.cpp_wrapper
        else "def call("
    )

