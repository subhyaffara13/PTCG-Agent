
def translate_args(
    sig: CppSignature | DispatcherSignature,
    cpp_sig: CppSignature,
) -> str:
    # Adds SpecialArgName.possibly_redundant_memory_format NamedCType for memory_format bindings
    def add_spl_memory_format_binding(input_bindings: list[Binding]) -> list[Binding]:
        output_bindings: list[Binding] = []
        for binding in input_bindings:
            if binding.name == "memory_format":
                spl_mem_format_binding = Binding(
                    nctype=NamedCType(
                        SpecialArgName.possibly_redundant_memory_format,
                        binding.nctype.type,
                    ),
                    name=binding.name,
                    default=binding.default,
                    argument=binding.argument,
                )
                output_bindings.append(spl_mem_format_binding)
            else:
                output_bindings.append(binding)
        return output_bindings

    src_bindings = list(sig.arguments())
    goal_bindings = list(cpp_sig.arguments())
    # When last argument of CPP signature has SpecialArgName.possibly_redundant_memory_format NCType,
    # get memory_format bindings of dispatcher signature to have the same NCType as well
    for arg in goal_bindings:
        if arg.nctype.name == SpecialArgName.possibly_redundant_memory_format:
            src_bindings = add_spl_memory_format_binding(src_bindings)
            break
    exprs = translate(src_bindings, goal_bindings)
    return ", ".join(a.expr for a in exprs)

