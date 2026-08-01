
def get_guardrail_class_from_hooks():
    """
    Get guardrail classes by discovering them from the guardrail_hooks directory structure.
    """
    """
    Get guardrail initializers by discovering them from the guardrail_hooks directory structure.

    Scans the guardrail_hooks directory for subdirectories containing __init__.py files
    with either guardrail_initializer_registry or initialize_guardrail functions.

    Returns:
        Dict[str, Callable]: A dictionary mapping guardrail types to their initializer functions
    """
    discovered_classes = {}

    try:
        # Get the path to the guardrail_hooks directory
        current_dir = os.path.dirname(__file__)
        hooks_dir = os.path.join(current_dir, "guardrail_hooks")

        if not os.path.exists(hooks_dir):
            verbose_proxy_logger.debug("guardrail_hooks directory not found")
            return discovered_classes

        # Scan each subdirectory in guardrail_hooks
        for item in os.listdir(hooks_dir):
            item_path = os.path.join(hooks_dir, item)

            # Skip files and __pycache__ directories
            if not os.path.isdir(item_path) or item.startswith("__"):
                continue

            # Check if the directory has an __init__.py file
            init_file = os.path.join(item_path, "__init__.py")

            if not os.path.exists(init_file):
                continue

            module_path = f"litellm.proxy.guardrails.guardrail_hooks.{item}"

            try:
                # Import the module
                verbose_proxy_logger.debug(f"Discovering guardrails in: {module_path}")

                module = importlib.import_module(module_path)

                # Check for guardrail_initializer_registry dictionary
                if hasattr(module, "guardrail_class_registry"):
                    registry = getattr(module, "guardrail_class_registry")
                    if isinstance(registry, dict):
                        discovered_classes.update(registry)

            except ImportError as e:
                verbose_proxy_logger.debug(f"Could not import {module_path}: {e}")
                continue
            except Exception as e:
                verbose_proxy_logger.exception(f"Error processing {module_path}: {e}")
                continue

    except Exception as e:
        verbose_proxy_logger.error(f"Error discovering guardrail initializers: {e}")

    return discovered_classes

