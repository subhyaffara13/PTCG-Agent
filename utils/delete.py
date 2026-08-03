import json
from typing import Any, Dict, Optional, Union

def delete(path: str, handler: _HandlerType, **kwargs: Any) -> RouteDef:
    return route(hdrs.METH_DELETE, path, handler, **kwargs)


def delete(
    url: URL | str,
    *,
    params: QueryParamTypes | None = None,
    headers: HeaderTypes | None = None,
    cookies: CookieTypes | None = None,
    auth: AuthTypes | None = None,
    proxy: ProxyTypes | None = None,
    follow_redirects: bool = False,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
    verify: ssl.SSLContext | str | bool = True,
    trust_env: bool = True,
) -> Response:
    """
    Sends a `DELETE` request.

    **Parameters**: See `httpx.request`.

    Note that the `data`, `files`, `json` and `content` parameters are not available
    on this function, as `DELETE` requests should not include a request body.
    """
    return request(
        "DELETE",
        url,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        proxy=proxy,
        follow_redirects=follow_redirects,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
    )


def delete(url: _t.UriType, **kwargs: Unpack[_t.RequestKwargs]) -> Response:
    r"""Sends a DELETE request.

    :param url: URL for the new :class:`Request` object.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    return request("delete", url, **kwargs)


def Delete(g: jit_utils.GraphContext, tensor_list, dim):
    return g.op("SequenceErase", tensor_list, dim)


def delete(url, **kwargs):
    r"""Sends a DELETE request.

    :param url: URL for the new :class:`Request` object.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    return request("delete", url, **kwargs)


def delete(arr, obj, axis=None):
    """
    Return a new array with sub-arrays along an axis deleted. For a one
    dimensional array, this returns those entries not returned by
    `arr[obj]`.

    Parameters
    ----------
    arr : array_like
        Input array.
    obj : slice, int, array-like of ints or bools
        Indicate indices of sub-arrays to remove along the specified axis.

        .. versionchanged:: 1.19.0
            Boolean indices are now treated as a mask of elements to remove,
            rather than being cast to the integers 0 and 1.

    axis : int, optional
        The axis along which to delete the subarray defined by `obj`.
        If `axis` is None, `obj` is applied to the flattened array.

    Returns
    -------
    out : ndarray
        A copy of `arr` with the elements specified by `obj` removed. Note
        that `delete` does not occur in-place. If `axis` is None, `out` is
        a flattened array.

    See Also
    --------
    insert : Insert elements into an array.
    append : Append elements at the end of an array.

    Notes
    -----
    Often it is preferable to use a boolean mask. For example:

    >>> arr = np.arange(12) + 1
    >>> mask = np.ones(len(arr), dtype=np.bool)
    >>> mask[[0,2,4]] = False
    >>> result = arr[mask,...]

    Is equivalent to ``np.delete(arr, [0,2,4], axis=0)``, but allows further
    use of `mask`.

    Examples
    --------
    >>> import numpy as np
    >>> arr = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]])
    >>> arr
    array([[ 1,  2,  3,  4],
           [ 5,  6,  7,  8],
           [ 9, 10, 11, 12]])
    >>> np.delete(arr, 1, 0)
    array([[ 1,  2,  3,  4],
           [ 9, 10, 11, 12]])

    >>> np.delete(arr, np.s_[::2], 1)
    array([[ 2,  4],
           [ 6,  8],
           [10, 12]])
    >>> np.delete(arr, [1,3,5], None)
    array([ 1,  3,  5,  7,  8,  9, 10, 11, 12])

    """
    conv = _array_converter(arr)
    arr, = conv.as_arrays(subok=False)

    ndim = arr.ndim
    arrorder = 'F' if arr.flags.fnc else 'C'
    if axis is None:
        if ndim != 1:
            arr = arr.ravel()
        # needed for np.matrix, which is still not 1d after being ravelled
        ndim = arr.ndim
        axis = ndim - 1
    else:
        axis = normalize_axis_index(axis, ndim)

    slobj = [slice(None)] * ndim
    N = arr.shape[axis]
    newshape = list(arr.shape)

    if isinstance(obj, slice):
        start, stop, step = obj.indices(N)
        xr = range(start, stop, step)
        numtodel = len(xr)

        if numtodel <= 0:
            return conv.wrap(arr.copy(order=arrorder), to_scalar=False)

        # Invert if step is negative:
        if step < 0:
            step = -step
            start = xr[-1]
            stop = xr[0] + 1

        newshape[axis] -= numtodel
        new = empty(newshape, arr.dtype, arrorder)
        # copy initial chunk
        if start == 0:
            pass
        else:
            slobj[axis] = slice(None, start)
            new[tuple(slobj)] = arr[tuple(slobj)]
        # copy end chunk
        if stop == N:
            pass
        else:
            slobj[axis] = slice(stop - numtodel, None)
            slobj2 = [slice(None)] * ndim
            slobj2[axis] = slice(stop, None)
            new[tuple(slobj)] = arr[tuple(slobj2)]
        # copy middle pieces
        if step == 1:
            pass
        else:  # use array indexing.
            keep = ones(stop - start, dtype=bool)
            keep[:stop - start:step] = False
            slobj[axis] = slice(start, stop - numtodel)
            slobj2 = [slice(None)] * ndim
            slobj2[axis] = slice(start, stop)
            arr = arr[tuple(slobj2)]
            slobj2[axis] = keep
            new[tuple(slobj)] = arr[tuple(slobj2)]

        return conv.wrap(new, to_scalar=False)

    if isinstance(obj, (int, integer)) and not isinstance(obj, bool):
        single_value = True
    else:
        single_value = False
        _obj = obj
        obj = np.asarray(obj)
        # `size == 0` to allow empty lists similar to indexing, but (as there)
        # is really too generic:
        if obj.size == 0 and not isinstance(_obj, np.ndarray):
            obj = obj.astype(intp)
        elif obj.size == 1 and obj.dtype.kind in "ui":
            # For a size 1 integer array we can use the single-value path
            # (most dtypes, except boolean, should just fail later).
            obj = obj.item()
            single_value = True

    if single_value:
        # optimization for a single value
        if (obj < -N or obj >= N):
            raise IndexError(
                f"index {obj} is out of bounds for axis {axis} with "
                f"size {N}")
        if (obj < 0):
            obj += N
        newshape[axis] -= 1
        new = empty(newshape, arr.dtype, arrorder)
        slobj[axis] = slice(None, obj)
        new[tuple(slobj)] = arr[tuple(slobj)]
        slobj[axis] = slice(obj, None)
        slobj2 = [slice(None)] * ndim
        slobj2[axis] = slice(obj + 1, None)
        new[tuple(slobj)] = arr[tuple(slobj2)]
    else:
        if obj.dtype == bool:
            if obj.shape != (N,):
                raise ValueError('boolean array argument obj to delete '
                                 'must be one dimensional and match the axis '
                                 f'length of {N}')

            # optimization, the other branch is slower
            keep = ~obj
        else:
            keep = ones(N, dtype=bool)
            keep[obj,] = False

        slobj[axis] = keep
        new = arr[tuple(slobj)]

    return conv.wrap(new, to_scalar=False)


