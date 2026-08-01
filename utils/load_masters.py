
def load_masters(designspace, master_finder=lambda s: s):
    """Ensure that all SourceDescriptor.font attributes have an appropriate TTFont
    object loaded, or else open TTFont objects from the SourceDescriptor.path
    attributes.

    The paths can point to either an OpenType font, a TTX file, or a UFO. In the
    latter case, use the provided master_finder callable to map from UFO paths to
    the respective master font binaries (e.g. .ttf, .otf or .ttx).

    Return list of master TTFont objects in the same order they are listed in the
    DesignSpaceDocument.
    """
    for master in designspace.sources:
        # If a SourceDescriptor has a layer name, demand that the compiled TTFont
        # be supplied by the caller. This spares us from modifying MasterFinder.
        if master.layerName and master.font is None:
            raise VarLibValidationError(
                f"Designspace source '{master.name or '<Unknown>'}' specified a "
                "layer name but lacks the required TTFont object in the 'font' "
                "attribute."
            )

    return designspace.loadSourceFonts(_open_font, master_finder=master_finder)

