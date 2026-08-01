
def _truncate_long_str(value: str, *, expand_new_lines: bool = False) -> str:
  """Truncate long strings."""
  value = html.escape(value)
  if expand_new_lines:
    # `repr` replace `\n` by `\\n` on str, so only apply it on the short version
    short_value = repr(value)
  else:
    short_value = value
  # TODO(epot): Could have a better expand section which truncate long string
  # (e.g. > 100 lines)
  # TODO(epot): Better CSS (with button)
  if len(short_value) > 80:
    if expand_new_lines:
      # On the long value, add the same braces `'` or `"`
      long_value = short_value[0] + value + short_value[-1]
    else:
      long_value = value
    return H.span(class_=['content-switch'])(
        # Short version
        H.span(class_=['content-version-short'])(
            short_value[:80]
            + H.span(
                class_=['content-switch-expand', 'register-onclick-switch']
            )('...')
        ),
        # Long version
        H.span(class_=['content-version-long', 'register-onclick-switch'])(
            long_value
        ),
    )
  else:
    return short_value

