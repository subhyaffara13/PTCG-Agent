
def _extract_members(
    mod: nn.Module,
    named_members: Callable[..., Iterable[tuple[str, Tensor]]],
    subclass: Callable[[Tensor], Tensor],
) -> tuple[tuple[Tensor, ...], tuple[str, ...], dict[str, list[str]]]:
    all_named_members = tuple(named_members(remove_duplicate=False))
    unique_named_members = tuple(named_members(remove_duplicate=True))
    names_map = create_names_map(unique_named_members, all_named_members)

    # Remove all the members in the model
    # pyrefly: ignore [implicit-any]
    memo = {}
    accessor = NamedMemberAccessor(mod)
    for name, p in all_named_members:
        if p not in memo:
            memo[p] = subclass(torch.empty_like(p, device="meta"))
        replacement = memo[p]
        accessor.set_tensor(name, replacement)

    if len(unique_named_members) == 0:
        names, params = (), ()
    else:
        names, params = zip(*unique_named_members)  # type: ignore[assignment]
    return params, names, names_map

