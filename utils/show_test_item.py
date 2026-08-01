
def show_test_item(item: Item, *, add_space: bool) -> None:
    """Show test function, parameters and the fixtures of the test item."""
    tw = item.config.get_terminal_writer()
    tw.line()
    tw.write(" " * 8)
    tw.write(item.nodeid)
    used_fixtures = sorted(getattr(item, "fixturenames", []))
    if used_fixtures:
        tw.write(f" (fixtures used: {', '.join(used_fixtures)})")
    if add_space:
        tw.write(" ")
    tw.flush()

