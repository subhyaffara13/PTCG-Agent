from typing import Any

def describe(
    article: str | None,
    value: Any,
    name: str | None = None,
    verbose: bool = False,
    capital: bool = False,
) -> str:
    """Return string that describes a value

    Parameters
    ----------
    article : str or None
        A definite or indefinite article. If the article is
        indefinite (i.e. "a" or "an") the appropriate one
        will be inferred. Thus, the arguments of ``describe``
        can themselves represent what the resulting string
        will actually look like. If None, then no article
        will be prepended to the result. For non-articled
        description, values that are instances are treated
        definitely, while classes are handled indefinitely.
    value : any
        The value which will be named.
    name : str or None (default: None)
        Only applies when ``article`` is "the" - this
        ``name`` is a definite reference to the value.
        By default one will be inferred from the value's
        type and repr methods.
    verbose : bool (default: False)
        Whether the name should be concise or verbose. When
        possible, verbose names include the module, and/or
        class name where an object was defined.
    capital : bool (default: False)
        Whether the first letter of the article should
        be capitalized or not. By default it is not.

    Examples
    --------
    Indefinite description:

    >>> describe("a", object())
    'an object'
    >>> describe("a", object)
    'an object'
    >>> describe("a", type(object))
    'a type'

    Definite description:

    >>> describe("the", object())
    "the object at '...'"
    >>> describe("the", object)
    'the object object'
    >>> describe("the", type(object))
    'the type type'

    Definitely named description:

    >>> describe("the", object(), "I made")
    'the object I made'
    >>> describe("the", object, "I will use")
    'the object I will use'
    """
    if isinstance(article, str):
        article = article.lower()

    if not inspect.isclass(value):
        typename = type(value).__name__
    else:
        typename = value.__name__
    if verbose:
        typename = _prefix(value) + typename

    if article == "the" or (article is None and not inspect.isclass(value)):
        if name is not None:
            result = f"{typename} {name}"
            if article is not None:
                return add_article(result, True, capital)
            else:
                return result
        else:
            tick_wrap = False
            if inspect.isclass(value):
                name = value.__name__
            elif isinstance(value, types.FunctionType):
                name = value.__name__
                tick_wrap = True
            elif isinstance(value, types.MethodType):
                name = value.__func__.__name__
                tick_wrap = True
            elif type(value).__repr__ in (
                object.__repr__,
                type.__repr__,
            ):  # type:ignore[comparison-overlap]
                name = "at '%s'" % hex(id(value))
                verbose = False
            else:
                name = repr(value)
                verbose = False
            if verbose:
                name = _prefix(value) + name
            if tick_wrap:
                name = name.join("''")
            return describe(article, value, name=name, verbose=verbose, capital=capital)
    elif article in ("a", "an") or article is None:
        if article is None:
            return typename
        return add_article(typename, False, capital)
    else:
        raise ValueError(
            "The 'article' argument should be 'the', 'a', 'an', or None not %r" % article
        )


def describe(a, axis=0, ddof=0, bias=True):
    """
    Computes several descriptive statistics of the passed array.

    Parameters
    ----------
    a : array_like
        Data array
    axis : int or None, optional
        Axis along which to calculate statistics. Default 0. If None,
        compute over the whole array `a`.
    ddof : int, optional
        degree of freedom (default 0); note that default ddof is different
        from the same routine in stats.describe
    bias : bool, optional
        If False, then the skewness and kurtosis calculations are corrected for
        statistical bias.

    Returns
    -------
    nobs : int
        (size of the data (discarding missing values)

    minmax : (int, int)
        min, max

    mean : float
        arithmetic mean

    variance : float
        unbiased variance

    skewness : float
        biased skewness

    kurtosis : float
        biased kurtosis

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.stats.mstats import describe
    >>> ma = np.ma.array(range(6), mask=[0, 0, 0, 1, 1, 1])
    >>> describe(ma)
    DescribeResult(nobs=np.int64(3), minmax=(masked_array(data=0,
                 mask=False,
           fill_value=999999), masked_array(data=2,
                 mask=False,
           fill_value=999999)), mean=np.float64(1.0),
           variance=np.float64(0.6666666666666666),
           skewness=masked_array(data=0., mask=False, fill_value=1e+20),
            kurtosis=np.float64(-1.5))

    """
    a, axis = _chk_asarray(a, axis)
    n = a.count(axis)
    mm = (ma.minimum.reduce(a, axis=axis), ma.maximum.reduce(a, axis=axis))
    m = a.mean(axis)
    v = a.var(axis, ddof=ddof)
    sk = skew(a, axis, bias=bias)
    kurt = kurtosis(a, axis, bias=bias)

    return DescribeResult(n, mm, m, v, sk, kurt)


