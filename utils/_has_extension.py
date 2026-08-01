
def _has_extension(
    proto: message.Message, ext: message.FieldDescriptor
) -> bool:
  if ext.label == ext.LABEL_REPEATED:
    return bool(len(proto.Extensions[ext]))
  return proto.HasExtension(ext)

