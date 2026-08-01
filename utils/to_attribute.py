
def to_attribute(name, attr_string):
    attr_classes = (NominalAttribute, NumericAttribute, DateAttribute,
                    StringAttribute, RelationalAttribute)

    for cls in attr_classes:
        attr = cls.parse_attribute(name, attr_string)
        if attr is not None:
            return attr

    raise ParseArffError(f"unknown attribute {attr_string}")

