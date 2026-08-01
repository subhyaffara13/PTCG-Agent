
def synthesize__repr__(cls) -> ParsedDef:
    return compose_fn(
        cls,
        "__repr__",
        [
            f"return '{cls.__name__}("
            + ", ".join(
                [
                    f"{field.name}=self.{field.name}"
                    for field in dataclasses.fields(cls)
                    if field.repr
                ]
            )
            + ")'"
        ],
        signature="(self) -> str",
    )

