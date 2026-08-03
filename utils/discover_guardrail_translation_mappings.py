import os
from typing import Dict

def discover_guardrail_translation_mappings() -> (
    Dict[CallTypes, Type["BaseTranslation"]]
):
    """
    Discover guardrail translation mappings by scanning the llms directory structure.

    Scans for modules with guardrail_translation_mappings dictionaries and aggregates them.

    Returns:
        Dict[CallTypes, Type[BaseTranslation]]: A dictionary mapping call types to their translation handler classes
    """
    discovered_mappings: Dict[CallTypes, Type["BaseTranslation"]] = {}

    try:
        # Get the path to the llms directory
        current_dir = os.path.dirname(__file__)
        llms_dir = current_dir

        if not os.path.exists(llms_dir):
            verbose_logger.debug("llms directory not found")
            return discovered_mappings

        # Recursively scan for guardrail_translation directories
        for root, dirs, files in os.walk(llms_dir):
            # Skip __pycache__ and base_llm directories
            dirs[:] = [d for d in dirs if not d.startswith("__") and d != "base_llm"]

            # Check if this is a guardrail_translation directory with __init__.py
            if (
                os.path.basename(root) == "guardrail_translation"
                and "__init__.py" in files
            ):
                # Build the module path relative to litellm
                rel_path = os.path.relpath(root, os.path.dirname(llms_dir))
                module_path = "litellm." + rel_path.replace(os.sep, ".")

                try:
                    # Import the module
                    verbose_logger.debug(
                        f"Discovering guardrail translations in: {module_path}"
                    )

                    module = importlib.import_module(module_path)

                    # Check for guardrail_translation_mappings dictionary
                    if hasattr(module, "guardrail_translation_mappings"):
                        mappings = getattr(module, "guardrail_translation_mappings")
                        if isinstance(mappings, dict):
                            discovered_mappings.update(mappings)
                            verbose_logger.debug(
                                f"Found guardrail_translation_mappings in {module_path}: {list(mappings.keys())}"
                            )

                except ImportError as e:
                    verbose_logger.error(f"Could not import {module_path}: {e}")
                    continue
                except Exception as e:
                    verbose_logger.error(f"Error processing {module_path}: {e}")
                    continue

        try:
            from litellm.proxy._experimental.mcp_server.guardrail_translation import (
                guardrail_translation_mappings as mcp_guardrail_translation_mappings,
            )

            discovered_mappings.update(mcp_guardrail_translation_mappings)
            verbose_logger.debug(
                "Loaded MCP guardrail translation mappings: %s",
                list(mcp_guardrail_translation_mappings.keys()),
            )
        except ImportError:
            verbose_logger.debug(
                "MCP guardrail translation mappings not available; skipping"
            )

        verbose_logger.debug(
            f"Discovered {len(discovered_mappings)} guardrail translation mappings: {list(discovered_mappings.keys())}"
        )

    except Exception as e:
        verbose_logger.error(f"Error discovering guardrail translation mappings: {e}")

    return discovered_mappings

