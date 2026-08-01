
def _determine_setters(
    frozen: bool, slots: bool, base_attr_map: dict[str, type]
):
    """
    Determine the correct setter functions based on whether a class is frozen
    and/or slotted.
    """
    if frozen is True:
        if slots is True:
            return (), _setattr, _setattr_with_converter

        # Dict frozen classes assign directly to __dict__.
        # But only if the attribute doesn't come from an ancestor slot
        # class.
        # Note _inst_dict will be used again below if cache_hash is True

        def fmt_setter(
            attr_name: str, value_var: str, has_on_setattr: bool
        ) -> str:
            if _is_slot_attr(attr_name, base_attr_map):
                return _setattr(attr_name, value_var, has_on_setattr)

            return f"_inst_dict['{attr_name}'] = {value_var}"

        def fmt_setter_with_converter(
            attr_name: str,
            value_var: str,
            has_on_setattr: bool,
            converter: Converter,
        ) -> str:
            if has_on_setattr or _is_slot_attr(attr_name, base_attr_map):
                return _setattr_with_converter(
                    attr_name, value_var, has_on_setattr, converter
                )

            return f"_inst_dict['{attr_name}'] = {converter._fmt_converter_call(attr_name, value_var)}"

        return (
            ("_inst_dict = self.__dict__",),
            fmt_setter,
            fmt_setter_with_converter,
        )

    # Not frozen -- we can just assign directly.
    return (), _assign, _assign_with_converter

