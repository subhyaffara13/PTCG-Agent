
def batch_transform(
    transform: state_types.Transform, leading_rank: int
) -> state_types.Transform:
  match transform:
    case TransposeTransform() as t:
      return TransposeTransform(
          (*range(leading_rank), *(d + leading_rank for d in t.permutation))
      )
    case TilingTransform() | SwizzleTransform() as t:
      return t
    case _:
      raise NotImplementedError(f"Unsupported transform: {type(transform)}")

