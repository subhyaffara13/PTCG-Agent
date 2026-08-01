
def _rich_install_progress_bar(
    iterable: Iterable[InstallRequirement], *, total: int
) -> Iterator[InstallRequirement]:
    columns = (
        TextColumn("{task.fields[indent]}"),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("{task.description}"),
    )
    console = get_console()

    bar = Progress(*columns, refresh_per_second=6, console=console, transient=True)
    # Hiding the progress bar at initialization forces a refresh cycle to occur
    # until the bar appears, avoiding very short flashes.
    task = bar.add_task("", total=total, indent=" " * get_indentation(), visible=False)
    with bar:
        for req in iterable:
            bar.update(task, description=rf"\[{req.name}]", visible=True)
            yield req
            bar.advance(task)

