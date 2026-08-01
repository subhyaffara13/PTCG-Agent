
def build_default_tree_metadata(
    tree: PyTree,
    *,
    custom_metadata: PyTree | None = None,
    use_zarr3: bool = False,
) -> TreeMetadata:
  """Builds the TreeMetadata using a default implementation."""
  return _TreeMetadataImpl.build(
      tree,
      custom_metadata=custom_metadata,
      use_zarr3=use_zarr3,
  )

