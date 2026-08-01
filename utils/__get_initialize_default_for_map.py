
def _GetInitializeDefaultForMap(field):
  if not field.is_repeated:
    raise ValueError('map_entry set on non-repeated field %s' % (
        field.name))
  fields_by_name = field.message_type.fields_by_name
  key_checker = type_checkers.GetTypeChecker(fields_by_name['key'])

  value_field = fields_by_name['value']
  if _IsMessageMapField(field):
    def MakeMessageMapDefault(message):
      return containers.MessageMap(
          message._listener_for_children, value_field.message_type, key_checker,
          field.message_type)
    return MakeMessageMapDefault
  else:
    value_checker = type_checkers.GetTypeChecker(value_field)
    def MakePrimitiveMapDefault(message):
      return containers.ScalarMap(
          message._listener_for_children, key_checker, value_checker,
          field.message_type)
    return MakePrimitiveMapDefault

