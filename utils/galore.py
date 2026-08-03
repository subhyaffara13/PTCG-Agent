from typing import Any, Callable, Optional, Union

def galore(
    learning_rate: base.ScalarOrSchedule,
    rank: int = 128,
    update_proj_gap: int = 200,
    scale: float = 1.0,
    base_optimizer: Optional[base.GradientTransformation] = None,
    weight_decay: jax.typing.ArrayLike = 0.0,
    mask: Optional[Union[Any, Callable[[base.Params], Any]]] = None,
    weight_dimension_numbers: Optional[GaLoreDimNumsOrFn] = None,
) -> base.GradientTransformation:
  r"""GaLore: Memory-efficient training via gradient lowrank projection.

  GaLore (Gradient Low-Rank Projection) is a memory-efficient training strategy
  that enables full-parameter learning while reducing optimizer state memory by
  projecting gradients into a low-rank subspace.

  The key insight is that gradients of weight matrices in neural networks often
  exhibit low-rank structure. GaLore exploits this by:

  1. Computing a low-rank projection matrix P using SVD of the gradient
  2. Projecting gradients to a low-rank subspace: R = P^T @ G (or G @ P)
  3. Maintaining optimizer states in the reduced subspace
  4. Projecting updates back to full space: update = P @ normalized_R

  For a weight matrix of shape (m, n) with rank r projection:

  - Standard Adam stores m + v states: 2 * m * n parameters
  - GaLore stores: 2 * min(r*n, m*r) + projection matrix

  This can achieve up to 65% memory reduction for large linear layers.

  .. note::
    GaLore only projects 2D weight matrices by default. Use
    ``weight_dimension_numbers`` to project higher-dimensional tensors
    (like attention projections stored as 3D arrays).

  .. warning::
    The ``base_optimizer`` must be a **gradient scaling transformation** that
    does NOT require parameter values. See ``scale_by_galore`` for details on
    compatible vs incompatible optimizers.

    **Do NOT use**: ``adamw``, ``lamb``, ``lars`` as base_optimizer.

    **Use instead**: ``scale_by_adam``, ``scale_by_lion``, etc., and configure
    weight decay via the ``weight_decay`` parameter of this function.

  Examples:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(jnp.square(x['w']))
    >>> solver = optax.contrib.galore(learning_rate=0.01, rank=16)
    >>> params = {'w': jnp.ones((100, 100)), 'b': jnp.ones((100,))}
    >>> print('Objective function: ', f(params))
    Objective function:  10000.0
    >>> opt_state = solver.init(params)
    >>> for _ in range(5):
    ...  grad = jax.grad(f)(params)
    ...  updates, opt_state = solver.update(grad, opt_state, params)
    ...  params = optax.apply_updates(params, updates)
    ...  print('Objective function: {:.2E}'.format(f(params)))
    Objective function: 9.98E+03
    Objective function: 9.96E+03
    Objective function: 9.94E+03
    Objective function: 9.92E+03
    Objective function: 9.90E+03

  Using weight decay (equivalent to AdamW behavior):
    >>> solver = optax.contrib.galore(
    ...     learning_rate=0.01,
    ...     rank=16,
    ...     weight_decay=0.01,  # Use this, NOT adamw as base_optimizer
    ... )

  Using a custom base optimizer:
    >>> solver = optax.contrib.galore(
    ...     learning_rate=0.01,
    ...     rank=16,
    ...     base_optimizer=optax.scale_by_adam(b1=0.9, b2=0.99),
    ... )

  Projecting 3D attention weights as 2D matrices:
    >>> from optax.contrib import GaLoreDimensionNumbers
    >>> # For attention weights shaped (embed_dim, num_heads, head_dim)
    >>> dim_nums = {'attn': GaLoreDimensionNumbers(
    ...     reduction_axis=0,      # embed_dim
    ...     output_axis=(1, 2),    # heads*head_dim
    ... )}
    >>> solver = optax.contrib.galore(
    ...     learning_rate=0.01, rank=16, weight_dimension_numbers=dim_nums
    ... )

  Args:
    learning_rate: A global scaling factor, either fixed or evolving along
      iterations with a scheduler.
    rank: Target rank for the low-rank projection. Lower values save more
      memory but may slow convergence. Default 128 is a good starting point.
    update_proj_gap: Number of steps between projection matrix updates.
      The projectors are recomputed from the gradient SVD every this many
      steps to adapt to the changing gradient landscape.
    scale: Additional scaling factor for updates.
    base_optimizer: The base gradient transformation to apply in the low-rank
      subspace. Must be a gradient-only transformation like ``scale_by_adam``,
      NOT an optimizer requiring params like ``adamw``. If None, defaults to
      ``optax.scale_by_adam()``. If the base optimizer includes a learning
      rate, set ``learning_rate=1.0`` here to avoid double-scaling.
    weight_decay: Strength of decoupled weight decay regularization (as in
      AdamW). This is applied correctly in full parameter space, unlike
      weight decay in the base optimizer which would fail.
    mask: A tree with same structure as params PyTree, or a Callable that
      returns such a pytree. Leaves should be booleans indicating whether
      to apply weight decay to each parameter.
    weight_dimension_numbers: Specifies how to treat non-2D tensors as 2D
      matrices for projection. See ``scale_by_galore`` for details.

  Returns:
    A GradientTransformation implementing the GaLore optimizer.

  References:
    Zhao et al., `GaLore: Memory-Efficient LLM Training by Gradient Low-Rank
    Projection <https://arxiv.org/abs/2403.03507>`_, 2024
  """
  return combine.chain(
      scale_by_galore(
          rank=rank,
          update_proj_gap=update_proj_gap,
          scale=scale,
          base_optimizer=base_optimizer,
          weight_dimension_numbers=weight_dimension_numbers,
      ),
      transform.add_decayed_weights(weight_decay, mask),
      transform.scale_by_learning_rate(learning_rate),
  )

