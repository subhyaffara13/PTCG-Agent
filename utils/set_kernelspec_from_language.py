
def set_kernelspec_from_language(notebook):
    """Set the kernel specification based on the 'main_language' metadata"""
    language = notebook.metadata.get("jupytext", {}).get("main_language")
    if "kernelspec" not in notebook.metadata and language:
        try:
            kernelspec = kernelspec_from_language(language)
        except ValueError:
            return
        notebook.metadata["kernelspec"] = kernelspec
        notebook.metadata.get("jupytext", {}).pop("main_language")

