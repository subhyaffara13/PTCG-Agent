
def _repr_with_extra(self):
    fields = list(self.__dataclass_fields__.keys())
    other_fields = list(k for k in self.__dict__ if k not in fields)
    return f"{self.__class__.__name__}({', '.join(f'{k}={self.__dict__[k]!r}' for k in fields + other_fields)})"

