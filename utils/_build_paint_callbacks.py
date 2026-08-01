
def _buildPaintCallbacks():
    return {
        (
            BuildCallback.BEFORE_BUILD,
            ot.Paint,
            ot.PaintFormat.PaintRadialGradient,
        ): _beforeBuildPaintRadialGradient,
        (
            BuildCallback.BEFORE_BUILD,
            ot.Paint,
            ot.PaintFormat.PaintVarRadialGradient,
        ): _beforeBuildPaintRadialGradient,
        (BuildCallback.CREATE_DEFAULT, ot.ColorStop): _defaultColorStop,
        (BuildCallback.CREATE_DEFAULT, ot.VarColorStop): _defaultVarColorStop,
        (BuildCallback.CREATE_DEFAULT, ot.ColorLine): _defaultColorLine,
        (BuildCallback.CREATE_DEFAULT, ot.VarColorLine): _defaultVarColorLine,
        (
            BuildCallback.CREATE_DEFAULT,
            ot.Paint,
            ot.PaintFormat.PaintSolid,
        ): _defaultPaintSolid,
        (
            BuildCallback.CREATE_DEFAULT,
            ot.Paint,
            ot.PaintFormat.PaintVarSolid,
        ): _defaultPaintSolid,
    }

