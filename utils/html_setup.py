
def html_setup() -> (
    set[part_interface.CSSStyleRule | part_interface.JavaScriptDefn]
):
  """Builds the setup HTML that should be included in any arrayviz output."""
  arrayviz_src = html_escaping.heuristic_strip_javascript_comments(
      load_arrayvis_javascript()
  )
  return {
      part_interface.CSSStyleRule(html_escaping.without_repeated_whitespace("""
        .arrayviz_container {
            white-space: normal;
        }
        .arrayviz_container .info {
            font-family: monospace;
            color: #aaaaaa;
            margin-bottom: 0.25em;
            white-space: pre;
        }
        .arrayviz_container .info input[type="range"] {
            vertical-align: middle;
            filter: grayscale(1) opacity(0.5);
        }
        .arrayviz_container .info input[type="range"]:hover {
            filter: grayscale(0.5);
        }
        .arrayviz_container .info input[type="number"]:not(:focus) {
            border-radius: 3px;
        }
        .arrayviz_container .info input[type="number"]:not(:focus):not(:hover) {
            color: #777777;
            border: 1px solid #777777;
        }
        .arrayviz_container .info.sliders {
            white-space: pre;
        }
        .arrayviz_container .hovertip {
            display: none;
            position: absolute;
            background-color: white;
            border: 1px solid black;
            padding: 0.25ch;
            pointer-events: none;
            width: fit-content;
            overflow: visible;
            white-space: pre;
            z-index: 1000;
        }
        .arrayviz_container .hoverbox {
            display: none;
            position: absolute;
            box-shadow: 0 0 0 1px black, 0 0 0 2px white;
            pointer-events: none;
            z-index: 900;
        }
        .arrayviz_container .clickdata {
            white-space: pre;
        }
        .arrayviz_container .loading_message {
            color: #aaaaaa;
        }
      """)),
      part_interface.JavaScriptDefn(
          arrayviz_src + " this.getRootNode().host.defns.arrayviz = arrayviz;"
      ),
  }

