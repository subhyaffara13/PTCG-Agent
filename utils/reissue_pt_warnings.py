
def reissue_pt_warnings(caught_warnings):
    # Reissue warnings
    if len(caught_warnings) > 1:
        for w in caught_warnings:
            if w.category is not UserWarning:
                warnings.warn(w.message, w.category)

