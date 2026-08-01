
def run_city_game(repos: list[RepoStorageInfo]) -> None:
    """Launch the interactive city explorer."""
    if not repos:
        print("No repositories found.")
        return

    try:
        import termios
        import tty
    except ImportError:
        print("Interactive mode requires a Unix-like terminal (Linux/macOS).")
        return

    if not sys.stdin.isatty() or not sys.stdout.isatty():
        print("Interactive mode requires a terminal.")
        return

    term = shutil.get_terminal_size()
    if term.columns < _MIN_TERM_W or term.lines < _MIN_TERM_H:
        print(f"Your terminal is {term.columns}×{term.lines} characters.")
        print(f"Please resize to at least {_MIN_TERM_W}×{_MIN_TERM_H} to explore the city!")
        return

    city = _prepare_city_data(repos)

    tiles_with_repos = [t for t in city.tiles if t.repo is not None]
    start_tile = random.choice(tiles_with_repos) if tiles_with_repos else city.tiles[0]

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        sys.stdout.write("\033[?1049h\033[?25l\033[2J")
        sys.stdout.flush()
        _game_loop(city, start_tile.grid_row, start_tile.grid_col)
    finally:
        sys.stdout.write("\033[?25h\033[?1049l")
        sys.stdout.flush()
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

