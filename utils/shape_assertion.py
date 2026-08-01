
def shape_assertion(assert_what: typing.Array,
                    *error_message_inputs: typing.Array,
                    error_message: str) -> None:
  """Adds a shape assertion in the code.

  Args:
    assert_what: a boolean asserted to be true. Must be computed based only
      on dimension expressions, so that it can be evaluated after shape
      refinement.
    error_message_inputs: integers expressions whose values can be referenced
      in the `error_message`. Must be computed based only
      on dimension expressions, so that they can be evaluated after shape
      refinement.
    error_message: an error message, possibly containing format specifiers
      {0}, {1}, ..., referencing the values of the `error_message_inputs`.
      The format specifiers are sometimes processed with Python's
      `string::format` method, and sometimes with `llvm::formatv`.
  """
  shape_assertion_p.bind(assert_what, *error_message_inputs,
                         error_message=error_message)

