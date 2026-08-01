
def get_code(fn: Callable[P, _T], *args: P.args, **kwargs: P.kwargs) -> list[str]:
    """Get the inductor-generated code, but skip any actual compilation or running."""
    from .graph import GraphLowering

    source_codes: list[str] = []

    def save_output_code(code: str) -> None:
        source_codes.append(code)

    def patched_compile_to_module(self: GraphLowering) -> Any:
        class DummyModule:
            """This is empty to replace the generated triton module"""

            def __init__(self) -> None:
                pass

            def call(self, *args: Any, **kwargs: Any) -> None:
                # Don't do anything when called
                pass

        wrapper_code, kernel_code = (
            self.codegen_with_cpp_wrapper() if self.cpp_wrapper else self.codegen()
        )
        # Skip all the actual compiling.
        save_output_code(wrapper_code.value)
        if kernel_code:
            save_output_code(kernel_code.value)

        return DummyModule()

    with (
        mock.patch.object(
            GraphLowering, "compile_to_module", patched_compile_to_module
        ),
        mock.patch.object(GraphLowering, "save_output_code", save_output_code),
    ):
        torch._dynamo.reset()
        # Note the return here is None
        _ = fn(*args, **kwargs)

    return source_codes

