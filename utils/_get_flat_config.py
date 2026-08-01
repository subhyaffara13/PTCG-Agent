
def _get_flat_config():
  """Helper to generate simple config without references."""

  # The suggested way to create a ConfigDict() is to call its constructor
  # and assign all relevant fields.
  config = config_dict.ConfigDict()

  # In order to add new attributes you can just use . notation, like with any
  # python object. They will be tracked by ConfigDict, and you get type checking
  # etc. for free.
  config.integer = 23
  config.float = 2.34
  config.string = 'james'
  config.bool = True

  # It is possible to assign dictionaries to ConfigDict and they will be
  # automatically and recursively wrapped with ConfigDict. However, make sure
  # that the dict you are assigning does not use internal references/cycles as
  # this is not supported. Instead, create the dicts explicitly as demonstrated
  # by get_config(). But note that this operation makes an element-by-element
  # copy of your original dict.

  # Also note that the recursive wrapping on input dictionaries with ConfigDict
  # does not extend through non-dictionary types (including basic Python types
  # and custom classes). This causes unexpected behavior most commonly if a
  # value is a list of dictionaries, so avoid giving ConfigDict such inputs.
  config.dict = {
      'integer': 1,
      'float': 3.14,
      'string': 'mark',
      'bool': False,
      'dict': {
          'float': 5
      }
  }
  return config

