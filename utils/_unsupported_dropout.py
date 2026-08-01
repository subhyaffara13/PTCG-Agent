
def _unsupported_dropout(name: str):
    @symbolic_helper.parse_args("v", "none", "b")
    def feature_dropout(g, input, p, train):
        # NB: In inference mode, FeatureDropout is exported as an identity op.
        if train:
            return symbolic_helper._unimplemented(name, "training mode", input)
        return input

    return feature_dropout

