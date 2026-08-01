
def _load_dataclass(datacls: type[DataclassInstance], data: dict) -> DataclassInstance:
    """Load a dataclass instance from a dictionary.

    Fields not expected by the dataclass are ignored.
    """
    return datacls(**{k: v for k, v in data.items() if k in datacls.__dataclass_fields__})

