
def raw_terminal() -> AbstractContextManager[int]:
    from ._termui_impl import raw_terminal as f

    return f()

