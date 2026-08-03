from typing import Any

def build_foldable_representation(
    value: Any,
    ignore_exceptions: bool = False,
) -> rendering_parts.RenderableAndLineAnnotations:
  """Builds a foldable representation of an object using default configuration.

  Uses the default renderer and expansion strategy.

  Args:
    value: Value to render.
    ignore_exceptions: Whether to catch errors during rendering of subtrees and
      show a fallback for those subtrees, instead of failing the entire
      renderer. Best used in contexts where `value_to_foldable_html` is not
      being called directly, e.g. when registering this as a default
      pretty-printer.

  Returns:
    A text representation of the object.
  """
  foldable_ir_with_annotations = (
      active_renderer.get().to_foldable_representation(
          value, ignore_exceptions=ignore_exceptions
      )
  )
  # Expand the renderable ignoring its annotations.
  active_expansion_strategy.get()(foldable_ir_with_annotations.renderable)
  return foldable_ir_with_annotations

