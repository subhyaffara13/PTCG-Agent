
def _get_impl_save_args(
    item: Optional[PyTree] = None,
    save_args: Optional[PyTreeSaveArgs] = None,
    args: Optional[PyTreeSaveArgs] = None,
) -> BasePyTreeSaveArgs:
  """Construct BasePyTreeSaveArgs."""
  if isinstance(item, CheckpointArgs):
    raise ValueError(
        'Make sure to specify kwarg name `args=` when providing'
        ' `PyTreeSaveArgs`.'
    )
  if args is None:
    args = PyTreeSaveArgs(
        item=item,
        save_args=save_args,
    )
  return BasePyTreeSaveArgs(
      item=args.item,
      save_args=args.save_args,
      ocdbt_target_data_file_size=args.ocdbt_target_data_file_size,
      custom_metadata=args.custom_metadata,
  )