def delete(
    interaction_id: str,
    extra_headers: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
) -> Union[DeleteInteractionResult, Coroutine[Any, Any, DeleteInteractionResult]]:
    """Sync: Delete an interaction by its ID."""
    local_vars = locals()
    custom_llm_provider = custom_llm_provider or "gemini"

    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
        _is_async = kwargs.pop("adelete_interaction", False) is True

        litellm_params = GenericLiteLLMParams(**kwargs)

        interactions_api_config = get_provider_interactions_api_config(
            provider=custom_llm_provider,
        )

        if interactions_api_config is None:
            raise ValueError(
                f"Interactions API not supported for: {custom_llm_provider}"
            )

        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model=None,
            optional_params={"interaction_id": interaction_id},
            litellm_params={"litellm_call_id": litellm_call_id},
            custom_llm_provider=custom_llm_provider,
        )

        return interactions_http_handler.delete_interaction(
            interaction_id=interaction_id,
            interactions_api_config=interactions_api_config,
            custom_llm_provider=custom_llm_provider,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            extra_headers=extra_headers,
            timeout=timeout,
            _is_async=_is_async,
        )
    except Exception as e:
        raise litellm.exception_type(
            model=None,
            custom_llm_provider=custom_llm_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )


def delete(
    vector_store_id: str,
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
):
    """
    Delete a vector store.

    Args:
        vector_store_id: The ID of the vector store to delete.

    Returns:
        Deletion confirmation response.
    """
    local_vars = locals()
    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
        _is_async = kwargs.pop("adelete", False) is True

        litellm_params = GenericLiteLLMParams(**kwargs)

        if custom_llm_provider is None:
            custom_llm_provider = "openai"

        if "/" in custom_llm_provider:
            api_type, custom_llm_provider, _, _ = get_llm_provider(
                model=custom_llm_provider,
                custom_llm_provider=None,
                litellm_params=None,
            )
        else:
            api_type = None
            custom_llm_provider = custom_llm_provider

        vector_store_provider_config = (
            ProviderConfigManager.get_provider_vector_stores_config(
                provider=litellm.LlmProviders(custom_llm_provider),
                api_type=api_type,
            )
        )

        if vector_store_provider_config is None:
            raise ValueError(
                f"Vector store delete is not supported for {custom_llm_provider}"
            )

        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model=None,
            optional_params={"vector_store_id": vector_store_id},
            litellm_params={"litellm_call_id": litellm_call_id},
            custom_llm_provider=custom_llm_provider,
        )

        response = base_llm_http_handler.vector_store_delete_handler(
            vector_store_id=vector_store_id,
            vector_store_provider_config=vector_store_provider_config,
            custom_llm_provider=custom_llm_provider,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            extra_headers=extra_headers,
            extra_body=extra_body,
            timeout=timeout or request_timeout,
            _is_async=_is_async,
            client=kwargs.get("client"),
        )

        return response
    except Exception as e:
        raise litellm.exception_type(
            model=None,
            custom_llm_provider=custom_llm_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )


