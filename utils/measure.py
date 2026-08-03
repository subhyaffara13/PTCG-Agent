import sys
from typing import Callable

def measure(code_str, times=1, label=None):
    """
    Return elapsed time for executing code in the namespace of the caller.

    The supplied code string is compiled with the Python builtin ``compile``.
    The precision of the timing is 10 milli-seconds. If the code will execute
    fast on this timescale, it can be executed many times to get reasonable
    timing accuracy.

    Parameters
    ----------
    code_str : str
        The code to be timed.
    times : int, optional
        The number of times the code is executed. Default is 1. The code is
        only compiled once.
    label : str, optional
        A label to identify `code_str` with. This is passed into ``compile``
        as the second argument (for run-time error messages).

    Returns
    -------
    elapsed : float
        Total elapsed time in seconds for executing `code_str` `times` times.

    Examples
    --------
    >>> times = 10
    >>> etime = np.testing.measure('for i in range(1000): np.sqrt(i**2)', times=times)
    >>> print("Time for a single execution : ", etime / times, "s")  # doctest: +SKIP
    Time for a single execution :  0.005 s

    """
    frame = sys._getframe(1)
    locs, globs = frame.f_locals, frame.f_globals

    code = compile(code_str, f'Test name: {label} ', 'exec')
    i = 0
    elapsed = jiffies()
    while i < times:
        i += 1
        exec(code, globs, locs)
    elapsed = jiffies() - elapsed
    return 0.01 * elapsed


def measure(
    f: Callable[P, T],
    *,
    aggregate: Literal[True] = ...,
    iterations: Literal[1] = ...,
) -> Callable[P, tuple[T, float | None]]:
  ...


def measure(
    f: Callable[P, T],
    *,
    aggregate: Literal[False] = ...,
    iterations: Literal[1] = ...,
) -> Callable[P, tuple[T, list[tuple[str, float]] | None]]:
  ...


def measure(
    f: Callable[P, T],
    *,
    aggregate: Literal[True] = ...,
    iterations: int = ...,
) -> Callable[P, tuple[T, list[float] | None]]:
  ...


def measure(
    f: Callable[P, T],
    *,
    aggregate: Literal[False] = ...,
    iterations: int = ...,
) -> Callable[P, tuple[T, list[list[tuple[str, float]]] | None]]:
  ...


def measure(
    f, *, aggregate: bool = True, iterations: int = 1,
):
  """Measures the GPU runtime of a function using CUPTI.

  ``measure`` is a higher-order function that wraps a function ``f`` to
  return GPU runtime in milliseconds, in addition to its regular outputs.

  Args:
    f: The function to measure.
    aggregate: Whether to report an aggregate runtime. When ``False`` (only
      supported by ``mode="cupti"``), the per-kernel timings are returned as a
      list of tuples ``(<kernel name>, <runtime in ms>)``.
    iterations: How many times to run the function. Only supported by
      ``mode="cupti"``. When greater than 1, the return type will become a list
      of measurements.

  Returns:
    A function that accepts the same inputs as ``f`` and returns
    ``(f_outputs, timings)``, where ``f_outputs`` are the outputs of ``f``,
    and ``timings`` is either a float or a list of tuples, depending on
    ``aggregate``. If no kernels are launched, ``timings`` is ``None``.

  Notes:
    `CUPTI (CUDA Profiling Tools Interface)
    <https://docs.nvidia.com/cupti/index.html>`_ is a high-accuracy profiling
    API used by Nsight Systems and Nsight Compute. The CUPTI API only allows a
    single subscriber, so ``measure`` cannot be used with other CUPTI-based
    tools like CUDA-GDB, Compute Sanitizer, Nsight Systems, or Nsight
    Compute.
  """  # fmt: skip
  if iterations < 1:
    raise ValueError(f"{iterations=} must be positive")
  return Cupti().measure(f, aggregate=aggregate, iterations=iterations)

