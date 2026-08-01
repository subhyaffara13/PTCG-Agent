
def latest_step_metadata(
    root_path: epath.PathLike, name_format: NameFormat[MetadataT]
) -> Optional[MetadataT]:
  """Returns step.MetadataT of the latest step in `root_path`."""
  return max(
      sorted(
          name_format.find_all(root_path),
          key=lambda metadata: metadata.path.name,
          reverse=True,
      ),
      default=None,
      key=lambda metadata: metadata.step,
  )

