from typing import Optional

def _format_bytes(n: float) -> str:
    for unit in ("B", "kB", "MB", "GB", "TB"):
        if abs(n) < 1000:
            if n < 10:
                return f"{n:.2f}{unit}"
            elif n < 100:
                return f"{n:.1f}{unit}"
            return f"{n:.0f}{unit}"
        n /= 1000
    return f"{n:.1f}PB"


def _format_bytes(bytes_value: Optional[int]) -> str:
  return (
      'None'
      if bytes_value is None
      else f'{bytes_value} ({humanize.naturalsize(bytes_value, binary=True)})'
  )

