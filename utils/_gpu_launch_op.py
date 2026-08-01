
def _gpu_launch_op(module: ir.Module) -> gpu.LaunchOp:
  for op in module.body.operations:
    for region in op.operation.regions:
      for block in region.blocks:
        for sub_op in block.operations:
          if isinstance(sub_op, gpu.LaunchOp):
            return sub_op
  raise ValueError("gpu.launch op not found.")

