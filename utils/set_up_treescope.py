
def set_up_treescope():
  """Sets up treescope to render JAX objects."""
  if jax is None:
    raise RuntimeError(
        "Cannot set up JAX support in treescope: JAX cannot be imported."
    )
  type_registries.TREESCOPE_HANDLER_REGISTRY[jax.ShapeDtypeStruct] = (
      make_checked_dataclasslike_renderer(
          jax.ShapeDtypeStruct,
          fields=("shape", "dtype"),
          fields_with_none_default=("sharding",),
      )
  )
  type_registries.TREESCOPE_HANDLER_REGISTRY[jax.tree_util.SequenceKey] = (
      make_checked_dataclasslike_renderer(
          jax.tree_util.SequenceKey, fields=("idx",)
      )
  )
  type_registries.TREESCOPE_HANDLER_REGISTRY[jax.tree_util.DictKey] = (
      make_checked_dataclasslike_renderer(
          jax.tree_util.DictKey, fields=("key",)
      )
  )
  type_registries.TREESCOPE_HANDLER_REGISTRY[jax.tree_util.GetAttrKey] = (
      make_checked_dataclasslike_renderer(
          jax.tree_util.GetAttrKey, fields=("name",)
      )
  )
  type_registries.TREESCOPE_HANDLER_REGISTRY[
      jax.tree_util.FlattenedIndexKey
  ] = make_checked_dataclasslike_renderer(
      jax.tree_util.FlattenedIndexKey, fields=("key",)
  )
  type_registries.TREESCOPE_HANDLER_REGISTRY[jax.lax.Precision] = (
      render_precision
  )

  # The concrete type of a JAX array is a private type that is dynamically
  # registered as a jax.Array subclass, so we need to add it to the list of
  # dynamically-checked virtual base classes.
  type_registries.VIRTUAL_BASE_CLASSES.append(jax.Array)
  type_registries.IMMUTABLE_TYPES_REGISTRY[jax.Array] = True
  type_registries.NDARRAY_ADAPTER_REGISTRY[jax.Array] = JAXArrayAdapter()
  type_registries.TREESCOPE_HANDLER_REGISTRY[jax.Array] = render_jax_arrays

  for jax_api_module in [
      jax.lax,
      jax.numpy,
      jax.scipy,
      jax.random,
      jax.nn,
      jax.custom_derivatives,
      jax,
  ]:
    canonical_aliases.populate_from_public_api(
        jax_api_module, canonical_aliases.prefix_filter("jax")
    )

  for key_cls_name in [
      "SequenceKey",
      "DictKey",
      "GetAttrKey",
      "FlattenedIndexKey",
  ]:
    canonical_aliases.add_alias(
        getattr(jax.tree_util, key_cls_name),
        canonical_aliases.ModuleAttributePath("jax.tree_util", (key_cls_name,)),
        on_conflict="ignore",
    )


def set_up_treescope():
  """Sets up treescope to render Numpy objects."""
  type_registries.NDARRAY_ADAPTER_REGISTRY[np.ndarray] = NumpyArrayAdapter()
  type_registries.TREESCOPE_HANDLER_REGISTRY[np.ndarray] = render_ndarrays
  type_registries.TREESCOPE_HANDLER_REGISTRY[np.dtype] = render_dtype_instances

  with warnings.catch_warnings():
    # This warning is triggered by walking the numpy API, but we are not
    # actually accessing anything under numpy.core while building aliases, so it
    # is safe to ignore temporarily.
    warnings.filterwarnings(
        "ignore",
        category=DeprecationWarning,
        module="treescope.canonical_aliases",
        message=re.escape(
            "numpy.core is deprecated and has been renamed to numpy._core."
        ),
    )
    canonical_aliases.populate_from_public_api(
        np, canonical_aliases.prefix_filter("numpy", excludes=("numpy.core",))
    )


def set_up_treescope():
  """Sets up treescope to render PyTorch objects."""
  if torch is None:
    raise RuntimeError(
        "Cannot set up PyTorch support in treescope: PyTorch cannot be"
        " imported."
    )
  type_registries.NDARRAY_ADAPTER_REGISTRY[torch.Tensor] = TorchTensorAdapter()
  type_registries.TREESCOPE_HANDLER_REGISTRY[torch.Tensor] = (
      render_torch_tensors
  )
  type_registries.TREESCOPE_HANDLER_REGISTRY[torch.nn.Module] = (
      render_torch_modules
  )