def describe(a, axis=0, ddof=1, bias=True, nan_policy='propagate'):
    """Compute several descriptive statistics of the passed array.

    Parameters
    ----------
    a : array_like
        Input data.
    axis : int or None, optional
        Axis along which statistics are calculated. Default is 0.
        If None, compute over the whole array `a`.
    ddof : int, optional
        Delta degrees of freedom (only for variance).  Default is 1.
    bias : bool, optional
        If False, then the skewness and kurtosis calculations are corrected
        for statistical bias.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan.
        The following options are available (default is 'propagate'):

        * 'propagate': returns nan
        * 'raise': throws an error
        * 'omit': performs the calculations ignoring nan values

    Returns
    -------
    nobs : int or ndarray of ints
        Number of observations (length of data along `axis`).
        When 'omit' is chosen as nan_policy, the length along each axis
        slice is counted separately.
    minmax: tuple of ndarrays or floats
        Minimum and maximum value of `a` along the given axis.
    mean : ndarray or float
        Arithmetic mean of `a` along the given axis.
    variance : ndarray or float
        Unbiased variance of `a` along the given axis; denominator is number
        of observations minus one.
    skewness : ndarray or float
        Skewness of `a` along the given axis, based on moment calculations
        with denominator equal to the number of observations, i.e. no degrees
        of freedom correction.
    kurtosis : ndarray or float
        Kurtosis (Fisher) of `a` along the given axis.  The kurtosis is
        normalized so that it is zero for the normal distribution.  No
        degrees of freedom are used.

    Raises
    ------
    ValueError
        If size of `a` is 0.

    See Also
    --------
    skew, kurtosis

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import stats
    >>> a = np.arange(10)
    >>> stats.describe(a)
    DescribeResult(nobs=10, minmax=(0, 9), mean=4.5,
                   variance=9.166666666666666, skewness=0.0,
                   kurtosis=-1.2242424242424244)
    >>> b = [[1, 2], [3, 4]]
    >>> stats.describe(b)
    DescribeResult(nobs=2, minmax=(array([1, 2]), array([3, 4])),
                   mean=array([2., 3.]), variance=array([2., 2.]),
                   skewness=array([0., 0.]), kurtosis=array([-2., -2.]))

    """
    xp = array_namespace(a)
    a, axis = _chk_asarray(a, axis, xp=xp)

    contains_nan = _contains_nan(a, nan_policy)

    # Test nan_policy before the implicit call to bool(contains_nan)
    # to avoid raising on lazy xps on the default nan_policy='propagate'
    if nan_policy == 'omit' and contains_nan:
        # only NumPy gets here; `_contains_nan` raises error for the rest
        a = ma.masked_invalid(a)
        return mstats_basic.describe(a, axis, ddof, bias)

    if xp_size(a) == 0:
        raise ValueError("The input must not be empty.")

    # use xp.astype when data-apis/array-api-compat#226 is resolved
    n = xp.asarray(_count_nonmasked(a, axis, xp=xp), dtype=xp.int64,
                   device=xp_device(a))
    n = n[()] if n.ndim == 0 else n
    mm = (xp.min(a, axis=axis), xp.max(a, axis=axis))
    a = xp_promote(a, force_floating=True, xp=xp)
    m = xp.mean(a, axis=axis)
    v = _var(a, axis=axis, ddof=ddof, xp=xp)
    v = v[()] if v.ndim == 0 else v
    sk = skew(a, axis, bias=bias)
    kurt = kurtosis(a, axis, bias=bias)

    return DescribeResult(n, mm, m, v, sk, kurt)


def describe(G, describe_hook=None):
    """Prints a description of the graph G.

    By default, the description includes some basic properties of the graph.
    You can also provide additional functions to compute and include
    more properties in the description.

    Parameters
    ----------
    G : graph
        A NetworkX graph.

    describe_hook: callable, optional (default=None)
        A function that takes a graph as input and returns a
        dictionary of additional properties to include in the description.
        The keys of the dictionary are the property names, and the values
        are the corresponding property values.

    Examples
    --------
    >>> G = nx.path_graph(5)
    >>> nx.describe(G)
    Number of nodes                : 5
    Number of edges                : 4
    Directed                       : False
    Multigraph                     : False
    Tree                           : True
    Bipartite                      : True
    Average degree (min, max)      : 1.60 (1, 2)
    Number of connected components : 1

    >>> def augment_description(G):
    ...     return {"Average Shortest Path Length": nx.average_shortest_path_length(G)}
    >>> nx.describe(G, describe_hook=augment_description)
    Number of nodes                : 5
    Number of edges                : 4
    Directed                       : False
    Multigraph                     : False
    Tree                           : True
    Bipartite                      : True
    Average degree (min, max)      : 1.60 (1, 2)
    Number of connected components : 1
    Average Shortest Path Length   : 2.0

    >>> G.name = "Path Graph of 5 nodes"
    >>> nx.describe(G)
    Name of Graph                  : Path Graph of 5 nodes
    Number of nodes                : 5
    Number of edges                : 4
    Directed                       : False
    Multigraph                     : False
    Tree                           : True
    Bipartite                      : True
    Average degree (min, max)      : 1.60 (1, 2)
    Number of connected components : 1

    """
    info_dict = _create_describe_info_dict(G)

    if describe_hook is not None:
        additional_info = describe_hook(G)
        info_dict.update(additional_info)

    max_key_len = max(len(k) for k in info_dict)
    for key, val in info_dict.items():
        print(f"{key:<{max_key_len}} : {val}")


def describe(
    name: NameArg,
    namespace: NamespaceOpt = None,
    token: TokenOpt = None,
) -> None:
    """Get information about an existing endpoint."""
    api = get_hf_api(token=token)
    try:
        endpoint = api.get_inference_endpoint(name=name, namespace=namespace, token=token)
    except HfHubHTTPError as error:
        out.error(f"Fetch failed: {error}")
        raise typer.Exit(code=error.response.status_code) from error

    out.dict(endpoint.raw)

