import json
from typing import Any, Dict, List, Optional, Union

def create(
    meta_schema: referencing.jsonschema.ObjectSchema,
    validators: (
        Mapping[str, _typing.SchemaKeywordValidator]
        | Iterable[tuple[str, _typing.SchemaKeywordValidator]]
    ) = (),
    version: str | None = None,
    type_checker: _types.TypeChecker = _types.draft202012_type_checker,
    format_checker: _format.FormatChecker = _format.draft202012_format_checker,
    id_of: _typing.id_of = referencing.jsonschema.DRAFT202012.id_of,
    applicable_validators: _typing.ApplicableValidators = methodcaller(
        "items",
    ),
) -> type[Validator]:
    """
    Create a new validator class.

    Arguments:

        meta_schema:

            the meta schema for the new validator class

        validators:

            a mapping from names to callables, where each callable will
            validate the schema property with the given name.

            Each callable should take 4 arguments:

                1. a validator instance,
                2. the value of the property being validated within the
                   instance
                3. the instance
                4. the schema

        version:

            an identifier for the version that this validator class will
            validate. If provided, the returned validator class will
            have its ``__name__`` set to include the version, and also
            will have `jsonschema.validators.validates` automatically
            called for the given version.

        type_checker:

            a type checker, used when applying the :kw:`type` keyword.

            If unprovided, a `jsonschema.TypeChecker` will be created
            with a set of default types typical of JSON Schema drafts.

        format_checker:

            a format checker, used when applying the :kw:`format` keyword.

            If unprovided, a `jsonschema.FormatChecker` will be created
            with a set of default formats typical of JSON Schema drafts.

        id_of:

            A function that given a schema, returns its ID.

        applicable_validators:

            A function that, given a schema, returns the list of
            applicable schema keywords and associated values
            which will be used to validate the instance.
            This is mostly used to support pre-draft 7 versions of JSON Schema
            which specified behavior around ignoring keywords if they were
            siblings of a ``$ref`` keyword. If you're not attempting to
            implement similar behavior, you can typically ignore this argument
            and leave it at its default.

    Returns:

        a new `jsonschema.protocols.Validator` class

    """
    # preemptively don't shadow the `Validator.format_checker` local
    format_checker_arg = format_checker

    specification = referencing.jsonschema.specification_with(
        dialect_id=id_of(meta_schema) or "urn:unknown-dialect",
        default=referencing.Specification.OPAQUE,
    )

    @define
    class Validator:

        VALIDATORS = dict(validators)  # noqa: RUF012
        META_SCHEMA = dict(meta_schema)  # noqa: RUF012
        TYPE_CHECKER = type_checker
        FORMAT_CHECKER = format_checker_arg
        ID_OF = staticmethod(id_of)

        _APPLICABLE_VALIDATORS = applicable_validators
        _validators = field(init=False, repr=False, eq=False)

        schema: referencing.jsonschema.Schema = field(repr=reprlib.repr)
        _ref_resolver = field(default=None, repr=False, alias="resolver")
        format_checker: _format.FormatChecker | None = field(default=None)
        # TODO: include new meta-schemas added at runtime
        _registry: referencing.jsonschema.SchemaRegistry = field(
            default=_REMOTE_WARNING_REGISTRY,
            kw_only=True,
            repr=False,
        )
        _resolver = field(
            alias="_resolver",
            default=None,
            kw_only=True,
            repr=False,
        )

        def __init_subclass__(cls):
            warnings.warn(
                (
                    "Subclassing validator classes is not intended to "
                    "be part of their public API. A future version "
                    "will make doing so an error, as the behavior of "
                    "subclasses isn't guaranteed to stay the same "
                    "between releases of jsonschema. Instead, prefer "
                    "composition of validators, wrapping them in an object "
                    "owned entirely by the downstream library."
                ),
                DeprecationWarning,
                stacklevel=2,
            )

            def evolve(self, **changes):
                cls = self.__class__
                schema = changes.setdefault("schema", self.schema)
                NewValidator = validator_for(schema, default=cls)

                for field in fields(cls):  # noqa: F402
                    if not field.init:
                        continue
                    attr_name = field.name
                    init_name = field.alias
                    if init_name not in changes:
                        changes[init_name] = getattr(self, attr_name)

                return NewValidator(**changes)

            cls.evolve = evolve

        def __attrs_post_init__(self):
            if self._resolver is None:
                registry = self._registry
                if registry is not _REMOTE_WARNING_REGISTRY:
                    registry = SPECIFICATIONS.combine(registry)
                resource = specification.create_resource(self.schema)
                self._resolver = registry.resolver_with_root(resource)

            if self.schema is True or self.schema is False:
                self._validators = []
            else:
                self._validators = [
                    (self.VALIDATORS[k], k, v)
                    for k, v in applicable_validators(self.schema)
                    if k in self.VALIDATORS
                ]

            # REMOVEME: Legacy ref resolution state management.
            push_scope = getattr(self._ref_resolver, "push_scope", None)
            if push_scope is not None:
                id = id_of(self.schema)
                if id is not None:
                    push_scope(id)

        @classmethod
        def check_schema(cls, schema, format_checker=_UNSET):
            Validator = validator_for(cls.META_SCHEMA, default=cls)
            if format_checker is _UNSET:
                format_checker = Validator.FORMAT_CHECKER
            validator = Validator(
                schema=cls.META_SCHEMA,
                format_checker=format_checker,
            )
            for error in validator.iter_errors(schema):
                raise exceptions.SchemaError.create_from(error)

        @property
        def resolver(self):
            warnings.warn(
                (
                    f"Accessing {self.__class__.__name__}.resolver is "
                    "deprecated as of v4.18.0, in favor of the "
                    "https://github.com/python-jsonschema/referencing "
                    "library, which provides more compliant referencing "
                    "behavior as well as more flexible APIs for "
                    "customization."
                ),
                DeprecationWarning,
                stacklevel=2,
            )
            if self._ref_resolver is None:
                self._ref_resolver = _RefResolver.from_schema(
                    self.schema,
                    id_of=id_of,
                )
            return self._ref_resolver

        def evolve(self, **changes):
            schema = changes.setdefault("schema", self.schema)
            NewValidator = validator_for(schema, default=self.__class__)

            for (attr_name, init_name) in evolve_fields:
                if init_name not in changes:
                    changes[init_name] = getattr(self, attr_name)

            return NewValidator(**changes)

        def iter_errors(self, instance, _schema=None):
            if _schema is not None:
                warnings.warn(
                    (
                        "Passing a schema to Validator.iter_errors "
                        "is deprecated and will be removed in a future "
                        "release. Call validator.evolve(schema=new_schema)."
                        "iter_errors(...) instead."
                    ),
                    DeprecationWarning,
                    stacklevel=2,
                )
                validators = [
                    (self.VALIDATORS[k], k, v)
                    for k, v in applicable_validators(_schema)
                    if k in self.VALIDATORS
                ]
            else:
                _schema, validators = self.schema, self._validators

            if _schema is True:
                return
            elif _schema is False:
                yield exceptions.ValidationError(
                    f"False schema does not allow {instance!r}",
                    validator=None,
                    validator_value=None,
                    instance=instance,
                    schema=_schema,
                )
                return

            for validator, k, v in validators:
                errors = validator(self, v, instance, _schema) or ()
                for error in errors:
                    # set details if not already set by the called fn
                    error._set(
                        validator=k,
                        validator_value=v,
                        instance=instance,
                        schema=_schema,
                        type_checker=self.TYPE_CHECKER,
                    )
                    if k not in {"if", "$ref"}:
                        error.schema_path.appendleft(k)
                    yield error

        def descend(
            self,
            instance,
            schema,
            path=None,
            schema_path=None,
            resolver=None,
        ):
            if schema is True:
                return
            elif schema is False:
                yield exceptions.ValidationError(
                    f"False schema does not allow {instance!r}",
                    validator=None,
                    validator_value=None,
                    instance=instance,
                    schema=schema,
                )
                return

            if self._ref_resolver is not None:
                evolved = self.evolve(schema=schema)
            else:
                if resolver is None:
                    resolver = self._resolver.in_subresource(
                        specification.create_resource(schema),
                    )
                evolved = self.evolve(schema=schema, _resolver=resolver)

            for k, v in applicable_validators(schema):
                validator = evolved.VALIDATORS.get(k)
                if validator is None:
                    continue

                errors = validator(evolved, v, instance, schema) or ()
                for error in errors:
                    # set details if not already set by the called fn
                    error._set(
                        validator=k,
                        validator_value=v,
                        instance=instance,
                        schema=schema,
                        type_checker=evolved.TYPE_CHECKER,
                    )
                    if k not in {"if", "$ref"}:
                        error.schema_path.appendleft(k)
                    if path is not None:
                        error.path.appendleft(path)
                    if schema_path is not None:
                        error.schema_path.appendleft(schema_path)
                    yield error

        def validate(self, *args, **kwargs):
            for error in self.iter_errors(*args, **kwargs):
                raise error

        def is_type(self, instance, type):
            try:
                return self.TYPE_CHECKER.is_type(instance, type)
            except exceptions.UndefinedTypeCheck:
                exc = exceptions.UnknownType(type, instance, self.schema)
                raise exc from None

        def _validate_reference(self, ref, instance):
            if self._ref_resolver is None:
                try:
                    resolved = self._resolver.lookup(ref)
                except referencing.exceptions.Unresolvable as err:
                    raise exceptions._WrappedReferencingError(err) from err

                return self.descend(
                    instance,
                    resolved.contents,
                    resolver=resolved.resolver,
                )
            else:
                resolve = getattr(self._ref_resolver, "resolve", None)
                if resolve is None:
                    with self._ref_resolver.resolving(ref) as resolved:
                        return self.descend(instance, resolved)
                else:
                    scope, resolved = resolve(ref)
                    self._ref_resolver.push_scope(scope)

                    try:
                        return list(self.descend(instance, resolved))
                    finally:
                        self._ref_resolver.pop_scope()

        def is_valid(self, instance, _schema=None):
            if _schema is not None:
                warnings.warn(
                    (
                        "Passing a schema to Validator.is_valid is deprecated "
                        "and will be removed in a future release. Call "
                        "validator.evolve(schema=new_schema).is_valid(...) "
                        "instead."
                    ),
                    DeprecationWarning,
                    stacklevel=2,
                )
                self = self.evolve(schema=_schema)

            error = next(self.iter_errors(instance), None)
            return error is None

    evolve_fields = [
        (field.name, field.alias)
        for field in fields(Validator)
        if field.init
    ]

    if version is not None:
        safe = version.title().replace(" ", "").replace("-", "")
        Validator.__name__ = Validator.__qualname__ = f"{safe}Validator"
        Validator = validates(version)(Validator)  # type: ignore[misc]

    return Validator  # type: ignore[return-value]


