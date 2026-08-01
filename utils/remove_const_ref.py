
def remove_const_ref(binding: Binding) -> Binding:
    return Binding(
        name=binding.name,
        nctype=binding.nctype.remove_const_ref(),
        argument=binding.argument,
        default=binding.default,
    )

