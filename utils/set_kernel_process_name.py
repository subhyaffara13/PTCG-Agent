
def set_kernel_process_name(name):
  """Changes the Kernel's /proc/self/status process name on Linux.

  The kernel name is NOT what will be shown by the ps or top command.
  It is a 15 character string stored in the kernel's process table that
  is included in the kernel log when a process is OOM killed.
  The first 15 bytes of name are used.  Non-ASCII unicode is replaced with '?'.

  Does nothing if /proc/self/comm cannot be written or prctl() fails.

  Args:
    name: bytes|unicode, the Linux kernel's command name to set.
  """
  if not isinstance(name, bytes):
    name = name.encode('ascii', 'replace')
  try:
    # This is preferred to using ctypes to try and call prctl() when possible.
    with open('/proc/self/comm', 'wb') as proc_comm:
      proc_comm.write(name[:15])
  except OSError:
    try:
      import ctypes  # pylint: disable=g-import-not-at-top
    except ImportError:
      return  # No ctypes.
    try:
      libc = ctypes.CDLL('libc.so.6')
    except OSError:
      return  # No libc.so.6.
    pr_set_name = ctypes.c_ulong(15)  # linux/prctl.h PR_SET_NAME value.
    zero = ctypes.c_ulong(0)
    try:
      libc.prctl(pr_set_name, name, zero, zero, zero)
      # Ignore the prctl return value.  Nothing we can do if it errored.
    except AttributeError:
      return  # No prctl.