def create(**kwargs):
  """Creates a `ConfigDict` with the given named arguments as key-value pairs.

  This allows for simple dictionaries whose elements can be accessed directly
  using field access::

    from ml_collections import config_dict
    point = config_dict.create(x=1, y=2)
    print(point.x, point.y)

  This is particularly useful for compactly writing nested configurations::

    config = config_dict.create(
      data=config_dict.create(
        game='freeway',
        frame_size=100),
      model=config_dict.create(num_hidden=1000))

  The reason for the existence of this function is that it simplifies the
  code required for the majority of the use cases of `ConfigDict`, compared
  to using either `ConfigDict` or `namedtuple's`. Examples of such use cases
  include training script configuration, and returning multiple named values.

  Args:
    **kwargs: key-value pairs to be stored in the `ConfigDict`.

  Returns:
    A `ConfigDict` containing the key-value pairs in `kwargs`.
  """
  return ConfigDict(initial_dictionary=kwargs)


def create(
    # Model or Agent (one required per OpenAPI spec)
    model: Optional[str] = None,
    agent: Optional[str] = None,
    # Input (required)
    input: Optional[InteractionInput] = None,
    # Tools (for model interactions)
    tools: Optional[List[InteractionTool]] = None,
    # System instruction
    system_instruction: Optional[str] = None,
    # Generation config
    generation_config: Optional[Dict[str, Any]] = None,
    # Streaming
    stream: Optional[bool] = None,
    # Storage
    store: Optional[bool] = None,
    # Background execution
    background: Optional[bool] = None,
    # Agent execution environment ("remote", env id, or remote config object)
    environment: Optional[InteractionEnvironment] = None,
    # Response format
    response_modalities: Optional[List[str]] = None,
    response_format: Optional[Dict[str, Any]] = None,
    response_mime_type: Optional[str] = None,
    # Continuation
    previous_interaction_id: Optional[str] = None,
    # Extra params
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    # LiteLLM params
    custom_llm_provider: Optional[str] = None,
    **kwargs,
) -> Union[
    InteractionsAPIResponse,
    Iterator[InteractionsAPIStreamingResponse],
    Coroutine[
        Any,
        Any,
        Union[InteractionsAPIResponse, AsyncIterator[InteractionsAPIStreamingResponse]],
    ],
]:
    """
    Sync: Create a new interaction using Google's Interactions API.

    Per OpenAPI spec, provide either `model` or `agent`.

    Args:
        model: The model to use (e.g., "gemini-2.5-flash")
        agent: The agent to use (e.g., "deep-research-pro-preview-12-2025")
        input: The input content (string, content object, or list)
        tools: Tools available for the model
        system_instruction: System instruction for the interaction
        generation_config: Generation configuration
        stream: Whether to stream the response
        store: Whether to store the response for later retrieval
        background: Whether to run in background
        environment: Agent execution environment — ``"remote"``, an existing env id
            string, or a config object such as
            ``{"type": "remote", "sources": [...]}`` /
            ``{"type": "remote", "network": {...}}``
        response_modalities: Requested response modalities (TEXT, IMAGE, AUDIO)
        response_format: JSON schema for response format
        response_mime_type: MIME type of the response
        previous_interaction_id: ID of previous interaction for continuation
        extra_headers: Additional headers
        extra_body: Additional body parameters
        timeout: Request timeout
        custom_llm_provider: Override the LLM provider

    Returns:
        InteractionsAPIResponse or iterator for streaming
    """
    local_vars = locals()

    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
        _is_async = kwargs.pop("acreate_interaction", False) is True

        litellm_params = GenericLiteLLMParams(**kwargs)

        # Routing logic:
        # - agent provided (no model, or model accidentally set to agent name) → gemini
        # - model provided → resolve provider via get_llm_provider (normal routing)
        if agent and model == agent:
            model = None
        if agent and not model:
            custom_llm_provider = custom_llm_provider or "gemini"
        elif model:
            model, custom_llm_provider, _, _ = litellm.get_llm_provider(
                model=model,
                custom_llm_provider=custom_llm_provider,
                api_base=litellm_params.api_base,
                api_key=litellm_params.api_key,
            )
        else:
            custom_llm_provider = custom_llm_provider or "gemini"

        interactions_api_config = get_provider_interactions_api_config(
            provider=custom_llm_provider,
            model=model,
        )

        # Get optional params using utility (similar to responses API pattern)
        local_vars.update(kwargs)
        optional_params = (
            InteractionsAPIRequestUtils.get_requested_interactions_api_optional_params(
                local_vars
            )
        )

        # Check if this is a bridge provider (litellm_responses) - similar to responses API
        # Either provider is explicitly "litellm_responses" or no config found (bridge to responses)
        if (
            custom_llm_provider == "litellm_responses"
            or interactions_api_config is None
        ):
            # Bridge to litellm.responses() for non-native providers
            from litellm.interactions.litellm_responses_transformation.handler import (
                LiteLLMResponsesInteractionsHandler,
            )

            handler = LiteLLMResponsesInteractionsHandler()
            return handler.interactions_api_handler(
                model=model or "",
                input=input,
                optional_params=optional_params,
                custom_llm_provider=custom_llm_provider,
                _is_async=_is_async,
                stream=stream,
                **kwargs,
            )

        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model=model,
            optional_params=dict(optional_params),
            litellm_params={"litellm_call_id": litellm_call_id},
            custom_llm_provider=custom_llm_provider,
        )

        response = interactions_http_handler.create_interaction(
            model=model,
            agent=agent,
            input=input,
            interactions_api_config=interactions_api_config,
            optional_params=optional_params,
            custom_llm_provider=custom_llm_provider,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            extra_headers=extra_headers,
            extra_body=extra_body,
            timeout=timeout,
            _is_async=_is_async,
            stream=stream,
        )

        return response
    except Exception as e:
        raise litellm.exception_type(
            model=model,
            custom_llm_provider=custom_llm_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )


