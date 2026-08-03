import functools
from typing import Any, Callable

def leaf_function(fn: Callable[_P, _R]) -> Callable[_P, _R]: ...


def leaf_function(
    *, mutates_args: set[str]
) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]: ...


def leaf_function(
    fn: Callable[_P, _R] | None = None, *, mutates_args: set[str] | None = None
) -> Callable[_P, _R] | Callable[[Callable[_P, _R]], Callable[_P, _R]]:
    """
    Decorator to mark a function as a leaf function for :func:`torch.compile`.

    A leaf function appears as an opaque operation in the compiled graph. During
    compilation, Dynamo and AOT autograd do not trace into it. At runtime, the
    original eager Python code is executed directly.

    Quick Start:
        Suppose we want to log per-sample statistics during the forward pass::

            def compute_and_log_stats(x):
                stats = x.mean(dim=1)
                logger.info(f"Per-sample means: {stats}")
                return (stats,)

        With ``torch.compile(..., fullgraph=True)``, this fails because
        ``logger.info`` causes a graph break. To fix it, follow the steps below:

        1. Decorate your function with ``@leaf_function``
        2. Define a shape-inference function using ``@your_fn.register_fake``

        Concrete implementation::

            >>> import logging
            >>> import torch
            >>> from torch._dynamo.decorators import leaf_function
            >>>
            >>> logging.basicConfig(level=logging.INFO)
            >>> logger = logging.getLogger(__name__)
            >>>
            >>> @leaf_function
            ... def compute_and_log_stats(x):
            ...     stats = x.mean(dim=1)  # Shape: (x.shape[0],)
            ...     logger.info(f"Per-sample means: {stats}")
            ...     return (stats,)
            ...
            >>> @compute_and_log_stats.register_fake
            ... def compute_and_log_stats_fake(x):
            ...     # Match the output shape: (x.shape[0],)
            ...     return (x.new_empty(x.shape[0]),)
            ...
            >>> def fn(x):
            ...     return compute_and_log_stats(x)
            ...
            >>> x = torch.randn(3, 4)
            >>> compiled_fn = torch.compile(fn, backend="aot_eager", fullgraph=True)
            >>> out = compiled_fn(x)[0]

    When to Use:
        Use ``leaf_function`` when you need eager execution semantics that tracing
        cannot preserve:

        - **Non-traceable code**: The function consists of code that Dynamo or
          AOT Autograd cannot trace.
        - **Runtime side effects**: Operations that must happen exactly once per call
          at runtime (e.g., logging, external library calls).

        If your function has a static computation graph and no runtime side effects,
        prefer :func:`allow_in_graph` or :func:`nonstrict_trace` instead. They allow AOT autograd
        to trace through and potentially optimize the code.

    Usage:
        **Inputs and Outputs**:
        - Both inputs and outputs must use pytree-compatible types.
        Tensors, Python primitives (int, float, bool, str), and built-in containers
        (list, tuple, dict) are supported by default.

        Note: We recommend leaf_functions only accept and return tensors. Though primitive
        types (int, float, bool, str) are supported in inputs and outputs, they may cause
        surprising behavior: primitive inputs are guarded and may trigger recompilation,
        while primitive output values are captured from the fake implementation at compile time and
        remain fixed for all subsequent executions. Even though the real function runs
        at runtime, its primitive return values are silently replaced with the compile-time
        values from the fake implementation.

        Example::

            # BAD: primitive output varies at runtime
            counter = 0


            @leaf_function
            def count_calls(x):
                global counter
                counter += 1
                return (x, counter)


            @count_calls.register_fake
            def count_calls_fake(x):
                return (x, 999)  # placeholder value


            # At runtime: real function runs (counter increments to 1, 2, 3, ...)
            # But returned count is always 999 (from fake implementation at compile time)

        - User-defined classes must be registered via :func:`torch.utils._pytree.register_pytree_node`
        or :func:`torch.utils._pytree.register_dataclass`.

        - :class:`torch.nn.Module` can also be passed as input; its parameters and buffers
        are tracked for autograd. The module must exist outside the compile region.
        Running the module multiple times must not modify its parameters, buffers, or attributes.

        **register_fake (required)**:
        Since the function body is not traced, you must
        provide a shape-inference function via ``@fn.register_fake``. It runs at compile
        time with FakeTensor inputs (tensors with no data, only metadata) and must
        satisfy the following requirements:

        - Must have the same input and output signature (e.g., same pytree structure, same tensor metadata
          such as shapes, dtypes, device, strides) as the real function
        - Must be runnable with FakeTensor inputs
        - Must only use its explicit arguments (no closures over tensors or modules)

        Note: The input and output signature must be determinable at compile time.
        If your function's output structure depends on runtime values, adjust the leaf function
        boundary until outputs become predictable.

        To validate that your fake implementation matches the real function's outputs, set
        ``torch._dynamo.config.leaf_function_validate_outputs = True``.

    Limitations:
        Currently, inductor backend and :func:`torch.export.export` are not yet supported.

    Training / Autograd:
        Training is supported automatically if your leaf function is differentiable
        in eager mode (e.g., it's implemented with PyTorch ops, :class:`torch.autograd.Function`,
        or differentiable custom ops).

        **Restriction**: Calling ``.backward()`` *inside* the leaf function is not
        supported.

        **Escaped gradients check**: If the leaf function closes over a tensor with
        ``requires_grad=True``, gradients will not flow back to it (only explicit inputs
        receive gradients). To detect such cases, set
        ``torch._dynamo.config.leaf_function_check_escaped_gradients = True``.
        When enabled, a ``RuntimeError`` is raised with details about the escaped tensors.

        Internally, inputs and outputs are detached from the outer autograd graph at the
        leaf function boundary. The leaf function builds its own local autograd
        graph. In backward, gradients propagate through this local graph to the
        leaf function's inputs. If a :class:`torch.nn.Module` is passed in as input, the gradients
        will also flow back to its parameters and buffers.

    How leaf_function Works:
        Understanding this helps avoid pitfalls:

        1. **Compilation**: Dynamo and AOT autograd do not trace into the leaf function.
           Only your fake implementation runs during compilation to determine output signatures,
           shapes, and dtypes. The real function runs at runtime as eager Python.

        2. **Isolation**: Mutations to shared state (globals, closures) may not be
           visible across the boundary between leaf functions and compiled regions. Pass data
           explicitly as function arguments and return results as outputs.

    Dangerous Patterns:
        These patterns may cause silent incorrectness or errors:

        - **Side effects between leaf functions and compiled regions**: Mutations to
          Python state inside a leaf function may not be visible to the compiled
          region, and vice versa. The compiled graph may reorder or eliminate
          operations in ways that break assumptions about side effect ordering.

          Bad::

            # Compiled region
            self.counter += 1
            y = my_leaf_fn(self, x)  # Don't depend on self.counter inside leaf_fn

            y = my_leaf_fn(self, x)
            result = self.state  # Don't depend on state mutated by leaf_fn

          Logging/printing inside the leaf function is fine since it doesn't affect
          correctness.

        - **In-place mutations on inputs**: Undeclared in-place mutations on input
          tensors are detected and will raise an error. Either declare mutations via
          ``mutates_args`` or clone inputs before mutating.

          Bad::

            @leaf_function
            def my_leaf_fn(x):
                x.add_(1)  # Will raise: "Undeclared in-place mutation"
                return (x,)

          Good::

            @leaf_function(mutates_args={"buf"})
            def my_leaf_fn(x, buf):
                buf.add_(1)  # OK: declared in mutates_args
                return (x + buf,)

          For pytree args (lists, tuples, dicts of tensors), use the parameter name
          to declare mutation on all contained tensors::

            @leaf_function(mutates_args={"buffers"})
            def my_leaf_fn(x, buffers):
                for buf in buffers:
                    buf.add_(1)  # OK: 'buffers' declared in mutates_args
                return (x + sum(buffers),)

          Or use bracket notation for fine-grained control::

            @leaf_function(mutates_args={"buffers[0]"})
            def my_leaf_fn(x, buffers):
                buffers[0].add_(1)  # OK: 'buffers[0]' declared
                return (x + buffers[1],)  # buffers[1] is not cloned

        - **Closures in fake implementation**: Tensors or modules captured from enclosing scopes
          in the fake implementation will cause compilation errors. The real function can
          close over them if they don't require gradient, but the fake implementation must
          only use its arguments.

          Bad::

            weight = torch.randn(3, 3)


            @leaf_function
            def my_leaf_fn(x):
                return (x @ weight,)


            @my_leaf_fn.register_fake
            def my_leaf_fn_fake(x):
                return (x @ weight,)  # Error: weight used in fake implementation

          Good::

            weight = torch.randn(3, 3)


            @leaf_function
            def my_leaf_fn(x):
                return (x @ weight,)  # OK: real function can use closure


            @my_leaf_fn.register_fake
            def my_leaf_fn_fake(x):
                return (x @ torch.empty_like(x),)  # OK: uses only args

    Example::
        Wrapping a linear function with logging as a leaf_function. Gradients
        flow back because the inner operations are differentiable::

            >>> import torch
            >>> import torch.nn.functional as F
            >>> from torch._dynamo.decorators import leaf_function
            >>>
            >>> @leaf_function
            ... def custom_forward(linear, x):
            ...     # Logging at runtime
            ...     print(f"Input: shape={x.shape}, mean={x.mean().item():.4f}")
            ...     out = F.linear(x, linear.weight, linear.bias)
            ...     print(f"Output: shape={out.shape}, norm={out.norm().item():.4f}")
            ...     return (out,)
            ...
            >>> @custom_forward.register_fake
            ... def custom_forward_fake(linear, x):
            ...     # Return tensor with correct shape: (batch, out_features)
            ...     return (x.new_empty(x.shape[0], linear.weight.shape[0]),)
            ...
            >>> class MyModel(torch.nn.Module):
            ...     def __init__(self):
            ...         super().__init__()
            ...         self.linear = torch.nn.Linear(10, 20)
            ...     def forward(self, x):
            ...         return custom_forward(self.linear, x)
            ...
            >>> model = MyModel()
            >>> compiled = torch.compile(model, backend="aot_eager", fullgraph=True)
            >>> x = torch.randn(32, 10, requires_grad=True)
            >>> out = compiled(x)[0]
            >>> out.sum().backward()  # Gradients flow to model.linear.weight/bias and x

    Args:
        fn: The function being decorated.
        mutates_args: Set of Python expressions (as strings) identifying arguments
            that the function mutates in-place. Each string is evaluated against
            the function's parameters. Examples: ``'buf'`` for a plain tensor,
            ``'model.running_mean'`` for an nn.Module buffer,
            ``'buffers'`` to mark all tensors in a list, ``'buffers[0]'`` for a
            specific element, ``'state["key"]'`` for a dict entry.
    """
    if fn is None:
        return functools.partial(leaf_function, mutates_args=mutates_args)

    from . import trace_rules

    _check_mutually_exclusive_decorators(fn, "leaf_function")

    if mutates_args:
        import inspect
        import re

        params = set(inspect.signature(fn).parameters)
        for expr in mutates_args:
            root = re.split(r"[.\[]", expr, maxsplit=1)[0]
            if root not in params:
                raise ValueError(
                    f"mutates_args expression '{expr}' refers to parameter '{root}', "
                    f"which is not a parameter of '{fn.__name__}'. "
                    f"Available parameters: {', '.join(params)}"
                )

    @functools.wraps(fn)
    def inner(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        if inner._torchdynamo_leaf_fake_fn is None:  # type: ignore[attr-defined]
            raise ValueError(
                f"leaf_function '{getattr(fn, '__name__', fn)}' "
                "requires a fake implementation. Please provide one using the @<func>.register_fake "
                "decorator. See the leaf_function docstring for details."
            )

        return _invoke_leaf_function_python(
            fn,  # pyrefly: ignore [bad-argument-type]
            # pyrefly: ignore [bad-argument-type]
            inner._torchdynamo_leaf_fake_fn,
            args,
            kwargs,
            mutates_args=inner._torchdynamo_leaf_mutates_args,  # pyrefly: ignore [missing-attribute]
        )  # type: ignore[attr-defined]

    inner._torchdynamo_leaf_real_fn = fn  # type: ignore[attr-defined]
    inner._torchdynamo_leaf_fake_fn = None  # type: ignore[attr-defined]
    inner._torchdynamo_leaf_mutates_args = (  # pyrefly: ignore [missing-attribute]
        frozenset(mutates_args) if mutates_args else frozenset()
    )  # type: ignore[attr-defined]

    # Follow nonstrict_trace implementation
    wrapped_id = id(inner)
    trace_rules._allowed_callable_ids.add(wrapped_id)
    trace_rules._leaf_function_ids.add(wrapped_id)

    def deregister() -> None:
        trace_rules._allowed_callable_ids.remove(wrapped_id)
        trace_rules._leaf_function_ids.remove(wrapped_id)

    weakref.finalize(inner, deregister)

    def register_fake_setter(fake_fn: Callable[..., Any]) -> Callable[..., Any]:
        inner._torchdynamo_leaf_fake_fn = fake_fn  # type: ignore[attr-defined]
        return inner

    inner.register_fake = register_fake_setter  # type: ignore[attr-defined]

    return inner

