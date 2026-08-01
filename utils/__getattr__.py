
def __getattr__(name):
    if name == "HeuristicValueNetwork":
        from cb_agents.heuristic_value import HeuristicValueNetwork
        return HeuristicValueNetwork
    raise AttributeError(f"module {__name__} no attr {name}")


def __getattr__(name):
    if name == "HeuristicValueNetwork":
        from cb_agents.heuristic_value import HeuristicValueNetwork
        return HeuristicValueNetwork
    raise AttributeError(f"module {__name__} no attr {name}")


def __getattr__(name):
    if name == "HeuristicValueNetwork":
        from cb_agents.heuristic_value import HeuristicValueNetwork
        return HeuristicValueNetwork
    raise AttributeError(f"module {__name__} no attr {name}")


def __getattr__(name: str) -> Any:
    return _warn_deprecation(name, module_globals=globals())


def __getattr__(name: str) -> object:
    global GunicornUVLoopWebWorker, GunicornWebWorker

    # Importing gunicorn takes a long time (>100ms), so only import if actually needed.
    if name in ("GunicornUVLoopWebWorker", "GunicornWebWorker"):
        try:
            from .worker import GunicornUVLoopWebWorker as guv, GunicornWebWorker as gw
        except ImportError:
            return None

        GunicornUVLoopWebWorker = guv  # type: ignore[misc]
        GunicornWebWorker = gw  # type: ignore[misc]
        return guv if name == "GunicornUVLoopWebWorker" else gw

    raise AttributeError(f"module {__name__} has no attribute {name}")


