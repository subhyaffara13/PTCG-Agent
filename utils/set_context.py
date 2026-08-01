
def set_context(context=None, font_scale=1, rc=None):
    """
    Set the parameters that control the scaling of plot elements.

    These parameters correspond to label size, line thickness, etc.
    Calling this function modifies the global matplotlib `rcParams`. For more
    information, see the :doc:`aesthetics tutorial <../tutorial/aesthetics>`.

    The base context is "notebook", and the other contexts are "paper", "talk",
    and "poster", which are version of the notebook parameters scaled by different
    values. Font elements can also be scaled independently of (but relative to)
    the other values.

    See :func:`plotting_context` to get the parameter values.

    Parameters
    ----------
    context : dict, or one of {paper, notebook, talk, poster}
        A dictionary of parameters or the name of a preconfigured set.
    font_scale : float, optional
        Separate scaling factor to independently scale the size of the
        font elements.
    rc : dict, optional
        Parameter mappings to override the values in the preset seaborn
        context dictionaries. This only updates parameters that are
        considered part of the context definition.

    Examples
    --------

    .. include:: ../docstrings/set_context.rst

    """
    context_object = plotting_context(context, font_scale, rc)
    mpl.rcParams.update(context_object)

