
def _render_to_html_as_root_streaming(
    root_node: rendering_parts.RenderableTreePart,
    roundtrip: bool,
    deferreds: Sequence[foldable_impl.DeferredWithThunk],
    ignore_exceptions: bool = False,
) -> Iterator[str]:
  """Helper function: renders a root node to HTML one step at a time.

  Args:
    root_node: The root node to render.
    roundtrip: Whether to render in roundtrip mode.
    deferreds: Sequence of deferred objects to render and splice in.
    ignore_exceptions: Whether to ignore exceptions during deferred rendering,
      replacing them with error markers.

  Yields:
    HTML source for the rendered node, followed by logic to substitute each
    deferred object.
  """
  all_css_styles = set()
  all_js_defns = set()

  def _render_one(
      node,
      at_beginning_of_line: bool,
      render_context: dict[Any, Any],
      stream: io.StringIO,
  ):
    # Extract setup rules.
    html_context_for_setup = part_interface.HtmlContextForSetup(
        collapsed_selector=foldable_impl.COLLAPSED_SELECTOR,
        roundtrip_selector=foldable_impl.ROUNDTRIP_SELECTOR,
        abbreviate_selector=foldable_impl.make_abbreviate_selector(
            threshold=abbreviation.abbreviation_threshold.get(),
            roundtrip_threshold=(
                abbreviation.roundtrip_abbreviation_threshold.get()
            ),
        ),
    )
    setup_parts = node.html_setup_parts(html_context_for_setup)
    current_styles = []
    current_js_defns = []
    for part in setup_parts:
      if isinstance(part, part_interface.CSSStyleRule):
        if part not in all_css_styles:
          current_styles.append(part)
          all_css_styles.add(part)
      elif isinstance(part, part_interface.JavaScriptDefn):
        if part not in all_js_defns:
          current_js_defns.append(part)
          all_js_defns.add(part)
      else:
        raise ValueError(f"Invalid setup object: {part}")

    if current_styles:
      stream.write("<style>")
      for css_style in sorted(current_styles):
        stream.write(css_style.rule)
      stream.write("</style>")

    if current_js_defns:
      stream.write(
          "<treescope-run-here><script type='application/octet-stream'>"
      )
      for js_defn in sorted(current_js_defns):
        stream.write(js_defn.source)
      stream.write("</script></treescope-run-here>")

    # Render the node itself.
    node.render_to_html(
        stream,
        at_beginning_of_line=at_beginning_of_line,
        render_context=render_context,
    )

  # Set up the styles and scripts for the root object.
  stream = io.StringIO()
  stream.write("<style>")
  stream.write(html_escaping.without_repeated_whitespace("""
    .treescope_root {
      position: relative;
      font-family: monospace;
      white-space: pre;
      list-style-type: none;
      background-color: white;
      color: black;
      width: fit-content;
      min-width: 100%;
      box-sizing: border-box;
      padding-left: 2ch;
      line-height: 1.5;
      contain: content;
      content-visibility: auto;
      contain-intrinsic-size: auto none;
    }
  """))
  stream.write("</style>")
  # These scripts allow us to defer execution of javascript blocks until after
  # the content is loaded, avoiding locking up the browser rendering process.
  stream.write("<treescope-run-here><script type='application/octet-stream'>")
  stream.write(
      html_escaping.without_repeated_whitespace(_TREESCOPE_PREAMBLE_SCRIPT)
  )
  stream.write("</script></treescope-run-here>")

  # Render the root node.
  classnames = "treescope_root"
  if roundtrip:
    classnames += " roundtrip_mode"
  stream.write(
      f'<div class="{classnames}" tabindex="0" '
      'part="treescope_root" '
      'onkeydown="this.getRootNode().host.defns'
      '.toggle_root_roundtrip(this, event)">'
  )
  _render_one(root_node, True, {}, stream)
  stream.write("</div>")

  yield stream.getvalue()

  # Render any deferred parts. We insert each part into a hidden element, then
  # move them all out to their appropriate positions.
  if deferreds:
    stream = io.StringIO()
    for deferred in deferreds:
      stream.write(
          '<div style="display: none"'
          f' id="for_{deferred.placeholder.replacement_id}"><span>'
      )
      if (
          deferred.placeholder.saved_at_beginning_of_line is None
          or deferred.placeholder.saved_render_context is None
      ):
        replacement_part = rendering_parts.error_color(
            rendering_parts.text("<deferred rendering error>")
        )
      else:
        if deferred.placeholder.needs_layout_decision:
          assert isinstance(
              deferred.placeholder.child, part_interface.FoldableTreeNode
          )
          layout_decision = deferred.placeholder.child.get_expand_state()
        else:
          layout_decision = None
        try:
          replacement_part = deferred.thunk(layout_decision)
        except Exception as e:  # pylint: disable=broad-except
          if not ignore_exceptions:
            raise
          exc_child = rendering_parts.fold_condition(
              expanded=rendering_parts.indented_children(
                  [rendering_parts.text(traceback.format_exc())]
              ),
          )
          replacement_part = rendering_parts.error_color(
              rendering_parts.build_custom_foldable_tree_node(
                  label=rendering_parts.text(
                      f"<{type(e).__name__} during deferred rendering"
                  ),
                  contents=rendering_parts.siblings(
                      exc_child, rendering_parts.text(">")
                  ),
              ).renderable
          )
      _render_one(
          replacement_part,
          deferred.placeholder.saved_at_beginning_of_line,
          deferred.placeholder.saved_render_context,
          stream,
      )
      stream.write("</span></div>")

    all_ids = [deferred.placeholder.replacement_id for deferred in deferreds]
    # It's sometimes important to preserve node identity when inserting
    # deferred objects, for instance if we've already registered event listeners
    # on some nodes. However, editing the DOM in place can be slow because it
    # requires re-rendering the tree on every edit. To avoid this, we swap out
    # the tree with a clone, edit the original tree, then swap the original
    # tree back in.
    inner_script = (
        f"const targetIds = {json.dumps(all_ids)};"
        + html_escaping.without_repeated_whitespace("""
        const docroot = this.getRootNode();
        const treeroot = docroot.querySelector(".treescope_root");
        const treerootClone = treeroot.cloneNode(true);
        treeroot.replaceWith(treerootClone);
        const fragment = document.createDocumentFragment();
        fragment.appendChild(treeroot);
        for (let i = 0; i < targetIds.length; i++) {
            let target = fragment.getElementById(targetIds[i]);
            let sourceDiv = docroot.querySelector("#for_" + targetIds[i]);
            target.replaceWith(sourceDiv.firstElementChild);
            sourceDiv.remove();
        }
        treerootClone.replaceWith(treeroot);
        """)
    )
    stream.write(
        '<treescope-run-here><script type="application/octet-stream">'
        f"{inner_script}</script></treescope-run-here>"
    )
    yield stream.getvalue()

