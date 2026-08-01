
def check_empty_containers(obj) -> None:
    if obj == [] or obj == {} or obj == ():
        warnings.warn(
            "The inner type of a container is lost when "
            "calling torch.jit.isinstance in eager mode. For "
            "example, List[int] would become list and "
            "therefore falsely return True for List[float] or"
            " List[str].",
            stacklevel=2,
        )

