import os
from typing import Dict, List

def get_available_content_categories() -> List[Dict[str, str]]:
    """
    Return available content categories for UI display.

    Includes categories defined in .yaml/.yml files and in .json files
    (e.g. harm_toxic_abuse.json).

    Returns:
        List of dictionaries containing category name, display_name, and description
    """
    import yaml

    categories_dir = os.path.join(os.path.dirname(__file__), "categories")
    available_categories = []

    if not os.path.exists(categories_dir):
        return []

    # Scan the categories directory for YAML files
    for filename in os.listdir(categories_dir):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            category_file_path = os.path.join(categories_dir, filename)
            try:
                with open(category_file_path, "r") as f:
                    category_data = yaml.safe_load(f)

                if category_data and "category_name" in category_data:
                    # Use explicit display_name if provided, otherwise auto-generate from category_name
                    display_name = category_data.get("display_name") or (
                        category_data["category_name"].replace("_", " ").title()
                    )

                    available_categories.append(
                        {
                            "name": category_data["category_name"],
                            "display_name": display_name,
                            "description": category_data.get("description", ""),
                            "default_action": category_data.get(
                                "default_action", "BLOCK"
                            ),
                        }
                    )
            except Exception as e:
                # Skip files that can't be loaded but log the error for debugging
                from litellm._logging import verbose_proxy_logger

                verbose_proxy_logger.warning(
                    f"Failed to load category file {filename}: {str(e)}"
                )
                continue
        elif filename.endswith(".json"):
            # JSON category files (e.g. harm_toxic_abuse.json) - no YAML header, use filename
            category_name = os.path.splitext(filename)[0]
            try:
                if category_name == "harm_toxic_abuse":
                    display_name = "Harmful Toxic Abuse"
                    description = (
                        "Detects harmful, toxic, or abusive language and content"
                    )
                else:
                    display_name = category_name.replace("_", " ").title()
                    description = f"Content category: {display_name}"
                available_categories.append(
                    {
                        "name": category_name,
                        "display_name": display_name,
                        "description": description,
                        "default_action": "BLOCK",
                    }
                )
            except Exception:
                continue

    # Sort by name for consistent ordering
    available_categories.sort(key=lambda x: x["name"])

    return available_categories