def create(
    name: Optional[str] = None,
    file_ids: Optional[List[str]] = None,
    expires_after: Optional[Dict] = None,
    chunking_strategy: Optional[Dict] = None,
    metadata: Optional[Dict[str, str]] = None,
    # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
    # The extra values given here take precedence over values defined on the client or passed to this method.
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    # LiteLLM specific params,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
) -> Union[VectorStoreCreateResponse, Coroutine[Any, Any, VectorStoreCreateResponse]]:
    """
    Create a vector store.

    Args:
        name: The name of the vector store.
        file_ids: A list of File IDs that the vector store should use.
        expires_after: The expiration policy for the vector store.
        chunking_strategy: The chunking strategy used to chunk the file(s).
        metadata: Set of 16 key-value pairs that can be attached to an object.

    Returns:
        VectorStoreCreateResponse containing the created vector store details.
    """
    local_vars = locals()
    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
        _is_async = kwargs.pop("acreate", False) is True

        # get llm provider logic
        litellm_params = GenericLiteLLMParams(**kwargs)

        ## MOCK RESPONSE LOGIC
        if litellm_params.mock_response and isinstance(
            litellm_params.mock_response, dict
        ):
            return mock_vector_store_create_response(
                mock_response=VectorStoreCreateResponse(**litellm_params.mock_response)
            )

        # Default to OpenAI for vector stores
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

        # get provider config - using vector store custom logger for now
        vector_store_provider_config = (
            ProviderConfigManager.get_provider_vector_stores_config(
                provider=litellm.LlmProviders(custom_llm_provider),
                api_type=api_type,
            )
        )

        if vector_store_provider_config is None:
            raise ValueError(
                f"Vector store create is not supported for {custom_llm_provider}"
            )

        local_vars.update(kwargs)

        # Get VectorStoreCreateOptionalRequestParams with only valid parameters
        vector_store_create_optional_params: VectorStoreCreateOptionalRequestParams = (
            VectorStoreRequestUtils.get_requested_vector_store_create_optional_param(
                local_vars
            )
        )

        # Pre Call logging
        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model=None,
            optional_params={
                "name": name,
                **vector_store_create_optional_params,
            },
            litellm_params={
                "litellm_call_id": litellm_call_id,
            },
            custom_llm_provider=custom_llm_provider,
        )

        response = base_llm_http_handler.vector_store_create_handler(
            vector_store_create_optional_params=vector_store_create_optional_params,
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


def create(
    *,
    vector_store_id: str,
    file_id: str,
    attributes: Optional[VectorStoreFileAttributes] = None,
    chunking_strategy: Optional[Dict[str, Any]] = None,
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
) -> Union[VectorStoreFileObject, Coroutine[Any, Any, VectorStoreFileObject]]:
    local_vars = locals()
    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id")
        _is_async = kwargs.pop("acreate", False) is True

        custom_llm_provider = _ensure_provider(custom_llm_provider)

        _prepare_registry_credentials(vector_store_id=vector_store_id, kwargs=kwargs)

        litellm_params = GenericLiteLLMParams(vector_store_id=vector_store_id, **kwargs)

        provider_config = ProviderConfigManager.get_provider_vector_store_files_config(
            provider=LlmProviders(custom_llm_provider)
        )
        if provider_config is None:
            raise ValueError(
                f"Vector store file create is not supported for {custom_llm_provider}"
            )

        local_vars.update(kwargs)
        create_request: VectorStoreFileCreateRequest = (
            VectorStoreFileRequestUtils.get_create_request_params(local_vars)
        )
        create_request["file_id"] = file_id

        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model=None,
            optional_params={
                "vector_store_id": vector_store_id,
                **create_request,
            },
            litellm_params={
                "vector_store_id": vector_store_id,
                "litellm_call_id": litellm_call_id,
                **litellm_params.model_dump(exclude_none=True),
            },
            custom_llm_provider=custom_llm_provider,
        )

        response = base_llm_http_handler.vector_store_file_create_handler(
            vector_store_id=vector_store_id,
            create_request=create_request,
            vector_store_files_provider_config=provider_config,
            custom_llm_provider=custom_llm_provider,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            extra_headers=extra_headers,
            extra_body=extra_body,
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


def create(ctx: click.Context, credential_name: str, info: str, values: str):
    """Create a new credential"""
    client = CredentialsManagementClient(ctx.obj["base_url"], ctx.obj["api_key"])
    try:
        credential_info = json.loads(info)
        credential_values = json.loads(values)
    except json.JSONDecodeError as e:
        raise click.BadParameter(f"Invalid JSON: {str(e)}")

    try:
        response = client.create(credential_name, credential_info, credential_values)
        rich.print_json(data=response)
    except requests.exceptions.HTTPError as e:
        click.echo(f"Error: HTTP {e.response.status_code}", err=True)
        try:
            error_body = e.response.json()
            rich.print_json(data=error_body)
        except json.JSONDecodeError:
            click.echo(e.response.text, err=True)
        raise click.Abort()


def create(
    name: str,
    base_agent: Optional[str] = None,
    instructions: Optional[str] = None,
    base_environment: Optional[InteractionEnvironment] = None,
    custom_llm_provider: Optional[str] = None,
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    **kwargs,
) -> Union[AgentCreateResponse, Coroutine[Any, Any, AgentCreateResponse]]:
    """
    Sync: Create a managed agent on the provider side.

    Args:
        name: Name for the agent (required).
        base_agent: Base agent to derive from (e.g. "waverunner").
        instructions: System instructions for the agent.
        base_environment: Environment to fork from — an env_id string or a
            dict like ``{"type": "remote", "sources": [...]}``.
        custom_llm_provider: Provider to use, e.g. "gemini".
        extra_headers: Additional HTTP headers.
        extra_body: Additional request body fields.
        timeout: Request timeout.
        **kwargs: Forwarded to GenericLiteLLMParams (api_key, api_base, etc.).
    """
    local_vars = locals()
    custom_llm_provider = (
        custom_llm_provider or kwargs.get("custom_llm_provider") or "gemini"
    )
    try:
        _is_async = kwargs.pop("acreate_agent", False) is True
        if base_agent is not None:
            kwargs["base_agent"] = base_agent
        if instructions is not None:
            kwargs["instructions"] = instructions
        if base_environment is not None:
            kwargs["base_environment"] = base_environment
        kwargs.setdefault("custom_llm_provider", custom_llm_provider)
        litellm_params = GenericLiteLLMParams(**kwargs)
        logging_obj = _make_logging_obj(
            kwargs, name, custom_llm_provider, "create_agent", {}
        )
        config = _get_agents_api_config(custom_llm_provider)
        return agents_http_handler.create_agent(
            agents_api_config=config,
            name=name,
            litellm_params=litellm_params,
            logging_obj=logging_obj,
            extra_headers=extra_headers,
            extra_body=extra_body,
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


def create(
    max_tokens: int,
    messages: List[Dict],
    model: str,
    metadata: Optional[Dict] = None,
    stop_sequences: Optional[List[str]] = None,
    stream: Optional[bool] = False,
    system: Optional[str] = None,
    temperature: Optional[float] = None,
    thinking: Optional[Dict] = None,
    tool_choice: Optional[Dict] = None,
    tools: Optional[List[Dict]] = None,
    top_k: Optional[int] = None,
    top_p: Optional[float] = None,
    container: Optional[Dict] = None,
    **kwargs,
) -> Union[
    AnthropicMessagesResponse,
    Iterator[bytes],
    AsyncIterator[Any],
    Coroutine[
        Any, Any, Union[AnthropicMessagesResponse, AsyncIterator[Any], Iterator[bytes]]
    ],
]:
    """
    Async wrapper for Anthropic's messages API

    Args:
        max_tokens (int): Maximum tokens to generate (required)
        messages (List[Dict]): List of message objects with role and content (required)
        model (str): Model name to use (required)
        metadata (Dict, optional): Request metadata
        stop_sequences (List[str], optional): Custom stop sequences
        stream (bool, optional): Whether to stream the response
        system (str, optional): System prompt
        temperature (float, optional): Sampling temperature (0.0 to 1.0)
        thinking (Dict, optional): Extended thinking configuration
        tool_choice (Dict, optional): Tool choice configuration
        tools (List[Dict], optional): List of tool definitions
        top_k (int, optional): Top K sampling parameter
        top_p (float, optional): Nucleus sampling parameter
        **kwargs: Additional arguments

    Returns:
        Dict: Response from the API
    """
    return _sync_anthropic_messages(
        max_tokens=max_tokens,
        messages=messages,
        model=model,
        metadata=metadata,
        stop_sequences=stop_sequences,
        stream=stream,
        system=system,
        temperature=temperature,
        thinking=thinking,
        tool_choice=tool_choice,
        tools=tools,
        top_k=top_k,
        top_p=top_p,
        container=container,
        **kwargs,
    )


def create(
    bucket_id: Annotated[
        str,
        typer.Argument(
            help="Bucket ID: bucket_name, namespace/bucket_name, or hf://buckets/namespace/bucket_name",
        ),
    ],
    private: Annotated[
        bool,
        typer.Option(
            "--private",
            help="Create a private bucket.",
        ),
    ] = False,
    region: Annotated[
        REPO_REGIONS | None,
        typer.Option(
            "--region",
            help="Cloud region in which to create the bucket. Can be one of 'us' or 'eu'. Requires Team plan or above.",
        ),
    ] = None,
    exist_ok: Annotated[
        bool,
        typer.Option(
            "--exist-ok",
            help="Do not raise an error if the bucket already exists.",
        ),
    ] = False,
    token: TokenOpt = None,
) -> None:
    """Create a new bucket."""
    api = get_hf_api(token=token)

    if bucket_id.startswith(BUCKET_PREFIX):
        parsed = _parse_bucket_uri(bucket_id)
        if parsed.path_in_repo:
            raise typer.BadParameter(
                f"Cannot specify a prefix for bucket creation: {bucket_id}."
                f" Use namespace/bucket_name or {BUCKET_PREFIX}namespace/bucket_name."
            )
        bucket_id = parsed.id

    bucket_url = api.create_bucket(
        bucket_id,
        private=private if private else None,
        region=region,
        exist_ok=exist_ok,
    )
    out.result("Bucket created", uri=bucket_url.uri.to_uri(), url=bucket_url.url)

