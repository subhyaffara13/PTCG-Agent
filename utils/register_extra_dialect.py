from typing import Callable

def register_extra_dialect(loader: Callable[[ir.Context], None]):
  _extra_dialect_loaders.append(loader)

