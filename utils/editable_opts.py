
def editable_opts(request):
    if request.param == "strict":
        return ["--config-settings", "editable-mode=strict"]
    return []

