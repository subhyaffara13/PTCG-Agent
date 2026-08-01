
def _PropertyName(proto_field_name):
  """Returns the name of the public property attribute which
  clients can use to get and (in some cases) set the value
  of a protocol message field.

  Args:
    proto_field_name: The protocol message field name, exactly
      as it appears (or would appear) in a .proto file.
  """
  # TODO: Escape Python keywords (e.g., yield), and test this support.
  # nnorwitz makes my day by writing:
  # """
  # FYI.  See the keyword module in the stdlib. This could be as simple as:
  #
  # if keyword.iskeyword(proto_field_name):
  #   return proto_field_name + "_"
  # return proto_field_name
  # """
  # Kenton says:  The above is a BAD IDEA.  People rely on being able to use
  #   getattr() and setattr() to reflectively manipulate field values.  If we
  #   rename the properties, then every such user has to also make sure to apply
  #   the same transformation.  Note that currently if you name a field "yield",
  #   you can still access it just fine using getattr/setattr -- it's not even
  #   that cumbersome to do so.
  # TODO:  Remove this method entirely if/when everyone agrees with my
  #   position.
  return proto_field_name

