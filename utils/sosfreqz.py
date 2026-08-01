
def sosfreqz(*args, **kwargs):
    """
    Compute the frequency response of a digital filter in SOS format (legacy).

   .. legacy:: function

        This function is an alias, provided for backward compatibility.
        New code should use the function :func:`scipy.signal.freqz_sos`.
        This function became obsolete from version 1.15.0.

    """  # numpydoc ignore=RT01
    return freqz_sos(*args, **kwargs)

