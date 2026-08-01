
def should_allow_numbers_as_tensors(func: OpOverload) -> bool:
    return torch._C._should_allow_numbers_as_tensors(
        func.name().split("::")[-1].split(".")[0]
    )

