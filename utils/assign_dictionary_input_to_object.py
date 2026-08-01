
def assign_dictionary_input_to_object(dict_object: dict[str, Any],
                                      road_sections: Collection[str],
                                      default_value: Any) -> dict[str, Any]:
  """Check dictionary has road sections has key or return default_value dict."""
  if dict_object:
    assert set(dict_object) == set(road_sections), (
        "Objects are not defined for each road sections.")
    return dict_object
  dict_object_returned = {}
  for road_section in road_sections:
    dict_object_returned[road_section] = default_value
  return dict_object_returned

