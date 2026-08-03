from typing import Any, Callable

def eval_polymorphic_shape(fun_jax: Callable,
               *,
               polymorphic_shapes=None) -> Callable:
  """Evaluates the output shape in presence of shape polymorphism.

  This is done without lowering or executing the function, same as for
  `jax.eval_shape`.

  Args:
    fun_jax: target JAX function to be called. Its arguments and return value
      should be JAX arrays, or nested standard Python containers
      (tuple/list/dict) thereof (pytrees).
    polymorphic_shapes: Specifies input shapes to be treated polymorphically
      during shape evaluation. See discussion for `jax2tf.convert`.

      .. warning:: The shape-polymorphic lowering is an experimental feature.

  Returns: a function that takes `jax.ShapeDtypeStruct`s (or any values
    with `.shape` and `.dtype` attributes) corresponding to the inputs for
    `fun_jax`, and returns a tuple with:

      * the jax.ShapeDtypeStruct corresponding to the result, as for
       `jax.eval_shape`. The shape may contain symbolic dimension expressions.
      * the value that can be passed to `polymorphic_shapes` for a subsequent
        call to `jax2tf.eval_polymorphic_shape`, or `jax2tf.convert`.

  For example:

  >>> import jax
  >>> from jax.experimental import jax2tf
  >>> from jax import numpy as jnp
  >>>
  >>> f = lambda A, x: jnp.sin(jnp.dot(A, x))
  >>> A = jax.ShapeDtypeStruct((2000, 3000), jnp.float32)
  >>> x = jax.ShapeDtypeStruct((3000, 1000), jnp.float32)
  >>> out_spec, out_poly_shape = jax2tf.eval_polymorphic_shape(f, polymorphic_shapes=["a, b", "b, c"])(A, x)
  >>> print(out_spec.shape)
  ("a", "c")
  >>> print(out_poly_shape)
  (a, c)
  >>> res_spec, res_poly_shape = jax2tf.eval_polymorphic_shape(lambda x: x.T, polymorphic_shapes=[out_poly_shape])(out_spec)
  >>> print(res_poly_shape)
  (c, a)
  """
  def do_eval_polymorphic_shape(*args_specs) -> Any:
    args_poly_specs = export.symbolic_args_specs(
        args_specs, polymorphic_shapes)
    res_poly_spec = jax.eval_shape(fun_jax, *args_poly_specs)
    # TODO(necula): For now we export the polymorphic shapes using `str`.
    res_polymorphic_shape = tree_util.tree_map(lambda r: str(r.shape), res_poly_spec)
    return res_poly_spec, res_polymorphic_shape

  return do_eval_polymorphic_shape

