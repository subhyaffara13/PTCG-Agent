
def context_add_strides(context: AHContext, name: str, stride: tuple[int, ...]) -> None:
    for i, s in enumerate(stride):
        context.add_feature(f"{name}_stride_{i}", s)