def delete(
    *,
    vector_store_id: str,
    file_id: str,
    extra_headers: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
) -> Union[
    VectorStoreFileDeleteResponse, Coroutine[Any, Any, VectorStoreFileDeleteResponse]
]:
    local_vars = locals()
    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id")
        _is_async = kwargs.pop("adelete", False) is True

        custom_llm_provider = _ensure_provider(custom_llm_provider)

        _prepare_registry_credentials(vector_store_id=vector_store_id, kwargs=kwargs)

        litellm_params = GenericLiteLLMParams(vector_store_id=vector_store_id, **kwargs)

        provider_config = ProviderConfigManager.get_provider_vector_store_files_config(
            provider=LlmProviders(custom_llm_provider)
        )
        if provider_config is None:
            raise ValueError(
                f"Vector store file delete is not supported for {custom_llm_provider}"
            )

        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model=None,
            optional_params={
                "vector_store_id": vector_store_id,
                "file_id": file_id,
            },
            litellm_params={
                "vector_store_id": vector_store_id,
                "litellm_call_id": litellm_call_id,
                **litellm_params.model_dump(exclude_none=True),
            },
            custom_llm_provider=custom_llm_provider,
        )

        response = base_llm_http_handler.vector_store_file_delete_handler(
            vector_store_id=vector_store_id,
            file_id=file_id,
            vector_store_files_provider_config=provider_config,
            custom_llm_provider=custom_llm_provider,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            extra_headers=extra_headers,
            timeout=timeout or request_timeout,
            client=kwargs.get("client"),
            _is_async=_is_async,
        )
        return response
    except Exception as e:  # noqa: BLE001
        raise litellm.exception_type(
            model=None,
            custom_llm_provider=custom_llm_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )


def delete(ctx: click.Context, credential_name: str):
    """Delete a credential by name"""
    client = CredentialsManagementClient(ctx.obj["base_url"], ctx.obj["api_key"])
    try:
        response = client.delete(credential_name)
        rich.print_json(data=response)
    except requests.exceptions.HTTPError as e:
        click.echo(f"Error: HTTP {e.response.status_code}", err=True)
        try:
            error_body = e.response.json()
            rich.print_json(data=error_body)
        except json.JSONDecodeError:
            click.echo(e.response.text, err=True)
        raise click.Abort()


def delete(ctx: click.Context, keys: Optional[str], key_aliases: Optional[str]):
    """Delete API keys by key or alias"""
    client = KeysManagementClient(ctx.obj["base_url"], ctx.obj["api_key"])
    keys_list = [k.strip() for k in keys.split(",")] if keys else None
    aliases_list = [a.strip() for a in key_aliases.split(",")] if key_aliases else None
    try:
        response = client.delete(keys=keys_list, key_aliases=aliases_list)
        rich.print_json(data=response)
    except requests.exceptions.HTTPError as e:
        click.echo(f"Error: HTTP {e.response.status_code}", err=True)
        try:
            error_body = e.response.json()
            rich.print_json(data=error_body)
        except json.JSONDecodeError:
            click.echo(e.response.text, err=True)
        raise click.Abort()


