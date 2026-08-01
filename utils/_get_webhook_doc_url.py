
def _get_webhook_doc_url(webhook_name: str, webhook_path: str) -> str:
    """Returns the anchor to a given webhook in the docs (experimental)"""
    return "/docs#/default/" + webhook_name + webhook_path.replace("/", "_") + "_post"

