
def collect_defined_kernels(kernel_list: list[str]) -> Iterator[None]:
    from .codegen.wrapper import PythonWrapperCodegen

    orig_define_kernel = PythonWrapperCodegen.define_kernel

    def define_kernel(
        self: PythonWrapperCodegen,
        kernel_name: str,
        kernel_code: str,
        metadata: str | None = None,
        gpu: bool = True,
        cpp_definition: str | None = None,
    ) -> Any:
        kernel_list.append(kernel_code)
        return orig_define_kernel(
            self, kernel_name, kernel_code, metadata, gpu, cpp_definition
        )

    with mock.patch.object(PythonWrapperCodegen, "define_kernel", define_kernel):
        yield