def delete(
    name: str,
    custom_llm_provider: Optional[str] = None,
    extra_headers: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    **kwargs,
) -> Union[AgentDeleteResult, Coroutine[Any, Any, AgentDeleteResult]]:
    """Sync: Delete a specific agent by name."""
    local_vars = locals()
    custom_llm_provider = (
        custom_llm_provider or kwargs.get("custom_llm_provider") or "gemini"
    )
    try:
        _is_async = kwargs.pop("adelete_agent", False) is True
        kwargs.setdefault("custom_llm_provider", custom_llm_provider)
        litellm_params = GenericLiteLLMParams(**kwargs)
        logging_obj = _make_logging_obj(
            kwargs, name, custom_llm_provider, "delete_agent", {"name": name}
        )
        config = _get_agents_api_config(custom_llm_provider)
        return agents_http_handler.delete_agent(
            agents_api_config=config,
            name=name,
            litellm_params=litellm_params,
            logging_obj=logging_obj,
            extra_headers=extra_headers,
            timeout=timeout,
            _is_async=_is_async,
        )
    except Exception as e:
        raise litellm.exception_type(
            model=name,
            custom_llm_provider=custom_llm_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )


def delete(
    arr: ArrayLike,
    obj: ArrayLike | slice,
    axis: int | None = None,
    *,
    assume_unique_indices: bool = False,
) -> Array:
  """Delete entry or entries from an array.

  JAX implementation of :func:`numpy.delete`.

  Args:
    arr: array from which entries will be deleted.
    obj: index, indices, or slice to be deleted.
    axis: axis along which entries will be deleted.
    assume_unique_indices: In case of array-like integer (not boolean) indices,
      assume the indices are unique, and perform the deletion in a way that is
      compatible with JIT and other JAX transformations.

  Returns:
    Copy of ``arr`` with specified indices deleted.

  Note:
    ``delete()`` usually requires the index specification to be static. If the
    index is an integer array that is guaranteed to contain unique entries, you
    may specify ``assume_unique_indices=True`` to perform the operation in a
    manner that does not require static indices.

  See also:
    - :func:`jax.numpy.insert`: insert entries into an array.

  Examples:
    Delete entries from a 1D array:

    >>> a = jnp.array([4, 5, 6, 7, 8, 9])
    >>> jnp.delete(a, 2)
    Array([4, 5, 7, 8, 9], dtype=int32)
    >>> jnp.delete(a, slice(1, 4))  # delete a[1:4]
    Array([4, 8, 9], dtype=int32)
    >>> jnp.delete(a, slice(None, None, 2))  # delete a[::2]
    Array([5, 7, 9], dtype=int32)

    Delete entries from a 2D array along a specified axis:

    >>> a2 = jnp.array([[4, 5, 6],
    ...                 [7, 8, 9]])
    >>> jnp.delete(a2, 1, axis=1)
    Array([[4, 6],
           [7, 9]], dtype=int32)

    Delete multiple entries via a sequence of indices:

    >>> indices = jnp.array([0, 1, 3])
    >>> jnp.delete(a, indices)
    Array([6, 8, 9], dtype=int32)

    This will fail under :func:`~jax.jit` and other transformations, because
    the output shape cannot be known with the possibility of duplicate indices:

    >>> jax.jit(jnp.delete)(a, indices)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      ...
    ConcretizationTypeError: Abstract tracer value encountered where concrete value is expected: traced array with shape int32[3].

    If you can ensure that the indices are unique, pass ``assume_unique_indices``
    to allow this to be executed under JIT:

    >>> jit_delete = jax.jit(jnp.delete, static_argnames=['assume_unique_indices'])
    >>> jit_delete(a, indices, assume_unique_indices=True)
    Array([6, 8, 9], dtype=int32)
  """
  a = util.ensure_arraylike("delete", arr)
  if axis is None:
    a = a.ravel()
    axis = 0
  axis = _canonicalize_axis(axis, a.ndim)

  # Case 1: obj is a static integer.
  try:
    obj = operator.index(obj)  # pyrefly: ignore[bad-argument-type]
    obj = _canonicalize_axis(obj, a.shape[axis])
  except TypeError:
    pass
  else:
    idx = tuple(slice(None) for i in range(axis))
    return concatenate([a[idx + (slice(0, obj),)], a[idx + (slice(obj + 1, None),)]], axis=axis)

  # Case 2: obj is a static slice.
  if isinstance(obj, slice):
    obj = arange(a.shape[axis])[obj]
    assume_unique_indices = True

  # Case 3: obj is an array
  # NB: pass both arrays to check for appropriate error message.
  util.check_arraylike("delete", a, obj)
  # Can't use ensure_arraylike here because obj may be static.
  m = getattr(obj, "__jax_array__", None)
  if m is not None:
    obj = m()

  # Case 3a: unique integer indices; delete in a JIT-compatible way
  if issubdtype(_dtype(obj), np.integer) and assume_unique_indices:
    obj_array = asarray(obj).ravel()
    obj_array = clip(
        where(obj_array < 0, obj_array + a.shape[axis], obj_array),
        0,
        a.shape[axis],
    )
    obj_array = sort(obj_array)
    obj_array -= arange(len(obj_array), dtype=obj_array.dtype)
    i = arange(a.shape[axis] - obj_array.size, dtype=obj_array.dtype)
    i += (i[None, :] >= obj_array[:, None]).sum(0, dtype=i.dtype)
    return a[(slice(None),) * axis + (i,)]

  # Case 3b: non-unique indices: must be static.
  obj_array = core.concrete_or_error(np.asarray, obj, "'obj' array argument of jnp.delete()")
  if issubdtype(obj_array.dtype, np.integer):
    # TODO(jakevdp): in theory this could be done dynamically if obj has no duplicates,
    # but this would require the complement of lax.gather.
    mask = np.ones(a.shape[axis], dtype=bool)
    mask[obj_array] = False
  elif obj_array.dtype == bool:
    if obj_array.shape != (a.shape[axis],):
      raise ValueError("np.delete(arr, obj): for boolean indices, obj must be one-dimensional "
                       "with length matching specified axis.")
    mask = ~obj_array
  else:
    raise ValueError(f"np.delete(arr, obj): got obj.dtype={obj_array.dtype}; must be integer or bool.")
  return a[tuple(slice(None) for i in range(axis)) + (mask,)]


