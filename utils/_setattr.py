
def _setattr(attr_name: str, value_var: str, has_on_setattr: bool) -> str:
    """
    Use the cached object.setattr to set *attr_name* to *value_var*.
    """
    return f"_setattr('{attr_name}', {value_var})"


def _setattr(
    obj: _Dataclass,
    attribute_name: str,
    value: _In,
) -> None:
  """Set the `obj.attribute_name = value`."""
  # Note: In `dataclasses.dataclass(frozen=True)`, obj.__setattr__ will
  # correctly raise a `FrozenInstanceError` before `DataclassField.__set__` is
  # called.
  _init_dataclass_state(obj)
  # fmt: off
  obj._dataclass_field_values[attribute_name] = value  # pylint: disable=protected-access

