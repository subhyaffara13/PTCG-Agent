
def generate_bin_op_forward_only_wrapper(
    fn: FuncIR, emitter: Emitter, gen: WrapperGenerator
) -> None:
    gen.emit_arg_processing(error=GotoHandler("typefail"), raise_exception=False)
    handle_third_pow_argument(fn, emitter, gen, if_unsupported=["goto typefail;"])
    gen.emit_call(not_implemented_handler="goto typefail;")
    gen.emit_error_handling()
    emitter.emit_label("typefail")
    # If some argument has an incompatible type, treat this the same as
    # returning NotImplemented, and try to call the reverse operator method.
    #
    # Note that in normal Python you'd instead of an explicit
    # return of NotImplemented, but it doesn't generally work here
    # the body won't be executed at all if there is an argument
    # type check failure.
    #
    # The recommended way is to still use a type check in the
    # body. This will only be used in interpreted mode:
    #
    #    def __add__(self, other: int) -> Foo:
    #        if not isinstance(other, int):
    #            return NotImplemented
    #        ...
    generate_bin_op_reverse_dunder_call(fn, emitter, reverse_op_methods[fn.name])
    gen.finish()

