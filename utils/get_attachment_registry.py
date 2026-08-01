
def get_attachment_registry() -> AttachmentRegistry:
    """
    Get the global AttachmentRegistry singleton.

    Returns:
        The global AttachmentRegistry instance
    """
    global _attachment_registry
    if _attachment_registry is None:
        _attachment_registry = AttachmentRegistry()
    return _attachment_registry

