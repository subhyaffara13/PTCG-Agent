from typing import Any, Dict, List

def _get_available_models(ctx: click.Context) -> List[Dict[str, Any]]:
    """Get list of available models from the proxy server"""
    try:
        client = Client(base_url=ctx.obj["base_url"], api_key=ctx.obj["api_key"])
        models_list = client.models.list()
        # Ensure we return a list of dictionaries
        if isinstance(models_list, list):
            # Filter to ensure all items are dictionaries
            return [model for model in models_list if isinstance(model, dict)]
        return []
    except Exception as e:
        click.echo(f"Warning: Could not fetch models list: {e}", err=True)
        return []

