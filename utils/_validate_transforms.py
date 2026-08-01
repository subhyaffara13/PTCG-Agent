
def _validate_transforms(transforms):
  for transform in transforms:
    match transform:
      case indexing.NDIndexer():
        if _is_dynamic(transform):
          raise ValueError(
              "Dynamic indexing not supported in GPU interpret mode"
          )
      case _:
        raise ValueError(f"Unsupported transform: {transform}")

