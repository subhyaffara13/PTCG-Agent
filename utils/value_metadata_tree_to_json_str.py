
def value_metadata_tree_to_json_str(tree: PyTree) -> str:
  """Returns a JSON string representation of the given PyTree.

  Sample JSON::
  ```
  '{
    "mu_nu": {
      "category": "namedtuple",
      "module": "orbax.checkpoint._src.testing.test_tree_utils",
      "clazz": "MuNu",
      "entries": [
        {
          "key": "mu",
          "value": {
            "category": "custom",
            "clazz": "ValueMetadataEntry",
            "data": {
              "value_type": "jax.Array",
              "skip_deserialize": false
            }
          }
        },
        {
          "key": "nu",
          "value": {
            "category": "custom",
            "clazz": "ValueMetadataEntry",
            "data": {
              "value_type": "np.ndarray",
              "skip_deserialize": false
            }
          }
        }
      ]
    },
    "my_tuple": {
      "category": "custom",
      "clazz": "tuple",
      "entries": [
          {
            "category": "custom",
            "clazz": "ValueMetadataEntry",
            "data": {
              "value_type": "np.ndarray",
              "skip_deserialize": false
            }
          }
      ]
    }
  }'
  ```

  Args:
    tree: A PyTree to be converted to JSON string.
  """
  return simplejson.dumps(
      tree,
      default=_value_metadata_tree_for_json_dumps,
      tuple_as_array=False,  # Must be False to preserve tuples.
      namedtuple_as_object=False,  # Must be False to preserve namedtuples.
  )

