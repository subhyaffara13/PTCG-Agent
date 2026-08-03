from typing import Callable

def assert_numerical_grads(f: Callable[..., Array],
                           f_args: Sequence[Array],
                           order: int,
                           atol: float = 0.01,
                           **check_kwargs) -> None:
  """Checks that autodiff and numerical gradients of a function match.

  Args:
    f: A function to check.
    f_args: Arguments of the function.
    order: An order of gradients.
    atol: An absolute tolerance.
    **check_kwargs: Kwargs for ``jax_test.check_grads``.

  Raises:
    AssertionError: If automatic differentiation gradients deviate from finite
      difference gradients.
  """
  # Correct scaling.
  # Remove after https://github.com/google/jax/issues/3130 is fixed.
  atol *= f_args[0].size

  # Mock `jax.lax.stop_gradient` because finite diff. method does not honour it.
  mock_sg = lambda t: jax.tree_util.tree_map(jnp.ones_like, t)
  with mock.patch("jax.lax.stop_gradient", mock_sg):
    jax_test.check_grads(f, f_args, order=order, atol=atol, **check_kwargs)

