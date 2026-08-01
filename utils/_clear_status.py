
def _clear_status(status_dir: str, cell: GameCell) -> None:
    if not status_dir:
        return
    try:
        os.remove(os.path.join(status_dir, _status_filename(cell)))
    except FileNotFoundError:
        pass

