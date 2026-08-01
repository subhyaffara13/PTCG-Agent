
def convert_dataclass_transform_spec(self: DataclassTransformSpec) -> Json:
    return {
        "eq_default": self.eq_default,
        "order_default": self.order_default,
        "kw_only_default": self.kw_only_default,
        "frozen_default": self.frozen_default,
        "field_specifiers": list(self.field_specifiers),
    }

