
def build_step_metadatas(
    step_paths: Iterable[epath.Path],
    build_metadata: Callable[[epath.Path], Optional[MetadataT]],
) -> Iterator[MetadataT]:
  """Yields filtered metadata mapped with `step_paths`.

  Args:
    step_paths: Iterator of step paths.
    build_metadata: Callable to match and build step metadata from `step_paths`
      elements. If a `step_paths` element doesn't match then it returns None.

  Yields:
    Step metadata.
  """
  with futures.ThreadPoolExecutor() as executor:
    metadata_futures = [
        executor.submit(build_metadata, step_path) for step_path in step_paths
    ]
    for future in futures.as_completed(metadata_futures):
      metadata = future.result()
      if metadata is not None:
        yield metadata

