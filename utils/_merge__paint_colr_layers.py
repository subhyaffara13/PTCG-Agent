
def _merge_PaintColrLayers(self, out, lst):
    # we only enforce that the (flat) number of layers is the same across all masters
    # but we allow FirstLayerIndex to differ to acommodate for sparse glyph sets.

    out_layers = list(_flatten_layers(out, self.font["COLR"].table))

    # sanity check ttfs are subset to current values (see VariationMerger.mergeThings)
    # before matching each master PaintColrLayers to its respective COLR by position
    assert len(self.ttfs) == len(lst)
    master_layerses = [
        list(_flatten_layers(lst[i], self.ttfs[i]["COLR"].table))
        for i in range(len(lst))
    ]

    try:
        self.mergeLists(out_layers, master_layerses)
    except VarLibMergeError as e:
        # NOTE: This attribute doesn't actually exist in PaintColrLayers but it's
        # handy to have it in the stack trace for debugging.
        e.stack.append(".Layers")
        raise

    # following block is very similar to LayerListBuilder._beforeBuildPaintColrLayers
    # but I couldn't find a nice way to share the code between the two...

    if self.layerReuseCache is not None:
        # successful reuse can make the list smaller
        out_layers = self.layerReuseCache.try_reuse(out_layers)

    # if the list is still too big we need to tree-fy it
    is_tree = len(out_layers) > MAX_PAINT_COLR_LAYER_COUNT
    out_layers = build_n_ary_tree(out_layers, n=MAX_PAINT_COLR_LAYER_COUNT)

    # We now have a tree of sequences with Paint leaves.
    # Convert the sequences into PaintColrLayers.
    def listToColrLayers(paint):
        if isinstance(paint, list):
            layers = [listToColrLayers(l) for l in paint]
            paint = ot.Paint()
            paint.Format = int(ot.PaintFormat.PaintColrLayers)
            paint.NumLayers = len(layers)
            paint.FirstLayerIndex = len(self.layers)
            self.layers.extend(layers)
            if self.layerReuseCache is not None:
                self.layerReuseCache.add(layers, paint.FirstLayerIndex)
        return paint

    out_layers = [listToColrLayers(l) for l in out_layers]

    if len(out_layers) == 1 and out_layers[0].Format == ot.PaintFormat.PaintColrLayers:
        # special case when the reuse cache finds a single perfect PaintColrLayers match
        # (it can only come from a successful reuse, _flatten_layers has gotten rid of
        # all nested PaintColrLayers already); we assign it directly and avoid creating
        # an extra table
        out.NumLayers = out_layers[0].NumLayers
        out.FirstLayerIndex = out_layers[0].FirstLayerIndex
    else:
        out.NumLayers = len(out_layers)
        out.FirstLayerIndex = len(self.layers)

        self.layers.extend(out_layers)

        # Register our parts for reuse provided we aren't a tree
        # If we are a tree the leaves registered for reuse and that will suffice
        if self.layerReuseCache is not None and not is_tree:
            self.layerReuseCache.add(out_layers, out.FirstLayerIndex)

