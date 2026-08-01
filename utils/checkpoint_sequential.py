
def checkpoint_sequential(functions, segments, input, use_reentrant=None, **kwargs):
    r"""Checkpoint a sequential model to save memory.

    Sequential models execute a list of modules/functions in order
    (sequentially). Therefore, we can divide such a model in various segments
    and checkpoint each segment. All segments except the last will not store
    the intermediate activations. The inputs of each checkpointed segment will
    be saved for re-running the segment in the backward pass.

    .. warning::
        The ``use_reentrant`` parameter should be passed explicitly. In version
        2.9 we will raise an exception if ``use_reentrant`` is not passed.
        If you are using the ``use_reentrant=True` variant, please see
        :func:`~torch.utils.checkpoint.checkpoint` for
        the important considerations and limitations of this variant. It is
        recommended that you use ``use_reentrant=False``.

    .. warning:
        Since PyTorch 1.4, it allows only one Tensor as the input and
        intermediate outputs, just like :class:`torch.nn.Sequential`.

    Args:
        functions: A :class:`torch.nn.Sequential` or the list of modules or
            functions (comprising the model) to run sequentially.
        segments: Number of chunks to create in the model
        input: A Tensor that is input to :attr:`functions`
        preserve_rng_state(bool, optional):  Omit stashing and restoring
            the RNG state during each checkpoint.
            Default: ``True``
        use_reentrant(bool):
            specify whether to use the activation checkpoint variant that
            requires reentrant autograd. This parameter should be passed
            explicitly. In version 2.5 we will raise an exception if
            ``use_reentrant`` is not passed. If ``use_reentrant=False``,
            ``checkpoint`` will use an implementation that does not require
            reentrant autograd. This allows ``checkpoint`` to support additional
            functionality, such as working as expected with
            ``torch.autograd.grad`` and support for keyword arguments input into
            the checkpointed function.

    Returns:
        Output of running :attr:`functions` sequentially on :attr:`*inputs`

    Example:
        >>> # xdoctest: +SKIP("stub")
        >>> model = nn.Sequential(...)
        >>> input_var = checkpoint_sequential(model, chunks, input_var)
    """
    if use_reentrant is None:
        warnings.warn(
            "torch.utils.checkpoint.checkpoint_sequential: the use_reentrant "
            "parameter should be passed explicitly. "
            "In version 2.9 we will raise an exception if use_reentrant "
            "is not passed. use_reentrant=False is "
            "recommended, but if you need to preserve the current default "
            "behavior, you can pass use_reentrant=True. Refer to docs for more "
            "details on the differences between the two variants.", stacklevel=2
        )
        use_reentrant = True

    # Hack for keyword-only parameter in a python 2.7-compliant way
    preserve = kwargs.pop("preserve_rng_state", True)
    if kwargs:
        raise ValueError(
            "Unexpected keyword arguments: " + ",".join(arg for arg in kwargs)
        )

    def run_function(start, end, functions):
        def forward(input):
            for j in range(start, end + 1):
                input = functions[j](input)
            return input

        return forward

    if isinstance(functions, torch.nn.Sequential):
        functions = list(functions.children())

    segment_size = len(functions) // segments
    # the last chunk has to be non-volatile
    end = -1
    for start in range(0, segment_size * (segments - 1), segment_size):
        end = start + segment_size - 1
        input = checkpoint(
            run_function(start, end, functions),
            input,
            use_reentrant=use_reentrant,
            preserve_rng_state=preserve,
        )
    return run_function(end + 1, len(functions) - 1, functions)(input)

