
def set_xla_metadata(x=None, **kwargs):
  if x is None:
    return XlaMetadataContextManager(kwargs)
  else:
    hashable_metadata = tuple(sorted(kwargs.items()))
    return tree_util.tree_map(
        lambda v: xla_metadata_value_p.bind(
            v, xla_metadata_kvs=hashable_metadata
        ),
        x,
    )

