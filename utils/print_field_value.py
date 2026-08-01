
def PrintFieldValue(field,
                    value,
                    out,
                    indent=0,
                    as_utf8=_as_utf8_default,
                    as_one_line=False,
                    use_short_repeated_primitives=False,
                    pointy_brackets=False,
                    use_index_order=False,
                    message_formatter=None,
                    print_unknown_fields=False,
                    force_colon=False):
  """Print a single field value (not including name)."""
  printer = _Printer(
      out,
      indent,
      as_utf8,
      as_one_line,
      use_short_repeated_primitives,
      pointy_brackets,
      use_index_order,
      message_formatter=message_formatter,
      print_unknown_fields=print_unknown_fields,
      force_colon=force_colon,
  )
  printer.PrintFieldValue(field, value)

