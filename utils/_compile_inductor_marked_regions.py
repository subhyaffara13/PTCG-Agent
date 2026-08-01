
def _compile_inductor_marked_regions(gm):
    with torch.fx.traceback.preserve_node_meta(enable=False):
        return _RegionCompiler()(gm)

