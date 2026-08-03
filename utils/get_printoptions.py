import sys
from typing import Any

def get_printoptions() -> dict[str, Any]:
    r"""Gets the current options for printing, as a dictionary that
    can be passed as ``**kwargs`` to set_printoptions().
    """
    return dataclasses.asdict(PRINT_OPTS)


def get_printoptions():
    """
    Return the current print options.

    Returns
    -------
    print_opts : dict
        Dictionary of current print options with keys

        - precision : int
        - threshold : int
        - edgeitems : int
        - linewidth : int
        - suppress : bool
        - nanstr : str
        - infstr : str
        - sign : str
        - formatter : dict of callables
        - floatmode : str
        - legacy : str or False

        For a full description of these options, see `set_printoptions`.

    Notes
    -----
    These print options apply only to NumPy ndarrays, not to scalars.

    **Concurrency note:** see :ref:`text_formatting_options`

    See Also
    --------
    set_printoptions, printoptions

    Examples
    --------
    >>> import numpy as np

    >>> np.get_printoptions()
    {'edgeitems': 3, 'threshold': 1000, ..., 'override_repr': None}

    >>> np.get_printoptions()['linewidth']
    75
    >>> np.set_printoptions(linewidth=100)
    >>> np.get_printoptions()['linewidth']
    100

    """
    opts = format_options.get().copy()
    opts['legacy'] = {
        113: '1.13', 121: '1.21', 125: '1.25', 201: '2.1',
        202: '2.2', sys.maxsize: False,
    }[opts['legacy']]
    return opts


def get_printoptions():
  """Alias of :func:`numpy.get_printoptions`.

  JAX arrays are printed via NumPy, so NumPy's `printoptions`
  configurations will apply to printed JAX arrays.

  See the :func:`numpy.set_printoptions` documentation for details
  on the available options and their meanings.
  """
  return np.get_printoptions()

