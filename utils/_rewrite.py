
def _rewrite(fn: torch.nn.Module | Callable) -> torch.nn.Module | Callable:
    if isinstance(fn, torch.nn.Module):
        # Rewrite this module's `forward` as well as the `forward`s of
        # all of this module's recursive descendents. Return the new,
        # rewritten module hierarchy.
        def rewrite_module(m: torch.nn.Module):
            class RewrittenModule(torch.nn.Module):
                def __init__(self, orig):
                    super().__init__()
                    for k, v in orig.__dict__.items():
                        if isinstance(v, torch.nn.Module):
                            self.__dict__[k] = copy.copy(rewrite_module(v))
                        else:
                            self.__dict__[k] = copy.copy(v)

            RewrittenModule.forward = AST_Rewriter().rewrite(
                cast(FunctionType, m.forward)
            )
            return RewrittenModule(m)

        return rewrite_module(fn)
    else:
        # Rewrite this single free function
        return AST_Rewriter().rewrite(cast(FunctionType, fn))

