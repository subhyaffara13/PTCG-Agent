
def serialize(node, stream=None, Dumper=Dumper, **kwds):
    """
    Serialize a representation tree into a YAML stream.
    If stream is None, return the produced string instead.
    """
    return serialize_all([node], stream, Dumper=Dumper, **kwds)


def serialize(
    exported_program: ep.ExportedProgram,
    opset_version: dict[str, int] | None = None,
    pickle_protocol: int = DEFAULT_PICKLE_PROTOCOL,
    *,
    serialize_state_dict: bool = True,
    serialize_constants: bool = True,
    serialize_example_inputs: bool = True,
) -> SerializedArtifact:
    with _enable_graph_inputs_of_type_nn_module(exported_program.example_inputs):
        serialized_program = ExportedProgramSerializer(
            opset_version, pickle_protocol
        ).serialize(
            exported_program,
            serialize_state_dict=serialize_state_dict,
            serialize_constants=serialize_constants,
            serialize_example_inputs=serialize_example_inputs,
        )
    if not isinstance(serialized_program.exported_program, ExportedProgram):
        raise AssertionError(
            f"expected ExportedProgram, got {type(serialized_program.exported_program).__name__}"
        )

    json_bytes = _to_json_bytes(serialized_program.exported_program)
    artifact = SerializedArtifact(
        json_bytes,
        serialized_program.state_dict,
        serialized_program.constants,
        serialized_program.example_inputs,
    )
    return artifact


def serialize(obj):
    return _internal_rpc_pickler.serialize(obj)


def serialize(metadata: RootMetadata) -> SerializedMetadata:
  """Serializes `metadata` to a dictionary."""
  return InternalRootMetadata.from_root_metadata(metadata).serialize()


def serialize(metadata: StepMetadata) -> SerializedMetadata:
  """Serializes `metadata` to a dictionary."""
  metadata = InternalCheckpointMetadata.from_step_metadata(metadata)
  return metadata.serialize()


def serialize(compiled: jax.stages.Compiled):
  """Serializes a compiled binary.

  Because pytrees are not serializable, they are returned so that
  the user can handle them properly.
  """
  unloaded_executable = getattr(compiled._executable,
                                '_unloaded_executable', None)
  if unloaded_executable is None:
    raise ValueError("Compilation does not support serialization")
  if getattr(unloaded_executable, 'mut', None) and unloaded_executable.mut.in_mut:
    raise ValueError("can't serialize with a closed-over mutable array ref")
  args_info_flat, in_tree = jax.tree_util.tree_flatten(compiled.args_info)
  # TODO(necula): deal with constants in serialized executables
  if compiled._params.const_args:
    raise NotImplementedError("serialize_executables with const_args")
  with io.BytesIO() as file:
    _JaxPjrtPickler(file).dump(
        (unloaded_executable, args_info_flat, compiled._no_kwargs))
    return file.getvalue(), in_tree, compiled.out_tree


def serialize(exp: _export.Exported, vjp_order: int = 0) -> bytearray:
  """Serializes an Exported.

  Args:
    exp: the Exported to serialize.
    vjp_order: The maximum vjp order to include. E.g., the value 2 means that we
      serialize the primal functions and two orders of the `vjp` function. This
      should allow 2nd order reverse mode differentiation of the deserialized
      function. i.e., `jax.grad(jax.grad(f)).`
  """
  builder = flatbuffers.Builder(65536)
  exported = _serialize_exported(builder, exp, vjp_order)
  builder.Finish(exported)
  return builder.Output()


def serialize(message: _MESSAGE, deterministic: bool = None) -> bytes:
  """Return the serialized proto.

  Args:
    message: The proto message to be serialized.
    deterministic: If true, requests deterministic serialization
        of the protobuf, with predictable ordering of map keys.

  Returns:
    A binary bytes representation of the message.
  """
  return message.SerializeToString(deterministic=deterministic)


