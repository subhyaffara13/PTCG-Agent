
def _common_block_rules(
    context: HtmlContextForSetup,
) -> dict[str, CSSStyleRule]:
  return {
      "colored_line": CSSStyleRule(html_escaping.without_repeated_whitespace("""
            .colored_line
            {
              color: black;
              background-color: var(--block-color);
              border-top: 1px solid var(--block-color);
              border-bottom: 1px solid var(--block-color);
            }
          """)),
      "patterned_line": CSSStyleRule(
          html_escaping.without_repeated_whitespace("""
            .patterned_line
            {
              color: black;
              border: 1px solid var(--block-color);
              background-image: var(--block-background-image);
              background-clip: padding-box;
            }
          """)
      ),
      "topline": CSSStyleRule(html_escaping.without_repeated_whitespace(f"""
            .topline:not({context.collapsed_selector} *)
            {{
              padding-bottom: 0.15em;
              line-height: 1.5em;
              z-index: 1;
              position: relative;
            }}
          """)),
      "bottomline": CSSStyleRule(html_escaping.without_repeated_whitespace(f"""
            .bottomline:not({context.collapsed_selector} *)
            {{
              padding-top: 0.15em;
              line-height: 1.5em;
              z-index: 1;
              position: relative;
            }}
          """)),
      "hch_space_left": CSSStyleRule(
          html_escaping.without_repeated_whitespace("""
            .hch_space_left
            {
              padding-left: 0.5ch;
            }
          """)
      ),
      "hch_space_right": CSSStyleRule(
          html_escaping.without_repeated_whitespace("""
            .hch_space_right
            {
              padding-right: 0.5ch;
            }
          """)
      ),
  }

