
def to_gpu_transform(
    transform: state_types.Transform,
) -> mgpu.MemRefTransform:
  match transform:
    case TransposeTransform(permutation):
      return mgpu.TransposeTransform(permutation)
    case TilingTransform(tiling):
      return mgpu.TileTransform(tiling)
    case _:
      raise TypeError(f"Unsupported transform: {type(transform)}")

