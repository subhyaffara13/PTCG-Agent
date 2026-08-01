
def clipboard(qapp):
    clip = qapp.clipboard()
    yield clip
    clip.clear()

