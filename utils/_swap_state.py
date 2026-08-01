
def _swap_state(
    mod: nn.Module, names_map: dict[str, list[str]], elems: Iterable[Tensor]
) -> list[Tensor]:
    result: list[Tensor] = []
    accessor = NamedMemberAccessor(mod)
    for (_, attr_names), elem in zip(names_map.items(), elems):
        for i, attr_name in enumerate(attr_names):
            if i == 0:
                result.append(accessor.swap_tensor(attr_name, elem))
            else:
                accessor.set_tensor(attr_name, elem)
    return result

