import json

def notebook_model(nb):
    """Return a notebook model, with content a
    dictionary rather than a notebook object.
    To be used in tests only."""
    return dict(type="notebook", content=json.loads(json.dumps(nb)))