def __getattr__(attr: str) -> type[BrokenWorkerInterpreter]:
    """Support deprecated aliases."""
    if attr == "BrokenWorkerIntepreter":
        import warnings

        warnings.warn(
            "The 'BrokenWorkerIntepreter' alias is deprecated, use 'BrokenWorkerInterpreter' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return BrokenWorkerInterpreter

    raise AttributeError(f"module {__name__!r} has no attribute {attr!r}")


def __getattr__(name: str):
    if (val := globals().get(f"_DEPRECATED_{name}")) is None:
        msg = f"module '{__name__}' has no attribute '{name}"
        raise AttributeError(msg)

    # pylint: disable-next=import-outside-toplevel
    import warnings

    msg = (
        f"importing '{name}' from 'astroid' is deprecated and will be removed in v5, "
        "import it from 'astroid.nodes' instead"
    )
    warnings.warn(msg, DeprecationWarning, stacklevel=2)
    return val


def __getattr__(name: str) -> object:
    import warnings

    if name == "BaseCommand":
        warnings.warn(
            "'BaseCommand' is deprecated and will be removed in Click 9.0. Use"
            " 'Command' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return _BaseCommand

    if name == "MultiCommand":
        warnings.warn(
            "'MultiCommand' is deprecated and will be removed in Click 9.0. Use"
            " 'Group' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return _MultiCommand

    raise AttributeError(name)


def __getattr__(name: str) -> object:
    import warnings

    if name in {
        "OptionParser",
        "Argument",
        "Option",
        "split_opt",
        "normalize_opt",
        "ParsingState",
    }:
        warnings.warn(
            f"'parser.{name}' is deprecated and will be removed in Click 9.0."
            " The old parser is available in 'optparse'.",
            DeprecationWarning,
            stacklevel=2,
        )
        return globals()[f"_{name}"]

    if name == "split_arg_string":
        from .shell_completion import split_arg_string

        warnings.warn(
            "Importing 'parser.split_arg_string' is deprecated, it will only be"
            " available in 'shell_completion' in Click 9.0.",
            DeprecationWarning,
            stacklevel=2,
        )
        return split_arg_string

    raise AttributeError(name)


def __getattr__(name: str) -> object:
    import warnings

    if name == "BaseCommand":
        from .core import _BaseCommand

        warnings.warn(
            "'BaseCommand' is deprecated and will be removed in Click 9.0. Use"
            " 'Command' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return _BaseCommand

    if name == "MultiCommand":
        from .core import _MultiCommand

        warnings.warn(
            "'MultiCommand' is deprecated and will be removed in Click 9.0. Use"
            " 'Group' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return _MultiCommand

    if name == "OptionParser":
        from .parser import _OptionParser

        warnings.warn(
            "'OptionParser' is deprecated and will be removed in Click 9.0. The"
            " old parser is available in 'optparse'.",
            DeprecationWarning,
            stacklevel=2,
        )
        return _OptionParser

    if name == "__version__":
        import importlib.metadata
        import warnings

        warnings.warn(
            "The '__version__' attribute is deprecated and will be removed in"
            " Click 9.1. Use feature detection or"
            " 'importlib.metadata.version(\"click\")' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return importlib.metadata.version("click")

    raise AttributeError(name)


def __getattr__(name):
    return getattr(cloudpickle, name)


def __getattr__(name):
    import importlib

    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(
        "module {!r} has not attribute {!r}".format(__name__, name)
    )


def __getattr__(name: str) -> t.Any:
    if name == "__version__":
        import importlib.metadata
        import warnings

        warnings.warn(
            "The '__version__' attribute is deprecated and will be removed in"
            " ItsDangerous 2.3. Use feature detection or"
            " 'importlib.metadata.version(\"itsdangerous\")' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return importlib.metadata.version("itsdangerous")

    raise AttributeError(name)


def __getattr__(name):
    if name == "RefResolutionError":
        warnings.warn(
            _RefResolutionError._DEPRECATION_MESSAGE,
            DeprecationWarning,
            stacklevel=2,
        )
        return _RefResolutionError
    raise AttributeError(f"module {__name__} has no attribute {name}")


def __getattr__(name):
    if name == "ErrorTree":
        warnings.warn(
            "Importing ErrorTree from jsonschema.validators is deprecated. "
            "Instead import it from jsonschema.exceptions.",
            DeprecationWarning,
            stacklevel=2,
        )
        from jsonschema.exceptions import ErrorTree
        return ErrorTree
    elif name == "validators":
        warnings.warn(
            "Accessing jsonschema.validators.validators is deprecated. "
            "Use jsonschema.validators.validator_for with a given schema.",
            DeprecationWarning,
            stacklevel=2,
        )
        return _VALIDATORS
    elif name == "meta_schemas":
        warnings.warn(
            "Accessing jsonschema.validators.meta_schemas is deprecated. "
            "Use jsonschema.validators.validator_for with a given schema.",
            DeprecationWarning,
            stacklevel=2,
        )
        return _META_SCHEMAS
    elif name == "RefResolver":
        warnings.warn(
            _RefResolver._DEPRECATION_MESSAGE,
            DeprecationWarning,
            stacklevel=2,
        )
        return _RefResolver
    raise AttributeError(f"module {__name__} has no attribute {name}")


def __getattr__(name):
    if name == "__version__":
        warnings.warn(
            "Accessing jsonschema.__version__ is deprecated and will be "
            "removed in a future release. Use importlib.metadata directly "
            "to query for jsonschema's version.",
            DeprecationWarning,
            stacklevel=2,
        )

        from importlib import metadata
        return metadata.version("jsonschema")
    elif name == "RefResolver":
        from jsonschema.validators import _RefResolver
        warnings.warn(
            _RefResolver._DEPRECATION_MESSAGE,
            DeprecationWarning,
            stacklevel=2,
        )
        return _RefResolver
    elif name == "ErrorTree":
        warnings.warn(
            "Importing ErrorTree directly from the jsonschema package "
            "is deprecated and will become an ImportError. Import it from "
            "jsonschema.exceptions instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        from jsonschema.exceptions import ErrorTree
        return ErrorTree
    elif name == "FormatError":
        warnings.warn(
            "Importing FormatError directly from the jsonschema package "
            "is deprecated and will become an ImportError. Import it from "
            "jsonschema.exceptions instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        from jsonschema.exceptions import FormatError
        return FormatError
    elif name == "Validator":
        warnings.warn(
            "Importing Validator directly from the jsonschema package "
            "is deprecated and will become an ImportError. Import it from "
            "jsonschema.protocols instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        from jsonschema.protocols import Validator
        return Validator
    elif name == "RefResolutionError":
        from jsonschema.exceptions import _RefResolutionError
        warnings.warn(
            _RefResolutionError._DEPRECATION_MESSAGE,
            DeprecationWarning,
            stacklevel=2,
        )
        return _RefResolutionError

    format_checkers = {
        "draft3_format_checker": Draft3Validator,
        "draft4_format_checker": Draft4Validator,
        "draft6_format_checker": Draft6Validator,
        "draft7_format_checker": Draft7Validator,
        "draft201909_format_checker": Draft201909Validator,
        "draft202012_format_checker": Draft202012Validator,
    }
    ValidatorForFormat = format_checkers.get(name)
    if ValidatorForFormat is not None:
        warnings.warn(
            f"Accessing jsonschema.{name} is deprecated and will be "
            "removed in a future release. Instead, use the FORMAT_CHECKER "
            "attribute on the corresponding Validator.",
            DeprecationWarning,
            stacklevel=2,
        )
        return ValidatorForFormat.FORMAT_CHECKER

    raise AttributeError(f"module {__name__} has no attribute {name}")


def __getattr__(name: str) -> Any:
    """Lazy import handler for main module"""
    if name == "encoding":
        # Use _get_default_encoding which properly sets TIKTOKEN_CACHE_DIR
        # before loading tiktoken, ensuring the local cache is used
        # instead of downloading from the internet
        from litellm._lazy_imports import _get_default_encoding

        _encoding = _get_default_encoding()
        # Cache it in the module's __dict__ for subsequent accesses
        import sys

        sys.modules[__name__].__dict__["encoding"] = _encoding
        global _encoding_cache
        _encoding_cache = _encoding
        return _encoding
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __getattr__(name: str) -> Any:
    """Lazy import handler for utils module with cached registry for improved performance."""
    # Use cached registry from _lazy_imports instead of importing tuples every time
    from litellm._lazy_imports import _get_lazy_import_registry

    registry = _get_lazy_import_registry()

    # Check if name is in registry and call the cached handler function
    if name in registry:
        handler_func = registry[name]
        return handler_func(name)

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __getattr__(name: str) -> Any:
    """Lazy import handler with cached registry for improved performance."""
    global _async_client_cleanup_registered
    # Register async client cleanup on first access (only once)
    if not _async_client_cleanup_registered:
        from litellm.llms.custom_httpx.async_client_cleanup import (
            register_async_client_cleanup,
        )

        register_async_client_cleanup()
        _async_client_cleanup_registered = True

    # Use cached registry from _lazy_imports instead of importing tuples every time
    from ._lazy_imports import _get_lazy_import_registry

    registry = _get_lazy_import_registry()

    # Check if name is in registry and call the cached handler function
    if name in registry:
        handler_func = registry[name]
        return handler_func(name)

    # Lazy load encoding from main.py to avoid heavy tiktoken import
    if name == "encoding":
        from ._lazy_imports import _get_litellm_globals

        _globals = _get_litellm_globals()
        # Check if already cached
        if "encoding" not in _globals:
            from .main import encoding as _encoding

            _globals["encoding"] = _encoding
        return _globals["encoding"]

    # Lazy load bedrock_tool_name_mappings instance
    if name == "bedrock_tool_name_mappings":
        from ._lazy_imports import _get_litellm_globals

        _globals = _get_litellm_globals()
        # Check if already cached
        if "bedrock_tool_name_mappings" not in _globals:
            from .llms.bedrock.chat.invoke_handler import (
                bedrock_tool_name_mappings as _bedrock_tool_name_mappings,
            )

            _globals["bedrock_tool_name_mappings"] = _bedrock_tool_name_mappings
        return _globals["bedrock_tool_name_mappings"]

    # Lazy load AzureOpenAIError exception class
    if name == "AzureOpenAIError":
        from ._lazy_imports import _get_litellm_globals

        _globals = _get_litellm_globals()
        # Check if already cached
        if "AzureOpenAIError" not in _globals:
            from .llms.azure.common_utils import AzureOpenAIError as _AzureOpenAIError

            _globals["AzureOpenAIError"] = _AzureOpenAIError
        return _globals["AzureOpenAIError"]

    # Lazy load openaiOSeriesConfig instance
    if name == "openaiOSeriesConfig":
        from ._lazy_imports import _get_litellm_globals

        _globals = _get_litellm_globals()
        if "openaiOSeriesConfig" not in _globals:
            # Import the config class and instantiate it
            config_class = __getattr__("OpenAIOSeriesConfig")
            _globals["openaiOSeriesConfig"] = config_class()
        return _globals["openaiOSeriesConfig"]

    # Lazy load other config instances
    _config_instances = {
        "openAIGPTConfig": "OpenAIGPTConfig",
        "openAIGPTAudioConfig": "OpenAIGPTAudioConfig",
        "openAIGPT5Config": "OpenAIGPT5Config",
        "nvidiaNimConfig": "NvidiaNimConfig",
        "nvidiaNimEmbeddingConfig": "NvidiaNimEmbeddingConfig",
    }
    if name in _config_instances:
        from ._lazy_imports import _get_litellm_globals

        _globals = _get_litellm_globals()
        if name not in _globals:
            # Import the config class and instantiate it
            config_class = __getattr__(_config_instances[name])
            _globals[name] = config_class()
        return _globals[name]

    # Handle OpenAIO1Config alias
    if name == "OpenAIO1Config":
        return __getattr__("OpenAIOSeriesConfig")

    # Lazy load provider_list
    if name == "provider_list":
        from ._lazy_imports import _get_litellm_globals

        _globals = _get_litellm_globals()
        # Check if already cached
        if "provider_list" not in _globals:
            # LlmProviders is eagerly imported above, so we can import it directly
            from litellm.types.utils import LlmProviders

            _globals["provider_list"] = list(LlmProviders)
        return _globals["provider_list"]

    # Lazy load priority_reservation_settings instance
    if name == "priority_reservation_settings":
        from ._lazy_imports import _get_litellm_globals

        _globals = _get_litellm_globals()
        # Check if already cached
        if "priority_reservation_settings" not in _globals:
            # Import the class and instantiate it
            PriorityReservationSettings = __getattr__("PriorityReservationSettings")
            _globals["priority_reservation_settings"] = PriorityReservationSettings()
        return _globals["priority_reservation_settings"]

    # Lazy load logging_callback_manager instance
    if name == "logging_callback_manager":
        from ._lazy_imports import _get_litellm_globals

        _globals = _get_litellm_globals()
        # Check if already cached
        if "logging_callback_manager" not in _globals:
            # Import the class and instantiate it
            LoggingCallbackManager = __getattr__("LoggingCallbackManager")
            _globals["logging_callback_manager"] = LoggingCallbackManager()
        return _globals["logging_callback_manager"]

    # Lazy load _service_logger module
    if name == "_service_logger":
        from ._lazy_imports import _get_litellm_globals

        _globals = _get_litellm_globals()
        # Check if already cached
        if "_service_logger" not in _globals:
            # Import the module lazily
            import litellm._service_logger

            _globals["_service_logger"] = litellm._service_logger
        return _globals["_service_logger"]

    # Lazy load evals module functions
    if name in [
        "acreate_eval",
        "alist_evals",
        "aget_eval",
        "aupdate_eval",
        "adelete_eval",
        "acancel_eval",
        "create_eval",
        "list_evals",
        "get_eval",
        "update_eval",
        "delete_eval",
        "cancel_eval",
        "acreate_run",
        "alist_runs",
        "aget_run",
        "acancel_run",
        "adelete_run",
        "create_run",
        "list_runs",
        "get_run",
        "cancel_run",
        "delete_run",
    ]:
        from litellm.evals.main import (
            acreate_eval,
            alist_evals,
            aget_eval,
            aupdate_eval,
            adelete_eval,
            acancel_eval,
            create_eval,
            list_evals,
            get_eval,
            update_eval,
            delete_eval,
            cancel_eval,
            acreate_run,
            alist_runs,
            aget_run,
            acancel_run,
            adelete_run,
            create_run,
            list_runs,
            get_run,
            cancel_run,
            delete_run,
        )

        return locals()[name]

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __getattr__(name: str) -> t.Any:
    if name == "__version__":
        import importlib.metadata
        import warnings

        warnings.warn(
            "The '__version__' attribute is deprecated and will be removed in"
            " MarkupSafe 3.1. Use feature detection, or"
            ' `importlib.metadata.version("markupsafe")`, instead.',
            DeprecationWarning,
            stacklevel=2,
        )
        return importlib.metadata.version("markupsafe")

    raise AttributeError(name)


def __getattr__(name):
    if name == "random_tree":
        raise AttributeError(
            "nx.random_tree was removed in version 3.4. Use `nx.random_labeled_tree` instead.\n"
            "See: https://networkx.org/documentation/latest/release/release_3.4.html"
        )
    raise AttributeError(f"module 'networkx' has no attribute '{name}'")


def __getattr__(attr_name: str) -> object:
    if attr_name in _deprecated_dynamic_imports:
        from pydantic.warnings import PydanticDeprecatedSince20

        warn(
            f'Importing {attr_name} from `pydantic` is deprecated. This feature is either no longer supported, or is not public.',
            PydanticDeprecatedSince20,
            stacklevel=2,
        )

    dynamic_attr = _dynamic_imports.get(attr_name)
    if dynamic_attr is None:
        return _getattr_migration(attr_name)

    package, module_name = dynamic_attr

    if module_name == '__module__':
        result = import_module(f'.{attr_name}', package=package)
        globals()[attr_name] = result
        return result
    else:
        module = import_module(module_name, package=package)
        result = getattr(module, attr_name)
        g = globals()
        for k, (_, v_module_name) in _dynamic_imports.items():
            if v_module_name == module_name and k not in _deprecated_dynamic_imports:
                g[k] = getattr(module, k)
        return result


def __getattr__(attr_name: str) -> object:
    new_attr = _deprecated_import_lookup.get(attr_name)
    if new_attr is None:
        raise AttributeError(f"module 'pydantic_core' has no attribute '{attr_name}'")
    else:
        import warnings

        msg = f'`{attr_name}` is deprecated, use `{new_attr.__name__}` instead.'
        warnings.warn(msg, DeprecationWarning, stacklevel=1)
        return new_attr


def __getattr__(name):
    if name in submodules:
        return _importlib.import_module(f'scipy.{name}')
    else:
        try:
            return globals()[name]
        except KeyError:
            raise AttributeError(
                f"Module 'scipy' has no attribute '{name}'"
            )


def __getattr__(name: str) -> Any:  # pragma: no cover
    if name == "sequence":
        SetuptoolsDeprecationWarning.emit(
            "`setuptools.dist.sequence` is an internal implementation detail.",
            "Please define your own `sequence = tuple, list` instead.",
            due_date=(2025, 8, 28),  # Originally added on 2024-08-27
        )
        return _sequence
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __getattr__(name):
    if name == "__version__":
        from importlib.metadata import version

        rv = version("toolz")
        globals()[name] = rv
        return rv
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __getattr__(attr: str) -> type[Error]:
    return getattr(_error_maker, attr)  # type: ignore[no-any-return]


def __getattr__(name: str) -> t.Any:
    import warnings

    if name == "OrderedMultiDict":
        warnings.warn(
            "'OrderedMultiDict' is deprecated and will be removed in Werkzeug"
            " 3.2. Use 'MultiDict' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return _OrderedMultiDict

    if name == "ImmutableOrderedMultiDict":
        warnings.warn(
            "'ImmutableOrderedMultiDict' is deprecated and will be removed in"
            " Werkzeug 3.2. Use 'ImmutableMultiDict' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return _ImmutableOrderedMultiDict

    raise AttributeError(name)


def __getattr__(name: str) -> t.Any:
    import warnings

    if name == "OrderedMultiDict":
        from .structures import _OrderedMultiDict

        warnings.warn(
            "'OrderedMultiDict' is deprecated and will be removed in Werkzeug"
            " 3.2. Use 'MultiDict' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return _OrderedMultiDict

    if name == "ImmutableOrderedMultiDict":
        from .structures import _ImmutableOrderedMultiDict

        warnings.warn(
            "'OrderedMultiDict' is deprecated and will be removed in Werkzeug"
            " 3.2. Use 'ImmutableMultiDict' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return _ImmutableOrderedMultiDict

    raise AttributeError(name)


def __getattr__(name: str) -> "ModuleType":
    if name in __all__:
        import importlib

        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __getattr__(name: str) -> NoReturn:
    raise AttributeError(f"module {__name__} has no attribute {name}")


def __getattr__(name: str) -> "ModuleType":
    if name in __all__:
        import importlib

        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __getattr__(name: str) -> types.ModuleType:
    if name in __all__:
        import importlib

        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __getattr__(name):
    attr = getattr(
        types.SimpleNamespace(
            ScriptWriter=_scripts.ScriptWriter,
            sys_executable=os.environ.get(
                "__PYVENV_LAUNCHER__", os.path.normpath(sys.executable)
            ),
        ),
        name,
    )
    warnings.SetuptoolsDeprecationWarning.emit(
        summary="easy_install module is deprecated",
        details="Avoid accessing attributes of setuptools.command.easy_install.",
        due_date=(2025, 10, 31),
        see_url="https://github.com/pypa/setuptools/issues/4976",
    )
    return attr


def __getattr__(name: str):  # pragma: no cover
    if name == "_install":
        SetuptoolsDeprecationWarning.emit(
            "`setuptools.command._install` was an internal implementation detail "
            "that was left in for numpy<1.9 support.",
            due_date=(2025, 5, 2),  # Originally added on 2024-11-01
        )
        return orig.install
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __getattr__(name: str) -> type[_test]:
    if name == 'test':
        SetuptoolsDeprecationWarning.emit(
            "The test command is disabled and references to it are deprecated.",
            "Please remove any references to `setuptools.command.test` in all "
            "supported versions of the affected package.",
            due_date=(2024, 11, 15),
            stacklevel=2,
        )
        return _test
    raise AttributeError(name)


def __getattr__(name):
    if name not in ['newer', 'newer_group', 'newer_pairwise']:
        raise AttributeError(name)
    warnings.warn(
        "dep_util is Deprecated. Use functions from setuptools instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(_modified, name)


def __getattr__(name):
    if name == '_get_vc_env':
        warnings.warn(
            "_get_vc_env is private; find an alternative (pypa/distutils#340)"
        )
        return msvc._get_vc_env
    raise AttributeError(name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="constants", module="codata",
                                   private_modules=["_codata"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="constants", module="constants",
                                   private_modules=["_constants"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="fftpack", module="basic",
                                   private_modules=["_basic"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="fftpack", module="helper",
                                   private_modules=["_helper"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="fftpack", module="pseudo_diffs",
                                   private_modules=["_pseudo_diffs"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="fftpack", module="realtransforms",
                                   private_modules=["_realtransforms"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="integrate", module="dop",
                                   private_modules=["_dop"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="integrate", module="lsoda",
                                   private_modules=["_odepack"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="integrate", module="odepack",
                                   private_modules=["_odepack_py"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="integrate", module="quadpack",
                                   private_modules=["_quadpack_py"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="integrate", module="vode",
                                   private_modules=["_vode"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="interpolate", module="dfitpack",
                                   private_modules=["_fitpack"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="interpolate", module="fitpack",
                                   private_modules=["_fitpack_py"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="interpolate", module="fitpack2",
                                   private_modules=["_fitpack2"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="interpolate", module="interpnd",
                                   private_modules=["_interpnd"], all=__all__,
                                   attribute=name, dep_version="1.17.0")


def __getattr__(name):
    return _sub_module_deprecation(sub_package="interpolate", module="interpolate",
                                   private_modules=["_interpolate", "fitpack2", "_rgi"],
                                   all=__all__, attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="interpolate", module="ndgriddata",
                                   private_modules=["_ndgriddata"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="interpolate", module="polyint",
                                   private_modules=["_polyint"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="interpolate", module="rbf",
                                   private_modules=["_rbf"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="io", module="harwell_boeing",
                                   private_modules=["_harwell_boeing"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="io", module="idl",
                                   private_modules=["_idl"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="io", module="mmio",
                                   private_modules=["_mmio"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="io", module="netcdf",
                                   private_modules=["_netcdf"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="linalg", module="basic",
                                   private_modules=["_basic"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="linalg", module="decomp",
                                   private_modules=["_decomp"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="linalg", module="decomp_cholesky",
                                   private_modules=["_decomp_cholesky"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="linalg", module="decomp_lu",
                                   private_modules=["_decomp_lu"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="linalg", module="decomp_qr",
                                   private_modules=["_decomp_qr"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="linalg", module="decomp_schur",
                                   private_modules=["_decomp_schur"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="linalg", module="decomp_svd",
                                   private_modules=["_decomp_svd"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="linalg", module="matfuncs",
                                   private_modules=["_matfuncs"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="linalg", module="misc",
                                   private_modules=["_misc"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="linalg", module="special_matrices",
                                   private_modules=["_special_matrices"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package='ndimage', module='filters',
                                   private_modules=['_filters'], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package='ndimage', module='fourier',
                                   private_modules=['_fourier'], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package='ndimage', module='interpolation',
                                   private_modules=['_interpolation'], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package='ndimage', module='measurements',
                                   private_modules=['_measurements'], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package='ndimage', module='morphology',
                                   private_modules=['_morphology'], all=__all__,
                                   attribute=name)


def __getattr__(name):
    msg = ("`scipy.odr` is deprecated as of version 1.17.0 and will be removed in "
           "SciPy 1.19.0. Please use `https://pypi.org/project/odrpack/` instead.")
    if name not in __all__:
        raise AttributeError(
            f"`scipy.odr.models` has no attribute {name}. In addition, {msg}")

    import warnings
    from . import _models
    warnings.warn(msg, category=DeprecationWarning, stacklevel=2)

    return getattr(_models, name)


def __getattr__(name):
    msg = ("`scipy.odr` is deprecated as of version 1.17.0 and will be removed in "
           "SciPy 1.19.0. Please use `https://pypi.org/project/odrpack/` instead.")
    if name not in __all__:
        raise AttributeError(
            f"`scipy.odr.odrpack` has no attribute {name}. In addition, {msg}")

    import warnings
    from . import _odrpack
    warnings.warn(msg, category=DeprecationWarning, stacklevel=2)

    return getattr(_odrpack, name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="optimize", module="cobyla",
                                   private_modules=["_cobyla_py"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="optimize", module="lbfgsb",
                                   private_modules=["_lbfgsb_py"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="optimize", module="linesearch",
                                   private_modules=["_linesearch"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="optimize", module="minpack",
                                   private_modules=["_minpack_py"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="optimize", module="minpack2",
                                   private_modules=["_minpack2"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="optimize", module="moduleTNC",
                                   private_modules=["_moduleTNC"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="optimize", module="nonlin",
                                   private_modules=["_nonlin"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="optimize", module="optimize",
                                   private_modules=["_optimize"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="optimize", module="slsqp",
                                   private_modules=["_slsqp_py"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="optimize", module="tnc",
                                   private_modules=["_tnc"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="optimize", module="zeros",
                                   private_modules=["_zeros_py"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="signal", module="bsplines",
                                   private_modules=["_spline_filters"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="signal", module="filter_design",
                                   private_modules=["_filter_design"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="signal", module="fir_filter_design",
                                   private_modules=["_fir_filter_design"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="signal", module="ltisys",
                                   private_modules=["_ltisys"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="signal", module="lti_conversion",
                                   private_modules=["_lti_conversion"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="signal", module="signaltools",
                                   private_modules=["_signaltools"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="signal", module="spectral",
                                   private_modules=["_spectral_py"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="signal", module="spline",
                                   private_modules=["_spline"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="signal", module="waveforms",
                                   private_modules=["_waveforms"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="signal", module="wavelets",
                                   private_modules=["_wavelets"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="sparse", module="base",
                                   private_modules=["_base"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="sparse", module="bsr",
                                   private_modules=["_bsr"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="sparse", module="compressed",
                                   private_modules=["_compressed"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="sparse", module="construct",
                                   private_modules=["_construct"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="sparse", module="coo",
                                   private_modules=["_coo"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="sparse", module="csc",
                                   private_modules=["_csc"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="sparse", module="csr",
                                   private_modules=["_csr"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="sparse", module="data",
                                   private_modules=["_data"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="sparse", module="dia",
                                   private_modules=["_dia"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="sparse", module="dok",
                                   private_modules=["_dok"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="sparse", module="extract",
                                   private_modules=["_extract"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="sparse", module="lil",
                                   private_modules=["_lil"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="sparse", module="sparsetools",
                                   private_modules=["_sparsetools"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="sparse", module="spfuncs",
                                   private_modules=["_spfuncs"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="sparse", module="sputils",
                                   private_modules=["_sputils"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    if name in _submodules:
        return _importlib.import_module(f'scipy.sparse.{name}')
    else:
        try:
            return globals()[name]
        except KeyError:
            raise AttributeError(
                f"Module 'scipy.sparse' has no attribute '{name}'"
            )


def __getattr__(name):
    return _sub_module_deprecation(sub_package="spatial", module="ckdtree",
                                   private_modules=["_ckdtree"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="spatial", module="kdtree",
                                   private_modules=["_kdtree"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="spatial", module="qhull",
                                   private_modules=["_qhull"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="special", module="add_newdocs",
                                   private_modules=["_add_newdocs"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="special", module="basic",
                                   private_modules=["_basic", "_ufuncs"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="special", module="orthogonal",
                                   private_modules=["_orthogonal"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="special", module="sf_error",
                                   private_modules=["_sf_error"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="special", module="specfun",
                                   private_modules=["_basic", "_specfun"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="special", module="spfun_stats",
                                   private_modules=["_spfun_stats"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="stats", module="biasedurn",
                                   private_modules=["_biasedurn"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="stats", module="kde",
                                   private_modules=["_kde"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="stats", module="morestats",
                                   private_modules=["_morestats"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="stats", module="mstats_basic",
                                   private_modules=["_mstats_basic"], all=__all__,
                                   attribute=name, correct_module="mstats")


def __getattr__(name):
    return _sub_module_deprecation(sub_package="stats", module="mstats_extras",
                                   private_modules=["_mstats_extras"], all=__all__,
                                   attribute=name, correct_module="mstats")


def __getattr__(name):
    return _sub_module_deprecation(sub_package="stats", module="mvn",
                                   private_modules=["_mvn"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(
        sub_package="stats", module="stats",
        private_modules=["_stats_py", "_mgc", "_correlation"],
        all=__all__,
        attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="spatial.transform", module="rotation",
                                   private_modules=["_rotation"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="sparse.linalg", module="dsolve",
                                   private_modules=["_dsolve"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="sparse.linalg", module="eigen",
                                   private_modules=["_eigen"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="sparse.linalg", module="interface",
                                   private_modules=["_interface"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="sparse.linalg", module="isolve",
                                   private_modules=["_isolve"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="sparse.linalg", module="matfuncs",
                                   private_modules=["_matfuncs"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="signal.windows", module="windows",
                                   private_modules=["_windows"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="io.arff", module="arffread",
                                   private_modules=["_arffread"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="io.matlab", module="byteordercodes",
                                   private_modules=["_byteordercodes"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="io.matlab", module="mio",
                                   private_modules=["_mio"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="io.matlab", module="mio4",
                                   private_modules=["_mio4"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="io.matlab", module="mio5",
                                   private_modules=["_mio5"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="io.matlab", module="mio5_params",
                                   private_modules=["_mio5_params"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="io.matlab", module="mio5_utils",
                                   private_modules=["_mio5_utils"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="io.matlab", module="miobase",
                                   private_modules=["_miobase"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="io.matlab", module="mio_utils",
                                   private_modules=["_mio_utils"], all=__all__,
                                   attribute=name)


def __getattr__(name):
    return _sub_module_deprecation(sub_package="io.matlab", module="streams",
                                   private_modules=["_streams"], all=__all__,
                                   attribute=name)


def __getattr__(attr: str):
    if newAttr := {"tagMap": "TAG_MAP", "typeMap": "TYPE_MAP"}.get(attr):
        warnings.warn(f"{attr} is deprecated. Please use {newAttr} instead.", DeprecationWarning, stacklevel=2)
        return globals()[newAttr]
    raise AttributeError(attr)


def __getattr__(attr: str):
    if newAttr := {"tagMap": "TAG_MAP", "typeMap": "TYPE_MAP"}.get(attr):
        warnings.warn(f"{attr} is deprecated. Please use {newAttr} instead.", DeprecationWarning, stacklevel=2)
        return globals()[newAttr]
    raise AttributeError(attr)


def __getattr__(attr: str):
    if newAttr := {"tagMap": "TAG_MAP", "typeMap": "TYPE_MAP"}.get(attr):
        warnings.warn(f"{attr} is deprecated. Please use {newAttr} instead.", DeprecationWarning, stacklevel=2)
        return globals()[newAttr]
    raise AttributeError(attr)


def __getattr__(attr: str):
    if newAttr := {"tagMap": "TAG_MAP", "typeMap": "TYPE_MAP"}.get(attr):
        warnings.warn(f"{attr} is deprecated. Please use {newAttr} instead.", DeprecationWarning, stacklevel=2)
        return globals()[newAttr]
    raise AttributeError(attr)


def __getattr__(attr: str):
    if newAttr := {"tagMap": "TAG_MAP", "typeMap": "TYPE_MAP"}.get(attr):
        warnings.warn(f"{attr} is deprecated. Please use {newAttr} instead.", DeprecationWarning, stacklevel=2)
        return globals()[newAttr]
    raise AttributeError(attr)


def __getattr__(attr: str):
    if newAttr := {"tagMap": "TAG_MAP", "typeMap": "TYPE_MAP"}.get(attr):
        warnings.warn(f"{attr} is deprecated. Please use {newAttr} instead.", DeprecationWarning, stacklevel=2)
        return globals()[newAttr]
    raise AttributeError(attr)


def __getattr__(attr: str):
    if newAttr := {"tagMap": "TAG_MAP", "typeMap": "TYPE_MAP"}.get(attr):
        warnings.warn(f"{attr} is deprecated. Please use {newAttr} instead.", DeprecationWarning, stacklevel=2)
        return globals()[newAttr]
    raise AttributeError(attr)


def __getattr__(attr: str):
    if newAttr := {"tagMap": "TAG_MAP", "typeMap": "TYPE_MAP"}.get(attr):
        warnings.warn(f"{attr} is deprecated. Please use {newAttr} instead.", DeprecationWarning, stacklevel=2)
        return globals()[newAttr]
    raise AttributeError(attr)


def __getattr__(env_name):
    return deprecated_handler(env_name, __path__, __name__)


def __getattr__(env_name):
    return deprecated_handler(env_name, __path__, __name__)


def __getattr__(env_name):
    return deprecated_handler(env_name, __path__, __name__)


def __getattr__(env_name):
    return deprecated_handler(env_name, __path__, __name__)


def __getattr__(env_name):
    return deprecated_handler(env_name, __path__, __name__)


def __getattr__(key: str):
    # These imports need to be lazy to avoid circular import errors
    if key == "hash_array":
        from pandas.core.util.hashing import hash_array

        return hash_array
    if key == "hash_pandas_object":
        from pandas.core.util.hashing import hash_pandas_object

        return hash_pandas_object
    if key == "Appender":
        from pandas.util._decorators import Appender

        return Appender
    if key == "Substitution":
        from pandas.util._decorators import Substitution

        return Substitution

    if key == "cache_readonly":
        from pandas.util._decorators import cache_readonly

        return cache_readonly

    raise AttributeError(f"module 'pandas.util' has no attribute '{key}'")


def __getattr__(name: str):
    # GH#55139
    import warnings

    from pandas.errors import Pandas4Warning

    if name == "create_block_manager_from_blocks":
        # GH#33892, GH#58715
        warnings.warn(
            f"{name} is deprecated and will be removed in a future version. "
            "Use public APIs instead.",
            Pandas4Warning,
            # https://github.com/pandas-dev/pandas/pull/55139#pullrequestreview-1720690758
            # on hard-coding stacklevel
            stacklevel=2,
        )
        from pandas.core.internals.managers import create_block_manager_from_blocks

        return create_block_manager_from_blocks

    if name in [
        "Block",
        "ExtensionBlock",
        "DatetimeTZBlock",
    ]:
        warnings.warn(
            f"{name} is deprecated and will be removed in a future version. "
            "Use public APIs instead.",
            Pandas4Warning,
            # https://github.com/pandas-dev/pandas/pull/55139#pullrequestreview-1720690758
            # on hard-coding stacklevel
            stacklevel=2,
        )
        if name == "DatetimeTZBlock":
            from pandas.core.internals.api import _DatetimeTZBlock as DatetimeTZBlock

            return DatetimeTZBlock
        if name == "ExtensionBlock":
            from pandas.core.internals.blocks import ExtensionBlock

            return ExtensionBlock
        else:
            from pandas.core.internals.blocks import Block

            return Block

    raise AttributeError(f"module 'pandas.core.internals' has no attribute '{name}'")


def __getattr__(name: str):
    if name in __DEPRECATED:
        # Deprecated in NumPy 2.5, 2026-01-07
        import warnings

        warnings.warn(
            (
                "The chararray class is deprecated and will be removed in a future "
                "release. Use an ndarray with a string or bytes dtype instead."
            ),
            DeprecationWarning,
            stacklevel=2,
        )

    import numpy._core.defchararray as char

    if (export := getattr(char, name, None)) is not None:
        return export

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __getattr__(attr_name):
    from numpy._core import arrayprint

    from ._utils import _raise_warning
    ret = getattr(arrayprint, attr_name, None)
    if ret is None:
        raise AttributeError(
            f"module 'numpy.core.arrayprint' has no attribute {attr_name}")
    _raise_warning(attr_name, "arrayprint")
    return ret


def __getattr__(attr_name):
    from numpy._core import defchararray

    from ._utils import _raise_warning
    ret = getattr(defchararray, attr_name, None)
    if ret is None:
        raise AttributeError(
            f"module 'numpy.core.defchararray' has no attribute {attr_name}")
    _raise_warning(attr_name, "defchararray")
    return ret


def __getattr__(attr_name):
    from numpy._core import einsumfunc

    from ._utils import _raise_warning
    ret = getattr(einsumfunc, attr_name, None)
    if ret is None:
        raise AttributeError(
            f"module 'numpy.core.einsumfunc' has no attribute {attr_name}")
    _raise_warning(attr_name, "einsumfunc")
    return ret


def __getattr__(attr_name):
    from numpy._core import fromnumeric

    from ._utils import _raise_warning
    ret = getattr(fromnumeric, attr_name, None)
    if ret is None:
        raise AttributeError(
            f"module 'numpy.core.fromnumeric' has no attribute {attr_name}")
    _raise_warning(attr_name, "fromnumeric")
    return ret


def __getattr__(attr_name):
    from numpy._core import function_base

    from ._utils import _raise_warning
    ret = getattr(function_base, attr_name, None)
    if ret is None:
        raise AttributeError(
            f"module 'numpy.core.function_base' has no attribute {attr_name}")
    _raise_warning(attr_name, "function_base")
    return ret


def __getattr__(attr_name):
    from numpy._core import getlimits

    from ._utils import _raise_warning
    ret = getattr(getlimits, attr_name, None)
    if ret is None:
        raise AttributeError(
            f"module 'numpy.core.getlimits' has no attribute {attr_name}")
    _raise_warning(attr_name, "getlimits")
    return ret


def __getattr__(attr_name):
    from numpy._core import multiarray

    from ._utils import _raise_warning
    ret = getattr(multiarray, attr_name, None)
    if ret is None:
        raise AttributeError(
            f"module 'numpy.core.multiarray' has no attribute {attr_name}")
    _raise_warning(attr_name, "multiarray")
    return ret


def __getattr__(attr_name):
    from numpy._core import numeric

    from ._utils import _raise_warning

    sentinel = object()
    ret = getattr(numeric, attr_name, sentinel)
    if ret is sentinel:
        raise AttributeError(
            f"module 'numpy.core.numeric' has no attribute {attr_name}")
    _raise_warning(attr_name, "numeric")
    return ret


def __getattr__(attr_name):
    from numpy._core import numerictypes

    from ._utils import _raise_warning
    ret = getattr(numerictypes, attr_name, None)
    if ret is None:
        raise AttributeError(
            f"module 'numpy.core.numerictypes' has no attribute {attr_name}")
    _raise_warning(attr_name, "numerictypes")
    return ret


def __getattr__(attr_name):
    from numpy._core import overrides

    from ._utils import _raise_warning
    ret = getattr(overrides, attr_name, None)
    if ret is None:
        raise AttributeError(
            f"module 'numpy.core.overrides' has no attribute {attr_name}")
    _raise_warning(attr_name, "overrides")
    return ret


def __getattr__(attr_name):
    from numpy._core import records

    from ._utils import _raise_warning
    ret = getattr(records, attr_name, None)
    if ret is None:
        raise AttributeError(
            f"module 'numpy.core.records' has no attribute {attr_name}")
    _raise_warning(attr_name, "records")
    return ret


def __getattr__(attr_name):
    from numpy._core import shape_base

    from ._utils import _raise_warning
    ret = getattr(shape_base, attr_name, None)
    if ret is None:
        raise AttributeError(
            f"module 'numpy.core.shape_base' has no attribute {attr_name}")
    _raise_warning(attr_name, "shape_base")
    return ret


def __getattr__(attr_name):
    from numpy._core import umath

    from ._utils import _raise_warning
    ret = getattr(umath, attr_name, None)
    if ret is None:
        raise AttributeError(
            f"module 'numpy.core.umath' has no attribute {attr_name}")
    _raise_warning(attr_name, "umath")
    return ret


def __getattr__(attr_name):
    from numpy._core import _dtype

    from ._utils import _raise_warning
    ret = getattr(_dtype, attr_name, None)
    if ret is None:
        raise AttributeError(
            f"module 'numpy.core._dtype' has no attribute {attr_name}")
    _raise_warning(attr_name, "_dtype")
    return ret


def __getattr__(attr_name):
    from numpy._core import _dtype_ctypes

    from ._utils import _raise_warning
    ret = getattr(_dtype_ctypes, attr_name, None)
    if ret is None:
        raise AttributeError(
            f"module 'numpy.core._dtype_ctypes' has no attribute {attr_name}")
    _raise_warning(attr_name, "_dtype_ctypes")
    return ret


def __getattr__(attr_name):
    from numpy._core import _internal

    from ._utils import _raise_warning
    ret = getattr(_internal, attr_name, None)
    if ret is None:
        raise AttributeError(
            f"module 'numpy.core._internal' has no attribute {attr_name}")
    _raise_warning(attr_name, "_internal")
    return ret


def __getattr__(attr_name):
    from numpy._core import _multiarray_umath

    from ._utils import _raise_warning

    if attr_name in {"_ARRAY_API", "_UFUNC_API"}:
        import sys
        import textwrap
        import traceback

        from numpy.version import short_version

        msg = textwrap.dedent(f"""
            A module that was compiled using NumPy 1.x cannot be run in
            NumPy {short_version} as it may crash. To support both 1.x and 2.x
            versions of NumPy, modules must be compiled with NumPy 2.0.
            Some module may need to rebuild instead e.g. with 'pybind11>=2.12'.

            If you are a user of the module, the easiest solution will be to
            downgrade to 'numpy<2' or try to upgrade the affected module.
            We expect that some modules will need time to support NumPy 2.

            """)
        tb_msg = "Traceback (most recent call last):"
        for line in traceback.format_stack()[:-1]:
            if "frozen importlib" in line:
                continue
            tb_msg += line

        # Also print the message (with traceback).  This is because old versions
        # of NumPy unfortunately set up the import to replace (and hide) the
        # error.  The traceback shouldn't be needed, but e.g. pytest plugins
        # seem to swallow it and we should be failing anyway...
        sys.stderr.write(msg + tb_msg)
        raise ImportError(msg)

    ret = getattr(_multiarray_umath, attr_name, None)
    if ret is None:
        raise AttributeError(
            "module 'numpy.core._multiarray_umath' has no attribute "
            f"{attr_name}")
    _raise_warning(attr_name, "_multiarray_umath")
    return ret


def __getattr__(attr_name):
    attr = getattr(_core, attr_name)
    _raise_warning(attr_name)
    return attr


def __getattr__(attr):

    # Avoid importing things that aren't needed for building
    # which might import the main numpy module
    if attr == "test":
        from numpy._pytesttester import PytestTester
        test = PytestTester(__name__)
        return test

    else:
        raise AttributeError(f"module {__name__!r} has no attribute {attr!r}")


def __getattr__(attr):
    # Warn for deprecated/removed aliases
    import warnings

    if attr == "emath":
        raise AttributeError(
            "numpy.lib.emath was an alias for emath module that was removed "
            "in NumPy 2.0. Replace usages of numpy.lib.emath with "
            "numpy.emath.",
            name=None
        )
    elif attr in (
        "histograms", "type_check", "nanfunctions", "function_base",
        "arraypad", "arraysetops", "ufunclike", "utils", "twodim_base",
        "shape_base", "polynomial", "index_tricks",
    ):
        raise AttributeError(
            f"numpy.lib.{attr} is now private. If you are using a public "
            "function, it should be available in the main numpy namespace, "
            "otherwise check the NumPy 2.0 migration guide.",
            name=None
        )
    elif attr == "arrayterator":
        raise AttributeError(
            "numpy.lib.arrayterator submodule is now private. To access "
            "Arrayterator class use numpy.lib.Arrayterator.",
            name=None
        )
    else:
        raise AttributeError(f"module {__name__!r} has no attribute {attr!r}")


def __getattr__(name: str) -> object:
    if name == "NBitBase":
        import warnings

        # Deprecated in NumPy 2.3, 2025-05-01
        warnings.warn(
            "`NBitBase` is deprecated and will be removed from numpy.typing in the "
            "future. Use `@typing.overload` or a `TypeVar` with a scalar-type as upper "
            "bound, instead. (deprecated in NumPy 2.3)",
            DeprecationWarning,
            stacklevel=2,
        )
        return NBitBase

    if name in __DIR_SET:
        return globals()[name]

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __getattr__(name):
    if name == 'qApp':
        return _backend_qt.qApp
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __getattr__(name: str) -> Any:
    """Lazy import handler for images.main module"""
    if name == "ImageEditRequestUtils":
        # Lazy load ImageEditRequestUtils to avoid heavy import from images.utils at module load time
        from .utils import ImageEditRequestUtils as _ImageEditRequestUtils

        # Cache it in the module's __dict__ for subsequent accesses
        module = importlib.import_module(__name__)
        module.__dict__["ImageEditRequestUtils"] = _ImageEditRequestUtils
        return _ImageEditRequestUtils
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __getattr__(wrapper_name: str):
    """Load a wrapper by name.

    This optimizes the loading of gymnasium wrappers by only loading the wrapper if it is used.
    Errors will be raised if the wrapper does not exist or if the version is not the latest.

    Args:
        wrapper_name: The name of a wrapper to load.

    Returns:
        The specified wrapper.

    Raises:
        AttributeError: If the wrapper does not exist.
        DeprecatedWrapper: If the version is not the latest.
    """
    # Check if the requested wrapper is in the _wrapper_to_class dictionary
    if wrapper_name in _wrapper_to_class:
        import_stmt = f"gymnasium.wrappers.{_wrapper_to_class[wrapper_name]}"
        module = importlib.import_module(import_stmt)
        return getattr(module, wrapper_name)

    elif wrapper_name in _renamed_wrapper:
        raise AttributeError(
            f"{wrapper_name!r} has been renamed with `wrappers.{_renamed_wrapper[wrapper_name]}`"
        )

    raise AttributeError(f"module {__name__!r} has no attribute {wrapper_name!r}")


def __getattr__(wrapper_name: str):
    """Load a wrapper by name.

    This optimizes the loading of gymnasium wrappers by only loading the wrapper if it is used.
    Errors will be raised if the wrapper does not exist or if the version is not the latest.

    Args:
        wrapper_name: The name of a wrapper to load.

    Returns:
        The specified wrapper.

    Raises:
        AttributeError: If the wrapper does not exist.
        DeprecatedWrapper: If the version is not the latest.
    """
    # Check if the requested wrapper is in the _wrapper_to_class dictionary
    if wrapper_name in _wrapper_to_class:
        import_stmt = f"gymnasium.wrappers.vector.{_wrapper_to_class[wrapper_name]}"
        module = importlib.import_module(import_stmt)
        return getattr(module, wrapper_name)

    raise AttributeError(f"module {__name__!r} has no attribute {wrapper_name!r}")