def serialize(
    message: Message,
    always_print_fields_with_no_presence: bool=False,
    preserving_proto_field_name: bool=False,
    use_integers_for_enums: bool=False,
    descriptor_pool: Optional[DescriptorPool]=None,
) -> dict:
  """Converts protobuf message to a dictionary.

  When the dictionary is encoded to JSON, it conforms to ProtoJSON spec.

  Args:
    message: The protocol buffers message instance to serialize.
    always_print_fields_with_no_presence: If True, fields without presence
      (implicit presence scalars, repeated fields, and map fields) will always
      be serialized. Any field that supports presence is not affected by this
      option (including singular message fields and oneof fields).
    preserving_proto_field_name: If True, use the original proto field names as
      defined in the .proto file. If False, convert the field names to
      lowerCamelCase.
    use_integers_for_enums: If true, print integers instead of enum names.
    descriptor_pool: A Descriptor Pool for resolving types. If None use the
      default.

  Returns:
    A dict representation of the protocol buffer message.
  """
  return json_format.MessageToDict(
      message,
      always_print_fields_with_no_presence=always_print_fields_with_no_presence,
      preserving_proto_field_name=preserving_proto_field_name,
      use_integers_for_enums=use_integers_for_enums,
  )


def serialize(
    message: Message,
    as_utf8: bool = True,
    as_one_line: bool = False,
    use_short_repeated_primitives: bool = False,
    pointy_brackets: bool = False,
    use_index_order: bool = False,
    use_field_number: bool = False,
    descriptor_pool: Optional[DescriptorPool] = None,
    indent: int = 0,
    message_formatter: Optional[_MsgFormatter] = None,
    print_unknown_fields: bool = False,
    force_colon: bool = False,
) -> str:
  """Convert protobuf message to text format.

  Double values can be formatted compactly with 15 digits of
  precision (which is the most that IEEE 754 "double" can guarantee)
  using double_format='.15g'. To ensure that converting to text and back to a
  proto will result in an identical value, double_format='.17g' should be used.

  Args:
    message: The protocol buffers message.
    as_utf8: Return unescaped Unicode for non-ASCII characters.
    as_one_line: Don't introduce newlines between fields.
    use_short_repeated_primitives: Use short repeated format for primitives.
    pointy_brackets: If True, use angle brackets instead of curly braces for
      nesting.
    use_index_order: If True, fields of a proto message will be printed using
      the order defined in source code instead of the field number, extensions
      will be printed at the end of the message and their relative order is
      determined by the extension number. By default, use the field number
      order.
    use_field_number: If True, print field numbers instead of names.
    descriptor_pool (DescriptorPool): Descriptor pool used to resolve Any types.
    indent (int): The initial indent level, in terms of spaces, for pretty
      print.
    message_formatter (function(message, indent, as_one_line) -> unicode|None):
      Custom formatter for selected sub-messages (usually based on message
      type). Use to pretty print parts of the protobuf for easier diffing.
    print_unknown_fields: If True, unknown fields will be printed.
    force_colon: If set, a colon will be added after the field name even if the
      field is a proto message.

  Returns:
    str: A string of the text formatted protocol buffer message.
  """
  return text_format.MessageToString(
      message=message,
      as_utf8=as_utf8,
      as_one_line=as_one_line,
      use_short_repeated_primitives=use_short_repeated_primitives,
      pointy_brackets=pointy_brackets,
      use_index_order=use_index_order,
      use_field_number=use_field_number,
      descriptor_pool=descriptor_pool,
      indent=indent,
      message_formatter=message_formatter,
      print_unknown_fields=print_unknown_fields,
      force_colon=force_colon,
  )


def serialize(input, tree="etree", encoding=None, **serializer_opts):
    """Serializes the input token stream using the specified treewalker

    :arg input: the token stream to serialize

    :arg tree: the treewalker to use

    :arg encoding: the encoding to use

    :arg serializer_opts: any options to pass to the
        :py:class:`html5lib.serializer.HTMLSerializer` that gets created

    :returns: the tree serialized as a string

    Example:

    >>> from html5lib.html5parser import parse
    >>> from html5lib.serializer import serialize
    >>> token_stream = parse('<html><body><p>Hi!</p></body></html>')
    >>> serialize(token_stream, omit_optional_tags=False)
    '<html><head></head><body><p>Hi!</p></body></html>'

    """
    # XXX: Should we cache this?
    walker = treewalkers.getTreeWalker(tree)
    s = HTMLSerializer(**serializer_opts)
    return s.render(walker(input), encoding)

