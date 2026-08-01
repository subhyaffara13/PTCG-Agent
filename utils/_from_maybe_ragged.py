
def _from_maybe_ragged(
    dot_dimension_numbers: RaggedDotDimensionNumbers | DotDimensionNumbers,
) -> DotDimensionNumbers:
  return (
      dot_dimension_numbers.dot_dimension_numbers
      if isinstance(dot_dimension_numbers, RaggedDotDimensionNumbers)
      else dot_dimension_numbers
  )

