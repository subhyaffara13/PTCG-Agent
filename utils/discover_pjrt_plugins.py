
def discover_pjrt_plugins() -> None:
  """Discovers plugins in the namespace package `jax_plugins` and import them.

  There are two methods used to discover plugin modules. They are intended
  to be used together by implementers in order to cover all packaging and
  development cases:

  1. Define a globally unique module under the `jax_plugins` namespace
     package (i.e. just create a `jax_plugins` directory and define your
     module below it).
  2. If building a package via pyproject.toml or setup.py, advertise your
     plugin module name by including an entry-point under the `jax_plugins`
     group which points to your full module name.

  During Jax startup, Jax will load each module discovered in such a way and
  call its `initialize()` function. It is expected that this function should
  register its concrete plugin name/implementations via call(s) to
  `jax._src.xla_bridge.register_plugin(name, priority=, library_paty=,
  options=)`. Since `initialize()` functions are called for all installed
  plugins, they should avoid doing expensive, non-registration related work.

  TODO: We should provide a variant of `register_plugin` which allows the
  library_path and options to be resolved via a callback. This would enable
  light-weight plugin registration in cases where options need to be derived
  from heavy-weight system initialization.
  """
  plugin_modules = set()
  # Scan installed modules under |jax_plugins|. Note that not all packaging
  # scenarios are amenable to such scanning, so we also use the entry-point
  # method to seed the list.
  if jax_plugins:
    for _, name, _ in pkgutil.iter_modules(
        jax_plugins.__path__, jax_plugins.__name__ + '.'
    ):
      logger.debug("Discovered path based JAX plugin: %s", name)
      plugin_modules.add(name)
  else:
    logger.debug("No jax_plugins namespace packages available")

  # Augment with advertised entrypoints.
  from importlib.metadata import entry_points

  for entry_point in entry_points(group="jax_plugins"):
    logger.debug("Discovered entry-point based JAX plugin: %s",
                 entry_point.value)
    plugin_modules.add(entry_point.value)

  # Now load and initialize them all.
  for plugin_module_name in plugin_modules:
    logger.debug("Loading plugin module %s", plugin_module_name)
    plugin_module = None
    try:
      plugin_module = importlib.import_module(plugin_module_name)
    except ModuleNotFoundError:
      logger.warning("Jax plugin configuration error: Plugin module %s "
                     "does not exist", plugin_module_name)
    except ImportError:
      logger.exception("Jax plugin configuration error: Plugin module %s "
                       "could not be loaded")

    if plugin_module:
      try:
        plugin_module.initialize()
      except:
        logger.exception("Jax plugin configuration error: Exception when "
                         "calling %s.initialize()", plugin_module_name)

