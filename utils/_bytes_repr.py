
def _bytes_repr(num_bytes):
  count, units = (
    (f'{num_bytes / 1e9:,.1f}', 'GB')
    if num_bytes > 1e9
    else (f'{num_bytes / 1e6:,.1f}', 'MB')
    if num_bytes > 1e6
    else (f'{num_bytes / 1e3:,.1f}', 'KB')
    if num_bytes > 1e3
    else (f'{num_bytes:,}', 'B')
  )

  return f'{count} {units}'


def _bytes_repr(num_bytes):
  count, units = (
    (f'{num_bytes / 1e9 :,.1f}', 'GB')
    if num_bytes > 1e9
    else (f'{num_bytes / 1e6 :,.1f}', 'MB')
    if num_bytes > 1e6
    else (f'{num_bytes / 1e3 :,.1f}', 'KB')
    if num_bytes > 1e3
    else (f'{num_bytes:,}', 'B')
  )

  return f'{count} {units}'


def _bytes_repr(num_bytes):
  count, units = (
    (f'{num_bytes / 1e9:,.1f}', 'GB')
    if num_bytes > 1e9
    else (f'{num_bytes / 1e6:,.1f}', 'MB')
    if num_bytes > 1e6
    else (f'{num_bytes / 1e3:,.1f}', 'KB')
    if num_bytes > 1e3
    else (f'{num_bytes:,}', 'B')
  )

  return f'{count} {units}'

