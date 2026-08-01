
def dynamic_type(t: Type) -> str:
    if isinstance(t, OptionalType):
        return dynamic_type(t.elem)
    # Note we don't use t.is_tensor_like() here because it would
    # also include Tensor[]
    if str(t) == "Tensor":
        return "at::Tensor"
    # This is a legacy concept, so never report SymInt
    return cpp.argumenttype_type(
        t, mutable=False, binds="__placeholder__", symint=False
    ).cpp_type()

