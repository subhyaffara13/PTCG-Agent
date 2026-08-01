
def maybe_defer_rendering(
    main_thunk: Callable[
        [rendering_parts.ExpandState | None],
        rendering_parts.RenderableTreePart,
    ],
    placeholder_thunk: Callable[[], rendering_parts.RenderableTreePart],
    expanded_newlines_for_layout: int | None = None,
) -> rendering_parts.RenderableTreePart:
  """Possibly defers rendering of a part in interactive contexts.

  This function can be used by advanced handlers and autovisualizers to delay
  the rendering of "expensive" leaves such as `jax.Array` until after the tree
  structure is drawn. If run in a non-interactive context, this just calls the
  main thunk. If run in an interactive context, it instead calls the placeholder
  thunk, and enqueues the placeholder thunk to be called later.

  Rendering can be performed in a deferred context by running the handlers under
  the `collecting_deferred_renderings` context manager, and then rendered to
  a sequence of streaming HTML updates using the `display_streaming_as_root`
  function.

  Note that handlers who call this are responsible for ensuring that the
  logic in `main_thunk` is safe to run at a later point in time. In particular,
  any rendering context managers may have been exited by the time this main
  thunk is called. As a best practice, handlers should control all of the logic
  in `main_thunk` and shouldn't recursively call the subtree renderer inside it;
  subtrees should be rendered before calling `maybe_defer_rendering`.

  Args:
    main_thunk: A callable producing the main part to render. If deferred and if
      ``expanded_newlines_for_layout`` is not None, this will be called with the
      inferred final expand state of placeholder after layout decisions.
      Otherwise, will be called with None.
    placeholder_thunk: A callable producing a placeholder object, which will be
      rendered if we are deferring rendering.
    expanded_newlines_for_layout: A guess at the extra height of this node after
      it has been expanded. If not None, this node will participate in the
      layout algorithm as if it had this height, and the final inferred
      expansion state will be passed to ``main_thunk``.

  Returns:
    Either the rendered main part or a wrapped placeholder that will later be
    replaced with the main part.
  """
  deferral_list = _deferrables.get()
  if deferral_list is None:
    return main_thunk(None)
  else:
    if expanded_newlines_for_layout is None:
      needs_layout_decision = False
      child = placeholder_thunk()
    else:
      needs_layout_decision = True
      child = foldable_impl.fake_placeholder_foldable(
          placeholder_thunk(), extra_newlines_guess=expanded_newlines_for_layout
      )
    placeholder = foldable_impl.DeferredPlaceholder(
        child=child,
        replacement_id="deferred_" + uuid.uuid4().hex,
        needs_layout_decision=needs_layout_decision,
    )
    deferral_list.append(
        foldable_impl.DeferredWithThunk(placeholder, main_thunk)
    )
    return placeholder

