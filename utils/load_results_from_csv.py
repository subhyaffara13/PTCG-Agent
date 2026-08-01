
def load_results_from_csv(csv_path):
    rows = []
    import csv  # noqa: PLC0415

    with open(csv_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)  # noqa: PERF402
    return rows

