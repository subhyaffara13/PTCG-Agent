
def _should_lower(op: ir.OpView) -> bool:
  """Returns 'true' if the operation should be lowered."""
  return (
      # pyrefly: ignore[missing-attribute]
      op.OPERATION_NAME.startswith("mosaic_gpu.")
      or inference_utils.should_have_layout(op)
      or inference_utils.should_have_transforms(op)
      or inference_utils.should_have_tmem_layout(op)
      # Does it have subblocks?
      or any(bool(b) for r in op.regions for b in r)
  )

