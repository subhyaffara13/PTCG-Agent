
def _dataclass_field_base_reduce(obj):
    return _get_dataclass_field_type_sentinel, (obj.name,)

