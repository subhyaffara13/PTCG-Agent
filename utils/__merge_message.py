
def _MergeMessage(
    node, source, destination, replace_message, replace_repeated):
  """Merge all fields specified by a sub-tree from source to destination."""
  stack = [(node, source, destination)]
  while stack:
    current_node, current_source, current_destination = stack.pop()
    source_descriptor = current_source.DESCRIPTOR
    for name in current_node:
      child = current_node[name]
      field = source_descriptor.fields_by_name[name]
      if field is None:
        raise ValueError('Error: Can\'t find field {0} in message {1}.'.format(
            name, source_descriptor.full_name))
      if child:
        # Sub-paths are only allowed for singular message fields.
        if (field.is_repeated or
            field.cpp_type != FieldDescriptor.CPPTYPE_MESSAGE):
          raise ValueError('Error: Field {0} in message {1} is not a singular '
                           'message field and cannot have sub-fields.'.format(
                               name, source_descriptor.full_name))
        if current_source.HasField(name):
          stack.append(
              (child, getattr(current_source, name),
               getattr(current_destination, name)))
        continue
      if field.is_repeated:
        if replace_repeated:
          current_destination.ClearField(_StrConvert(name))
        repeated_source = getattr(current_source, name)
        repeated_destination = getattr(current_destination, name)
        repeated_destination.MergeFrom(repeated_source)
      else:
        if field.cpp_type == FieldDescriptor.CPPTYPE_MESSAGE:
          if replace_message:
            current_destination.ClearField(_StrConvert(name))
          if current_source.HasField(name):
            getattr(current_destination, name).MergeFrom(
                getattr(current_source, name))
        elif not field.has_presence or current_source.HasField(name):
          setattr(current_destination, name, getattr(current_source, name))
        else:
          current_destination.ClearField(_StrConvert(name))

