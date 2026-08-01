
def _inject_property(module: Module, tensor_name: str) -> None:
    r"""Injects a property into module[tensor_name].

    It assumes that the class in the module has already been modified from its
    original one using _inject_new_class and that the tensor under :attr:`tensor_name`
    has already been moved out

    Args:
        module (nn.Module): module into which to inject the property
        tensor_name (str): name of the name of the property to create
    """
    # We check the precondition.
    # This should never fire if register_parametrization is correctly implemented
    if hasattr(module, tensor_name):
        raise AssertionError(f"Module already has an attribute named '{tensor_name}'")

    @torch.jit.unused
    def get_cached_parametrization(parametrization) -> Tensor:
        global _cache
        key = (id(module), tensor_name)
        tensor = _cache.get(key)
        if tensor is None:
            tensor = parametrization()
            _cache[key] = tensor
        return tensor

    def get_parametrized(self) -> Tensor:
        if torch.jit.is_scripting():
            raise RuntimeError("Parametrization is not working with scripting.")
        parametrization = self.parametrizations[tensor_name]
        # pyrefly: ignore [redundant-condition]
        if _cache_enabled:
            if torch.jit.is_scripting():
                # Scripting
                raise RuntimeError(
                    "Caching is not implemented for scripting. "
                    "Either disable caching or avoid scripting."
                )
            elif torch._C._get_tracing_state() is not None:
                # Tracing
                raise RuntimeError(
                    "Cannot trace a model while caching parametrizations."
                )
            else:
                return get_cached_parametrization(parametrization)
        else:
            # If caching is not active, this function just evaluates the parametrization
            return parametrization()

    def set_original(self, value: Tensor) -> None:
        if torch.jit.is_scripting():
            raise RuntimeError("Parametrization is not working with scripting.")
        self.parametrizations[tensor_name].right_inverse(value)

    setattr(module.__class__, tensor_name, property(get_parametrized, set_original))

