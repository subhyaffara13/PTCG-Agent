
def _get_build_args_of_chosen_isa(vec_isa: VecISA) -> tuple[list[str], list[str]]:
    macros: list[str] = []
    build_flags: list[str] = []
    if vec_isa != invalid_vec_isa:
        # Add Windows support later.
        macros.extend(copy.deepcopy(x) for x in vec_isa.build_macro())

        build_flags = [vec_isa.build_arch_flags()]

        if config.is_fbcode():
            cap = str(vec_isa).upper()
            macros = [
                f"CPU_CAPABILITY={cap}",
                f"CPU_CAPABILITY_{cap}",
                f"HAVE_{cap}_CPU_DEFINITION",
            ]

    return macros, build_flags

