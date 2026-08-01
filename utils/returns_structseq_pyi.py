
def returns_structseq_pyi(signature: PythonSignature) -> tuple[str, str] | None:
    python_returns = [return_type_str_pyi(r.type) for r in signature.returns.returns]
    structseq_name = signature.name
    field_names = structseq_fieldnames(signature.returns.returns)
    if field_names:
        # These types are structseq objects which act like named NamedTuples, but
        # the constructor acts like the constructor of tuple. Using typing.NamedTuple
        # does not allow us to override __init__.
        seq_type = f"tuple[{', '.join(python_returns)}]"
        structseq_def_lines = [
            f"class {structseq_name}({seq_type}):  # fmt: skip",
        ]
        for name, ret_type in zip(field_names, python_returns):
            structseq_def_lines.extend(
                [
                    "    @property",
                    f"    def {name}(self) -> {ret_type}: ...",
                ]
            )
        structseq_def_lines.extend(
            [
                "    def __new__(",
                "        cls,",
                f"        sequence: {seq_type},",
                "    ) -> Self:  # fmt: skip",
                "        ...",
                f"    n_fields: Final[_int] = {len(field_names)}",
                f"    n_sequence_fields: Final[_int] = {len(field_names)}",
                "    n_unnamed_fields: Final[_int] = 0",
                "    def __init_subclass__(cls) -> NoReturn: ...  # prohibit subclassing",
                "",  # add an extra newline
            ]
        )
        structseq_def = "\n".join(structseq_def_lines)
        # Example:
        # structseq_def = (
        #     "class max(tuple[Tensor, Tensor]):  # fmt: skip\n"
        #     "    @property\n"
        #     "    def values(self) -> Tensor: ...\n"
        #     "    @property\n"
        #     "    def indices(self) -> Tensor: ...\n"
        #     "    def __new__(\n"
        #     "        cls,\n"
        #     "        sequence: tuple[Tensor, Tensor],\n"
        #     "    ) -> Self:  # fmt: skip\n"
        #     "        ...\n"
        #     "    n_fields: Final[_int] = 2",
        #     "    n_sequence_fields: Final[_int] = 2",
        #     "    n_unnamed_fields: Final[_int] = 0",
        #     "    def __init_subclass__(cls) -> NoReturn: ...  # prohibit subclassing",
        # )
        return structseq_name, structseq_def
    return None

