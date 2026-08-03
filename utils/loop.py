from typing import Callable

def loop(
    loop_factory: Callable[[], asyncio.AbstractEventLoop],
    fast: bool,
    loop_debug: bool,
) -> Iterator[asyncio.AbstractEventLoop]:
    """Return an instance of the event loop."""
    with loop_context(loop_factory, fast=fast) as _loop:
        if loop_debug:
            _loop.set_debug(True)  # pragma: no cover
        asyncio.set_event_loop(_loop)
        yield _loop


def loop(
    lower: jax_typing.ArrayLike,
    upper: jax_typing.ArrayLike,
    *,
    init_carry: None = ...,
    step: jax_typing.ArrayLike = ...,
    unroll: int | bool | None = ...,
) -> Callable[[Callable[[jax_typing.Array], None]], None]:
  ...


def loop(
    lower: jax_typing.ArrayLike,
    upper: jax_typing.ArrayLike,
    *,
    init_carry: _T = ...,
    step: jax_typing.ArrayLike = ...,
    unroll: int | bool | None = ...,
) -> Callable[[Callable[[jax_typing.Array, _T], _T]], _T]:
  ...


def loop(
    lower: jax_typing.ArrayLike,
    upper: jax_typing.ArrayLike,
    *,
    init_carry: _T | None = None,
    step: jax_typing.ArrayLike = 1,
    unroll: int | bool | None = None,
) -> Callable[[Callable[..., _T | None]], _T | None]:
  """Returns a decorator that calls the decorated function in a loop."""
  zero: jax_typing.ArrayLike
  if not all(map(jax_core.is_concrete, (lower, upper, step))):
    idx_type = jnp.result_type(lower, upper, step)
    lower = lax.convert_element_type(lower, idx_type)
    upper = lax.convert_element_type(upper, idx_type)
    step = lax.convert_element_type(step, idx_type)
    zero = jnp.array(0, dtype=idx_type)
  else:
    # Preserve concrete bounds to allow loop unrolling.
    lower = cast(int, lower)
    upper = cast(int, upper)
    step = cast(int, step)
    zero = 0

  def decorator(body):
    if init_carry is None:
      body_fn = lambda idx, _: body(lower + idx * step)
    else:
      body_fn = lambda idx, carry: body(lower + idx * step, carry)
    return lax.fori_loop(
        zero,
        pl_utils.cdiv(upper - lower, step),
        body_fn,
        init_val=init_carry,
        unroll=unroll,
    )

  return decorator

