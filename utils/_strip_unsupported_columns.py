
def _strip_unsupported_columns(csv_bytes: bytes) -> bytes:
    """Remove CSV columns not in VANTAGE_SUPPORTED_COLUMNS.

    Parses the header row, identifies column indices to keep, and
    rebuilds the CSV with only those columns.
    """
    lines = csv_bytes.split(b"\n")
    if not lines:
        return csv_bytes

    header_cols = lines[0].decode("utf-8").split(",")
    keep_indices = [
        i
        for i, col in enumerate(header_cols)
        if col.strip('"') in VANTAGE_SUPPORTED_COLUMNS
    ]

    # If all columns are supported, return as-is
    if len(keep_indices) == len(header_cols):
        return csv_bytes

    dropped = [col for i, col in enumerate(header_cols) if i not in keep_indices]
    verbose_logger.debug(
        "Vantage destination: dropping unsupported columns: %s", dropped
    )

    output = io.StringIO()
    writer = csv.writer(output)
    reader = csv.reader(io.StringIO(csv_bytes.decode("utf-8")))
    for row in reader:
        if not row:
            continue
        writer.writerow([row[i] for i in keep_indices])

    return output.getvalue().encode("utf-8")

