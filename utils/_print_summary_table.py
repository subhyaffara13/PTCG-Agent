
def _print_summary_table(provider_counts):
    summary_table = rich.table.Table(title="Model Import Summary")
    summary_table.add_column("Provider", style="cyan")
    summary_table.add_column("Count", style="green")

    for provider, count in provider_counts.items():
        summary_table.add_row(str(provider), str(count))

    total = sum(provider_counts.values())
    summary_table.add_row("[bold]Total[/bold]", f"[bold]{total}[/bold]")

    rich.print(summary_table)

