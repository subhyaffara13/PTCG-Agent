
def get(
    path: str,
    handler: _HandlerType,
    *,
    name: str | None = None,
    allow_head: bool = True,
    **kwargs: Any,
) -> RouteDef:
    return route(
        hdrs.METH_GET, path, handler, name=name, allow_head=allow_head, **kwargs
    )


def get(ctx: click.Context, key: Any) -> None:
    """Retrieve the value for the given key."""
    file = ctx.obj["FILE"]

    with stream_file(file) as stream:
        values = dotenv_values(stream=stream)

    stored_value = values.get(key)
    if stored_value:
        click.echo(stored_value)
    else:
        sys.exit(1)


def Get(packer_type, buf, head):
  """Get decodes a value at buf[head] using `packer_type`."""
  return packer_type.unpack_from(memoryview_type(buf), head)[0]


def get(
    url: URL | str,
    *,
    params: QueryParamTypes | None = None,
    headers: HeaderTypes | None = None,
    cookies: CookieTypes | None = None,
    auth: AuthTypes | None = None,
    proxy: ProxyTypes | None = None,
    follow_redirects: bool = False,
    verify: ssl.SSLContext | str | bool = True,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
    trust_env: bool = True,
) -> Response:
    """
    Sends a `GET` request.

    **Parameters**: See `httpx.request`.

    Note that the `data`, `files`, `json` and `content` parameters are not available
    on this function, as `GET` requests should not include a request body.
    """
    return request(
        "GET",
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


def get(
    o: Any,
    classinfo: Type | None = None,
    default: Any = None,
    path: list[str] | None = None,
    is_callable: bool | None = None,
    fallback: Any = None,
) -> Any:
    if path is None:
        path = []
    if o is None and default is not None:
        o = default
    if has(o, classinfo, default, path, is_callable):
        cur = o
        for p in path:
            cur = cur[p]
        return cur
    else:
        if default is not None:
            return default
        return fallback


def get(obj, *args, **kwargs):
    return matplotlib.artist.get(obj, *args, **kwargs)


def get():
    """get() -> list of Events
    get all events from the queue
    """
    _ft_init_check()
    return pygame.event.get()


def get(
    url: _t.UriType, params: _t.ParamsType = None, **kwargs: Unpack[_t.GetKwargs]
) -> Response:
    r"""Sends a GET request.

    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    return request("get", url, params=params, **kwargs)


def get(ind, seq, default=no_default):
    """ Get element in a sequence or dict

    Provides standard indexing

    >>> get(1, 'ABC')       # Same as 'ABC'[1]
    'B'

    Pass a list to get multiple values

    >>> get([1, 2], 'ABC')  # ('ABC'[1], 'ABC'[2])
    ('B', 'C')

    Works on any value that supports indexing/getitem
    For example here we see that it works with dictionaries

    >>> phonebook = {'Alice':  '555-1234',
    ...              'Bob':    '555-5678',
    ...              'Charlie':'555-9999'}
    >>> get('Alice', phonebook)
    '555-1234'

    >>> get(['Alice', 'Bob'], phonebook)
    ('555-1234', '555-5678')

    Provide a default for missing values

    >>> get(['Alice', 'Dennis'], phonebook, None)
    ('555-1234', None)

    See Also:
        pluck
    """
    try:
        return seq[ind]
    except TypeError:  # `ind` may be a list
        if isinstance(ind, list):
            if default == no_default:
                if len(ind) > 1:
                    return operator.itemgetter(*ind)(seq)
                elif ind:
                    return seq[ind[0]],
                else:
                    return ()
            else:
                return tuple(_get(i, seq, default) for i in ind)
        elif default != no_default:
            return default
        else:
            raise
    except (KeyError, IndexError):  # we know `ind` is not a list
        if default == no_default:
            raise
        else:
            return default


def get(name):
    return docdict.get(name)


def get(url, params=None, **kwargs):
    r"""Sends a GET request.

    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    return request("get", url, params=params, **kwargs)


def get(
    interaction_id: str,
    extra_headers: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
) -> Union[InteractionsAPIResponse, Coroutine[Any, Any, InteractionsAPIResponse]]:
    """Sync: Get an interaction by its ID."""
    local_vars = locals()
    custom_llm_provider = custom_llm_provider or "gemini"

    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
        _is_async = kwargs.pop("aget_interaction", False) is True

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

        return interactions_http_handler.get_interaction(
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


def get(ctx: click.Context, credential_name: str):
    """Get a credential by name"""
    client = CredentialsManagementClient(ctx.obj["base_url"], ctx.obj["api_key"])
    response = client.get(credential_name)
    rich.print_json(data=response)


def get(
    name: str,
    custom_llm_provider: Optional[str] = None,
    extra_headers: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    **kwargs,
) -> Union[AgentCreateResponse, Coroutine[Any, Any, AgentCreateResponse]]:
    """Sync: Get a specific agent by name."""
    local_vars = locals()
    custom_llm_provider = (
        custom_llm_provider or kwargs.get("custom_llm_provider") or "gemini"
    )
    try:
        _is_async = kwargs.pop("aget_agent", False) is True
        kwargs.setdefault("custom_llm_provider", custom_llm_provider)
        litellm_params = GenericLiteLLMParams(**kwargs)
        logging_obj = _make_logging_obj(
            kwargs, name, custom_llm_provider, "get_agent", {"name": name}
        )
        config = _get_agents_api_config(custom_llm_provider)
        return agents_http_handler.get_agent(
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


def get(d, key, default):
    if isinstance(d, dict):
        return d.get(key, default)
    return getattr(d, key, default)


def get(d, key, default):
    if isinstance(d, dict):
        return d.get(key, default)
    return getattr(d, key, default)


def get(d, key, default):
    """Helper to get from dict or SimpleNamespace."""
    if isinstance(d, dict):
        return d.get(key, default)
    return getattr(d, key, default)


def get(
    module: ir.Module,
    devices: np.ndarray,
    compile_options: xla_client.CompileOptions,
    backend: xla_client.Client,
    compression_algorithm: str = "zstandard",
    ignore_callbacks: IgnoreCallbacks = IgnoreCallbacks.NO,
) -> str:
  """Creates a hashed string to use as a key to the compilation cache.

  Creates a cache key that is a hex-encoded string of a unique hash based on
  the arguments. The hex-encoded string is 256 characters long.

  Args:
    module: the input program
    devices: an array of accelerator devices that the program will run on
    compile_options: options passed to the XLA compiler
    backend: description of the platform (e.g., TPU version)
    compression_algorithm: a string representing the compression algorithm used
      for the executable before persisting in the cache
    ignore_callbacks: whether to remove the all callback pointer from the
      computation.

  Typical return value example:
   'jit__psum-14ac577cdb2ef6d986078b4054cc9893a9a14a16dbb0d8f37b89167c1f1aacdf'
  """
  entries = [
      (
          "computation",
          lambda hash_obj: _hash_computation(
              hash_obj, module, ignore_callbacks
          ),
      ),
      (
          "jax_lib version",
          lambda hash_obj: hash_obj.update(
              bytes(jaxlib_version_str.encode("utf-8"))
          ),
      ),
      (
          "backend version",
          lambda hash_obj: _hash_platform(hash_obj, backend)
      ),
      (
          "XLA flags",
          lambda hash_obj: _hash_xla_flags(hash_obj, get_flag_prefixes()),
      ),
      (
          "compile_options",
          lambda hash_obj: _hash_serialized_compile_options(
              hash_obj,
              compile_options,
              # In case of GPU multi-process tasks we need to strip device
              # assignment to use cache key as invariant between processes.
              strip_device_assignment=(backend.platform == "gpu"),
          ),
      ),
      (
          "accelerator_config",
          lambda hash_obj: _hash_accelerator_config(hash_obj, devices),
      ),
      (
          "compression",
          lambda hash_obj: _hash_string(hash_obj, compression_algorithm),
      ),
      ("custom_hook", lambda hash_obj: _hash_string(hash_obj, custom_hook())),
  ]

  hash_obj = hashlib.sha256()
  for name, hashfn in entries:
    hashfn(hash_obj)
    _log_cache_key_hash(hash_obj, name, hashfn)
  sym_name = module.operation.attributes['sym_name']
  module_name = ir.StringAttr(sym_name).value
  return module_name + "-" + hash_obj.digest().hex()


def get(
    token,
    device_id,
    local_core_id,
    memory_space,
    buffer_id,
    transforms,
    block_indices=None,
    grid_loop_idx=None,
    *,
    src_device_id=None,
    src_local_core_id=None,
    clock=None,
    source_info=None,
    input_name=None,
) -> tuple[Token, np.ndarray]:
  device_id = int(device_id)
  local_core_id = int(local_core_id)
  memory_space = TPU_MEMORY_SPACE_NAMES[int(memory_space)]
  buffer_id = int(buffer_id)
  try:
    transforms = jax.tree.map(int, transforms)
  except:
    raise ValueError('Advanced indexers are not supported on TPU')
  src_device_id = _to_int(src_device_id)
  src_local_core_id = _to_int(src_local_core_id)
  if input_name is not None:
    # NOTE: input_name, block_indices, and grid_loop_idx are set only if this
    # function is being called to read a block from a pallas_call input (at the
    # start of one iteration of the kernel body).
    assert block_indices is not None
    block_indices = tuple(int(x) for x in block_indices)
    assert grid_loop_idx is not None
    grid_loop_idx = tuple(int(x) for x in tuple(grid_loop_idx))

  shared_memory = _get_shared_memory()

  local_core_id_for_buffer = _local_core_id_or_zero_if_hbm(
      local_core_id, memory_space
  )
  global_core_id = shared_memory.get_global_core_id(device_id, local_core_id)

  key = (memory_space, buffer_id, device_id, local_core_id_for_buffer)
  read_range = interpret_utils.to_range(transforms)
  ret, (shape, dtype), clock_ = shared_memory.get_buffer_content(
      key,
      read_range,
      global_core_id,
      logging_info=interpret_utils.TPULoggingInfo(
          device_id=device_id,
          local_core_id=local_core_id,
          source_info=source_info,
      ),
  )
  clock = clock if clock is not None else clock_

  # Compute the shape of the read value, assuming the read is fully in-bounds.
  # TODO(jburnim): We already know this shape in the Jaxpr where we insert a
  # callback to `get`.  Should we just pass the shape to `get`?
  # TODO(jburnim): Move to a helper function?
  full_read_shape: list[int] = []
  assert len(read_range) <= len(shape)
  for dim_size, idx_or_slice in itertools.zip_longest(
      shape, read_range, fillvalue=None
  ):
    assert isinstance(dim_size, int)
    if idx_or_slice is None:
      full_read_shape.append(dim_size)
    elif isinstance(idx_or_slice, int):
      continue
    else:
      dim_size = (idx_or_slice.stop - idx_or_slice.start) // idx_or_slice.step
      assert isinstance(dim_size, int)
      full_read_shape.append(dim_size)

  if (ret is None) or (tuple(full_read_shape) != ret.shape):
    if shared_memory.out_of_bounds_reads == 'raise':
      if source_info is None:
        ctx = contextlib.nullcontext()
      else:
        ctx = source_info_util.user_context(
            traceback=source_info.traceback, name_stack=source_info.name_stack
        )
      with ctx:
        if input_name is None:
          raise IndexError(
              'Out-of-bounds read of'
              f' ({device_id} {local_core_id} {memory_space} {buffer_id}):'
              f' reading [{read_range}] but buffer has shape {shape}.'
          )
        else:
          # Different error message when we are reading a block of an input,
          # to copy it to a buffer before invoking the kernel body.
          raise IndexError(
              f'Out-of-bounds block index {block_indices} for'
              f' input "{input_name}" in iteration {grid_loop_idx}'
              f' on device {device_id} (core {local_core_id}):'
              f' reading [{read_range}] but input has shape {shape}.'
          )
    # out_of_bounds_reads == "uninitialized"
    uninit_array = np.full(
        full_read_shape,
        interpret_utils.get_uninitialized_value(
            dtype, shared_memory.uninitialized_memory
        ),
        dtype=dtype,
    )
    if ret is None:
      ret = uninit_array
    else:
      uninit_array[tuple(slice(s) for s in ret.shape)] = ret
      ret = uninit_array

  if shared_memory.detect_races:
    if src_device_id is None:
      src_device_id = device_id
    if src_local_core_id is None:
      src_local_core_id = local_core_id
    assert races is not None
    races.check_read(
        src_device_id,
        src_local_core_id,
        clock,
        (memory_space, buffer_id, device_id, local_core_id_for_buffer),
        read_range,
        source_info=source_info,
    )

  return token, ret


def get(
    request,
    path,
    root=None,
    params=None,
    recursive=False,
    retry_count=5,
    headers=None,
    return_none_for_not_found_error=False,
    timeout=_METADATA_DEFAULT_TIMEOUT,
):
    """Fetch a resource from the metadata server.

    Args:
        request (google.auth.transport.Request): A callable used to make
            HTTP requests.
        path (str): The resource to retrieve. For example,
            ``'instance/service-accounts/default'``.
        root (Optional[str]): The full path to the metadata server root. If not
            provided, the default root will be used.
        params (Optional[Mapping[str, str]]): A mapping of query parameter
            keys to values.
        recursive (bool): Whether to do a recursive query of metadata. See
            https://cloud.google.com/compute/docs/metadata#aggcontents for more
            details.
        retry_count (int): How many times to attempt connecting to metadata
            server using above timeout.
        headers (Optional[Mapping[str, str]]): Headers for the request.
        return_none_for_not_found_error (Optional[bool]): If True, returns None
            for 404 error instead of throwing an exception.
        timeout (int): How long to wait, in seconds for the metadata server to respond.

    Returns:
        Union[Mapping, str]: If the metadata server returns JSON, a mapping of
            the decoded JSON is returned. Otherwise, the response content is
            returned as a string.

    Raises:
        google.auth.exceptions.TransportError: if an error occurred while
            retrieving metadata.
        google.auth.exceptions.MutualTLSChannelError: if using mtls and the environment
            configuration is invalid for mTLS (for example, the metadata host
            has been overridden in strict mTLS mode).

    """
    use_mtls = _mtls.should_use_mds_mtls()
    # Prepare the request object for mTLS if needed.
    # This will create a new request object with the mTLS session.
    _prepare_request_for_mds(request, use_mtls=use_mtls)

    if root is None:
        root = _get_metadata_root(use_mtls)

    # mTLS is only supported when connecting to the default metadata host.
    # If we are in strict mode (which requires mTLS), ensure that the metadata host
    # has not been overridden to a non-default host value (which means mTLS will fail).
    _validate_gce_mds_configured_environment()

    base_url = urljoin(root, path)
    query_params = {} if params is None else params

    headers_to_use = _METADATA_HEADERS.copy()
    if headers:
        headers_to_use.update(headers)

    if recursive:
        query_params["recursive"] = "true"

    url = _helpers.update_query(base_url, query_params)

    backoff = ExponentialBackoff(total_attempts=retry_count)
    last_exception = None
    for attempt in backoff:
        try:
            response = request(
                url=url, method="GET", headers=headers_to_use, timeout=timeout
            )
            if response.status in transport.DEFAULT_RETRYABLE_STATUS_CODES:
                _LOGGER.warning(
                    "Compute Engine Metadata server unavailable on "
                    "attempt %s of %s. Response status: %s",
                    attempt,
                    retry_count,
                    response.status,
                )
                last_exception = None
                continue
            else:
                last_exception = None
                break

        except exceptions.TransportError as e:
            _LOGGER.warning(
                "Compute Engine Metadata server unavailable on "
                "attempt %s of %s. Reason: %s",
                attempt,
                retry_count,
                e,
            )
            last_exception = e
    else:
        if last_exception:
            raise exceptions.TransportError(
                "Failed to retrieve {} from the Google Compute Engine "
                "metadata service. Compute Engine Metadata server unavailable. "
                "Last exception: {}".format(url, last_exception)
            ) from last_exception
        else:
            error_details = (
                response.data.decode("utf-8")
                if hasattr(response.data, "decode")
                else response.data
            )
            raise exceptions.TransportError(
                "Failed to retrieve {} from the Google Compute Engine "
                "metadata service. Compute Engine Metadata server unavailable. "
                "Response status: {}\nResponse details:\n{}".format(
                    url, response.status, error_details
                )
            )

    content = _helpers.from_bytes(response.data)

    if response.status == http_client.NOT_FOUND and return_none_for_not_found_error:
        return None

    if response.status == http_client.OK:
        if (
            _helpers.parse_content_type(response.headers["content-type"])
            == "application/json"
        ):
            try:
                return json.loads(content)
            except ValueError as caught_exc:
                new_exc = exceptions.TransportError(
                    "Received invalid JSON from the Google Compute Engine "
                    "metadata service: {:.20}".format(content)
                )
                raise new_exc from caught_exc
        else:
            return content

    raise exceptions.TransportError(
        "Failed to retrieve {} from the Google Compute Engine "
        "metadata service. Status: {} Response:\n{}".format(
            url, response.status, response.data
        ),
        response,
    )

