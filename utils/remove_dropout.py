from typing import Any

def remove_dropout(model: nn.Module) -> nn.Module:
    """
    Removes all dropout layers from the module.
    """
    fx_model = fx.symbolic_trace(model)

    class DropoutRemover(torch.fx.Transformer):
        def call_module(
            self, target: Target, args: tuple[Argument, ...], kwargs: dict[str, Any]
        ) -> Any:
            if isinstance(self.submodules[target], nn.Dropout):
                if len(args) != 1:
                    raise AssertionError(f"Expected 1 arg for Dropout, got {len(args)}")
                return args[0]
            else:
                return super().call_module(target, args, kwargs)

    return DropoutRemover(fx_model).transform()

