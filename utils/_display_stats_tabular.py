
def _display_stats_tabular(headers: list[str], table_data: list[list[Any]]) -> None:
    try:
        from tabulate import tabulate
    except ImportError as err:
        raise ImportError("Please install tabulate.") from err

    # Use tabulate to print the table
    print(tabulate(table_data, headers=headers, tablefmt="rst"))

