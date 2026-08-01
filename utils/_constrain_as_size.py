
def _constrain_as_size(
    symbol,
    min: builtins.int | None = None,
    max: builtins.int | None = None,
):
    """
    This indicates that a given int is size-like, and can be used in any context where a size is expected.
    You will typically use this when reading out integers from Tensors, e.g., max.item() or lengths.tolist()
    which then need to be used as tensor constructors. Providing these assertions to PyTorch can help resolve
      GuardOnDataDependentSymNode errors upon export, since we cannot guard on unbacked SymInts.

    This function has unusual semantics in some circumstances in framework
    code, we will treat this int as >= 2 (when we do a size-oblivious guard).
    This makes it easier to use the unbacked int in size contexts,
    as we will often attempt to guard on a size being zero/one
    (e.g., when computing the contiguity of a tensor, or testing if
    broadcasting can occur), which will not work on unbacked SymInts.
    However, if we conservatively assume that the size is not zero/one, we will
    end up with a graph that will still work even if the size is zero/one.

    For more details, see https://docs.google.com/document/d/1HSuTTVvYH1pTew89Rtpeu84Ht3nQEFTYhAX3Ypa_xJs/edit
    ```
    """
    torch.sym_constrain_range_for_size(symbol, min=min, max=max)

