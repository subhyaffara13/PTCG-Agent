
def eager_debug(
    gm: torch.fx.GraphModule, fake_tensor_inputs: list[torch.Tensor], **kwargs: Any
) -> Callable[..., Any]:
    if kwargs:
        log.warning("eager_debug backend ignoring extra kwargs %s", kwargs)

    from torch._subclasses.schema_check_mode import SchemaCheckMode

    # We could add more debugging bits here.
    # Right now, this backend can be used to check for and error on
    # custom dispatcher ops that have incorrect schemas.
    def inner(*args: Any) -> Any:
        with SchemaCheckMode():
            return torch.fx.Interpreter(gm).run(*args)

    return inner

