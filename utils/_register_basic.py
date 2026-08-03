from typing import Any

def _register_basic(idx_fmt_name: tuple[int, str, str]) -> None:
    from .TiffTags import TYPES

    idx, fmt, name = idx_fmt_name
    TYPES[idx] = name
    size = struct.calcsize(f"={fmt}")

    def basic_handler(
        self: ImageFileDirectory_v2, data: bytes, legacy_api: bool = True
    ) -> tuple[Any, ...]:
        return self._unpack(f"{len(data) // size}{fmt}", data)

    _load_dispatch[idx] = size, basic_handler  # noqa: F821
    _write_dispatch[idx] = lambda self, *values: (  # noqa: F821
        b"".join(self._pack(fmt, value) for value in values)
    )

