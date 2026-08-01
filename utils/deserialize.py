
def deserialize(
    artifact: SerializedArtifact,
    expected_opset_version: dict[str, int] | None = None,
    *,
    _unsafe_skip_version_check=False,
) -> ep.ExportedProgram:
    if not isinstance(artifact.exported_program, bytes):
        raise AssertionError(
            f"expected bytes, got {type(artifact.exported_program).__name__}"
        )
    serialized_exported_program = _bytes_to_dataclass(
        ExportedProgram, artifact.exported_program
    )
    return ExportedProgramDeserializer(expected_opset_version).deserialize(
        serialized_exported_program,
        artifact.state_dict,
        artifact.constants,
        artifact.example_inputs,
        _unsafe_skip_version_check=_unsafe_skip_version_check,
    )


def deserialize(binary_data, tensor_table):
    return _internal_rpc_pickler.deserialize(binary_data, tensor_table)


def deserialize(metadata_dict: SerializedMetadata) -> RootMetadata:
  """Deserializes `metadata_dict` to `RootMetadata`."""
  return InternalRootMetadata.deserialize(metadata_dict).to_root_metadata()


def deserialize(
    metadata_dict: SerializedMetadata,
    item_metadata: CompositeItemMetadata | SingleItemMetadata | None = None,
    metrics: dict[str, Any] | None = None,
) -> StepMetadata:
  """Deserializes `metadata_dict` and other kwargs to `InternalCheckpointMetadata`."""
  return InternalCheckpointMetadata.deserialize(metadata_dict).to_step_metadata(
      item_metadata=item_metadata, additional_metrics=metrics
  )


def deserialize(ser: bytearray) -> _export.Exported:
  """Deserializes an Exported.

  The serialized bytearray must be trusted input. If you deserialized it, when
  you execute it, it may execute any custom call registered in the jaxlib.
  """
  exp = ser_flatbuf.Exported.GetRootAsExported(ser)
  return _deserialize_exported(exp)


def deserialize(blob: bytearray) -> Exported:
  """Deserializes an Exported.

  Args:
    blob: a bytearray obtained from :meth:`jax.export.Exported.serialize`.
  """
  # Lazy load the serialization module, since flatbuffers is an optional
  # dependency.
  from jax._src.export.serialization import deserialize
  return deserialize(blob)