def delete(
    bucket_id: Annotated[
        str,
        typer.Argument(
            help="Bucket ID: namespace/bucket_name or hf://buckets/namespace/bucket_name",
        ),
    ],
    yes: Annotated[
        bool,
        typer.Option(
            "--yes",
            "-y",
            help="Skip confirmation prompt.",
        ),
    ] = False,
    missing_ok: Annotated[
        bool,
        typer.Option(
            "--missing-ok",
            help="Do not raise an error if the bucket does not exist.",
        ),
    ] = False,
    token: TokenOpt = None,
) -> None:
    """Delete a bucket.

    This deletes the entire bucket and all its contents. Use `hf buckets rm` to remove individual files.
    """
    if bucket_id.startswith(BUCKET_PREFIX):
        parsed = _parse_bucket_uri(bucket_id)
        if parsed.path_in_repo:
            raise typer.BadParameter(
                f"Cannot specify a prefix for bucket deletion: {bucket_id}."
                f" Use namespace/bucket_name or {BUCKET_PREFIX}namespace/bucket_name."
            )
        bucket_id = parsed.id
    elif "/" not in bucket_id:
        raise typer.BadParameter(
            f"Invalid bucket ID: {bucket_id}."
            f" Must be in format namespace/bucket_name or {BUCKET_PREFIX}namespace/bucket_name."
        )

    out.confirm(f"Are you sure you want to delete bucket '{bucket_id}'?", yes=yes)

    api = get_hf_api(token=token)
    api.delete_bucket(bucket_id, missing_ok=missing_ok)
    out.result("Bucket deleted", bucket_id=bucket_id)


def delete(
    name: NameArg,
    namespace: NamespaceOpt = None,
    yes: Annotated[
        bool,
        typer.Option("--yes", help="Skip confirmation prompts."),
    ] = False,
    token: TokenOpt = None,
) -> None:
    """Delete an Inference Endpoint permanently."""
    out.confirm(f"Delete endpoint '{name}'?", yes=yes)

    api = get_hf_api(token=token)
    try:
        api.delete_inference_endpoint(name=name, namespace=namespace, token=token)
    except HfHubHTTPError as error:
        out.error(f"Delete failed: {error}")
        raise typer.Exit(code=error.response.status_code) from error

    out.result(f"Deleted '{name}'.", name=name)

