from typing import Any

def optimize(node: nodes.Node, environment: "Environment") -> nodes.Node:
    """The context hint can be used to perform an static optimization
    based on the context given."""
    optimizer = Optimizer(environment)
    return t.cast(nodes.Node, optimizer.visit(node))


def optimize(*args: Any, **kwargs: Any) -> OptimizeContext | _NullDecorator:
    def rebuild_ctx() -> OptimizeContext | _NullDecorator:
        ca_kwargs_override = config.compiled_autograd_kwargs_override
        if ca_kwargs_override:
            # NOTE: The process of translating other `torch.compile` kwargs to `torch._dynamo.optimize` kwargs
            # is more complicated, we will add it in the future when needed.
            assert set(ca_kwargs_override.keys()) == {"fullgraph"}, (
                f"Only `fullgraph` kwarg override is supported for now, but got {ca_kwargs_override.keys()}"
            )
            kwargs["nopython"] = ca_kwargs_override["fullgraph"]
        return optimize(*args, **kwargs)

    return _optimize(rebuild_ctx, *args, **kwargs)


def optimize(expr, optimizations):
    """ Apply optimizations to an expression.

    Parameters
    ==========

    expr : expression
    optimizations : iterable of ``Optimization`` instances
        The optimizations will be sorted with respect to ``priority`` (highest first).

    Examples
    ========

    >>> from sympy import log, Symbol
    >>> from sympy.codegen.rewriting import optims_c99, optimize
    >>> x = Symbol('x')
    >>> optimize(log(x+3)/log(2) + log(x**2 + 1), optims_c99)
    log1p(x**2) + log2(x + 3)

    """

    for optim in sorted(optimizations, key=lambda opt: opt.priority, reverse=True):
        new_expr = optim(expr)
        if optim.cost_function is None:
            expr = new_expr
        else:
            expr = optim.cheapest(expr, new_expr)
    return expr

