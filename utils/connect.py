
def connect(s: MouseEventType, func: Callable[[MouseEvent], Any]) -> int: ...


def connect(s: KeyEventType, func: Callable[[KeyEvent], Any]) -> int: ...


def connect(s: PickEventType, func: Callable[[PickEvent], Any]) -> int: ...


def connect(s: ResizeEventType, func: Callable[[ResizeEvent], Any]) -> int: ...


def connect(s: CloseEventType, func: Callable[[CloseEvent], Any]) -> int: ...


def connect(s: DrawEventType, func: Callable[[DrawEvent], Any]) -> int: ...


def connect(s, func) -> int:
    return gcf().canvas.mpl_connect(s, func)

