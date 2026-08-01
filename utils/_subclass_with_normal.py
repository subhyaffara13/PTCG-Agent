
def _subclass_with_normal(effect_class):
    """
    Create a PathEffect class combining *effect_class* and a normal draw.
    """

    class withEffect(effect_class):
        def draw_path(self, renderer, gc, tpath, affine, rgbFace):
            super().draw_path(renderer, gc, tpath, affine, rgbFace)
            renderer.draw_path(gc, tpath, affine, rgbFace)

    withEffect.__name__ = f"with{effect_class.__name__}"
    withEffect.__qualname__ = f"with{effect_class.__name__}"
    withEffect.__doc__ = f"""
    A shortcut PathEffect for applying `.{effect_class.__name__}` and then
    drawing the original Artist.

    With this class you can use ::

        artist.set_path_effects([patheffects.with{effect_class.__name__}()])

    as a shortcut for ::

        artist.set_path_effects([patheffects.{effect_class.__name__}(),
                                 patheffects.Normal()])
    """
    # Docstring inheritance doesn't work for locally-defined subclasses.
    withEffect.draw_path.__doc__ = effect_class.draw_path.__doc__
    return withEffect

