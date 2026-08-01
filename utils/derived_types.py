
def derived_types(
    base_type: type | typing._SpecialForm,
    cpp_type: str,
    list_base: bool,
    optional_base_list: bool,
    optional_list_base: bool,
):
    result: list[tuple[type | typing._SpecialForm | GenericAlias, str]] = [
        (base_type, cpp_type),
        # pyrefly: ignore [not-a-type]
        (typing.Optional[base_type], f"{cpp_type}?"),  # noqa: UP045
    ]

    def derived_seq_types(typ: type | typing._SpecialForm):
        return (
            typing.Sequence[typ],  # type: ignore[valid-type]  # noqa: UP006
            typing.List[typ],  # type: ignore[valid-type]  # noqa: UP006
            GenericAlias(collections.abc.Sequence, (typ,)),
            GenericAlias(list, (typ,)),
        )

    if list_base:
        result.extend(
            (seq_typ, f"{cpp_type}[]") for seq_typ in derived_seq_types(base_type)
        )
    if optional_base_list:
        result.extend(
            (seq_typ, f"{cpp_type}?[]")
            # pyrefly: ignore [not-a-type]
            for seq_typ in derived_seq_types(typing.Optional[base_type])  # noqa: UP045
        )
    if optional_list_base:
        result.extend(
            (typing.Optional[seq_typ], f"{cpp_type}[]?")  # noqa: UP045
            for seq_typ in derived_seq_types(base_type)
        )
    return result

