
def composite_name_format(
    write_name_format: NameFormat[Metadata],
    read_name_formats: Sequence[NameFormat[Metadata]],
) -> NameFormat[Metadata]:
  """Returns *composite* NameFormat supporting multiple read/single write formats.

  Args:
    write_name_format: NameFormat used to build step names meant for writing
      checkpoints. Must be present in `read_name_formats` at a preferred
      priority position.
    read_name_formats: Sequence (ordered) of NameFormats used to find steps for
      reading checkpoints. Please note that to resolve conflicts (and avoid
      raising errors) in case of multiple NameFormats matching a given step, the
      sequence should be provided in highest to lowest priority order:
      NameFormat appearing earlier in the sequence is preferred.
  """
  return _CompositeNameFormat(write_name_format, read_name_formats)


def composite_name_format(
    write_name_format: NameFormat[CheckpointMetadata[None]],
    read_name_formats: Sequence[NameFormat[CheckpointMetadata[None]]],
) -> NameFormat[CheckpointMetadata[None]]:
  """Returns *composite* NameFormat supporting multiple read/single write formats.

  Args:
    write_name_format: NameFormat used to build step names meant for writing
      checkpoints. Must be present in `read_name_formats` at a preferred
      priority position.
    read_name_formats: Sequence (ordered) of NameFormats used to find steps for
      reading checkpoints. Please note that to resolve conflicts (and avoid
      raising errors) in case of multiple NameFormats matching a given step, the
      sequence should be provided in highest to lowest priority order:
      NameFormat appearing earlier in the sequence is preferred.
  """
  return _CompositeNameFormat(write_name_format, read_name_formats)

