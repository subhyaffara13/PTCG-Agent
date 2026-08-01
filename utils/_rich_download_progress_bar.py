
def _rich_download_progress_bar(
    iterable: Iterable[bytes],
    *,
    bar_type: BarType,
    size: int | None,
    initial_progress: int | None = None,
) -> Generator[bytes, None, None]:
    assert bar_type == "on", "This should only be used in the default mode."

    if not size:
        total = float("inf")
        columns: tuple[ProgressColumn, ...] = (
            TextColumn("[progress.description]{task.description}"),
            SpinnerColumn("line", speed=1.5),
            FileSizeColumn(),
            TransferSpeedColumn(),
            TimeElapsedColumn(),
        )
    else:
        total = size
        columns = (
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            DownloadColumn(),
            TransferSpeedColumn(),
            TextColumn("{task.fields[time_description]}"),
            TimeRemainingColumn(elapsed_when_finished=True),
        )

    progress = Progress(*columns, refresh_per_second=5)
    task_id = progress.add_task(
        " " * (get_indentation() + 2), total=total, time_description="eta"
    )
    if initial_progress is not None:
        progress.update(task_id, advance=initial_progress)
    with progress:
        for chunk in iterable:
            yield chunk
            progress.update(task_id, advance=len(chunk))
        progress.update(task_id, time_description="")

