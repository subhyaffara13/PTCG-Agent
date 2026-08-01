
def _sortAxisValues(axisValues):
    # Sort by axis index, remove duplicates and ensure that format 4 AxisValues
    # are dominant.
    # The MS Spec states: "if a format 1, format 2 or format 3 table has a
    # (nominal) value used in a format 4 table that also has values for
    # other axes, the format 4 table, being the more specific match, is used",
    # https://docs.microsoft.com/en-us/typography/opentype/spec/stat#axis-value-table-format-4
    results = []
    seenAxes = set()
    # Sort format 4 axes so the tables with the most AxisValueRecords are first
    format4 = sorted(
        [v for v in axisValues if v.Format == 4],
        key=lambda v: len(v.AxisValueRecord),
        reverse=True,
    )

    for val in format4:
        axisIndexes = set(r.AxisIndex for r in val.AxisValueRecord)
        minIndex = min(axisIndexes)
        if not seenAxes & axisIndexes:
            seenAxes |= axisIndexes
            results.append((minIndex, val))

    for val in axisValues:
        if val in format4:
            continue
        axisIndex = val.AxisIndex
        if axisIndex not in seenAxes:
            seenAxes.add(axisIndex)
            results.append((axisIndex, val))

    return [axisValue for _, axisValue in sorted(results)]

