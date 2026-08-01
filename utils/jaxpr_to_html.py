
def jaxpr_to_html(jaxpr: core.Jaxpr) -> str:
  """Renders a Jaxpr as HTML with interactive tracebacks and search."""

  # 1. Render jaxpr to string and get source map
  source_map_output: list[list[tuple[int, int, Any]]] = []
  rendered_str = jaxpr.pretty_print(
      source_map=source_map_output,
      use_color=True,
      output_format=pp.OutputFormat.HTML,
      separable_lines=True,
  )

  # 2. Process source map and build traceback DAG
  raw_frame_to_idx: dict[tuple[types.CodeType, int], int] = {}
  dag_nodes: list[dict[str, int | None]] = []
  node_to_idx: dict[tuple[int, int | None], int] = {}
  tb_to_node_idx: dict[Any, int | None] = {}

  def get_frame_idx(code: types.CodeType, lasti: int) -> int:
    key = (code, lasti)
    idx = raw_frame_to_idx.get(key)
    if idx is None:
      idx = len(raw_frame_to_idx)
      raw_frame_to_idx[key] = idx
    return idx

  def get_node_idx(frame_idx: int, parent_node_idx: int | None) -> int:
    key = (frame_idx, parent_node_idx)
    idx = node_to_idx.get(key)
    if idx is None:
      idx = len(dag_nodes)
      dag_nodes.append({"frame_idx": frame_idx, "parent": parent_node_idx})
      node_to_idx[key] = idx
    return idx

  def process_tb(tb: Any) -> int | None:
    idx = tb_to_node_idx.get(tb)
    if idx is not None:
      return idx

    code, lasti = tb.raw_frames()

    parent_node_idx = None
    # raw_frames gives inner to outer. We iterate from outer to inner.
    for i in reversed(range(len(code))):
      frame_idx = get_frame_idx(code[i], lasti[i])
      parent_node_idx = get_node_idx(frame_idx, parent_node_idx)

    tb_to_node_idx[tb] = parent_node_idx
    return parent_node_idx

  # 3. Generate HTML lines with spans
  lines = rendered_str.splitlines()
  html_lines = []
  line_to_nodes = defaultdict(set)

  for i, line in enumerate(lines):
    spans = source_map_output[i] if i < len(source_map_output) else []
    # Sort spans by start column
    spans.sort(key=lambda x: x[0])

    result = []
    last_idx = 0
    for start, end, tb in spans:
      if start > last_idx:
        result.append(line[last_idx:start])

      tb_node_idx = process_tb(tb)
      if tb_node_idx is not None:
        result.append(f'<span class="traceable" data-tb-idx="{tb_node_idx}">')
        result.append(line[start:end])
        result.append("</span>")
        line_to_nodes[i].add(tb_node_idx)
      else:
        result.append(line[start:end])
      last_idx = end

    if last_idx < len(line):
      result.append(line[last_idx:])

    html_lines.append("".join(result))

  # 4. Convert raw frames to final Frame representations with string pooling
  final_frames = []
  string_to_idx: dict[str, int] = {}

  def get_string_idx(s: str) -> int:
    idx = string_to_idx.get(s)
    if idx is None:
      idx = len(string_to_idx)
      string_to_idx[s] = idx
    return idx

  for code, lasti in raw_frame_to_idx:
    frame = source_info_util.raw_frame_to_frame(code, lasti)
    pattern = config.hlo_source_file_canonicalization_regex.value
    file_name = (
        re.sub(pattern, "", frame.file_name) if pattern else frame.file_name
    )
    final_frames.append({
        "file_idx": get_string_idx(file_name),
        "func_idx": get_string_idx(frame.function_name),
        "line": frame.start_line,
        "col": frame.start_column,
    })

  # 5. Build string_to_lines map
  string_to_lines = defaultdict(set)
  for i, node_indices in line_to_nodes.items():
    for node_idx in node_indices:
      curr = node_idx
      while curr is not None:
        node = dag_nodes[curr]
        frame_data = final_frames[node["frame_idx"]]
        string_to_lines[frame_data["file_idx"]].add(i)
        string_to_lines[frame_data["func_idx"]].add(i)
        curr = node["parent"]

  # 5. Construct final HTML and compress data

  data = {
      "frames": final_frames,
      "dag": dag_nodes,
      "strings": list(string_to_idx),
      "lines": html_lines,
      "string_to_lines": {str(k): list(v) for k, v in string_to_lines.items()},
  }

  json_data = json.dumps(data)
  compressed_data = gzip.compress(json_data.encode("utf-8"))
  base64_data = base64.b64encode(compressed_data).decode("utf-8")

  source_url_schema = config.source_url_schema.value or ""
  html_content = f"""
<!DOCTYPE html>
<html>
<head>
<style>
  body {{
    display: flex;
    font-family: monospace;
    margin: 0;
    height: 100vh;
  }}
  #left-pane-wrapper {{
    flex: 7;
    display: flex;
    overflow: hidden;
  }}
  #jaxpr-container {{
    flex: 1;
    overflow: auto;
    padding: 10px;
    background-color: #f5f5f5;
    line-height: 18px;
    font-size: 14px;
  }}
  .line {{
    height: 18px;
    white-space: pre;
  }}
  #pane-divider {{
    width: 5px;
    cursor: col-resize;
    background-color: #ccc;
  }}
  #side-pane {{
    flex: 3;
    overflow: auto;
    padding: 10px;
    background-color: #fff;
    border-left: 1px solid #ccc;
  }}
  #mini-map {{
    width: 30px;
    background-color: #f0f0f0;
    border-left: 1px solid #ddd;
    cursor: pointer;
  }}
  .traceable {{
    cursor: pointer;
    background-color: #e8f0fe;
  }}
  .traceable:hover {{
    background-color: #d2e3fc;
  }}
  .selected {{
    background-color: #aecbfa;
  }}
  .search-match {{
    background-color: #fff59d;
  }}
  .current-match {{
    background-color: #fff59d;
    border: 1px solid #f57f17;
    box-sizing: border-box;
  }}
  .frame {{
    margin-bottom: 8px;
    border-bottom: 1px solid #eee;
    padding-bottom: 4px;
  }}
  .frame-file {{ color: #5f6368; }}
  .frame-func {{ color: #1a73e8; font-weight: bold; }}
  .frame-loc {{ color: #80868b; }}
  .ansi-fg-30 {{ color: black; }}
  .ansi-fg-31 {{ color: #ea4335; }} /* red */
  .ansi-fg-32 {{ color: #34a853; }} /* green */
  .ansi-fg-33 {{ color: #fbcb05; }} /* yellow */
  .ansi-fg-34 {{ color: #4285f4; }} /* blue */
  .ansi-fg-35 {{ color: #a142f4; }} /* magenta */
  .ansi-fg-36 {{ color: #24b6d2; }} /* cyan */
  .ansi-fg-37 {{ color: white; }}
  .ansi-bg-40 {{ background-color: black; }}
  .ansi-bg-41 {{ background-color: #ea4335; }} /* red */
  .ansi-bg-42 {{ background-color: #34a853; }} /* green */
  .ansi-bg-43 {{ background-color: #fbcb05; }} /* yellow */
  .ansi-bg-44 {{ background-color: #4285f4; }} /* blue */
  .ansi-bg-45 {{ background-color: #a142f4; }} /* magenta */
  .ansi-bg-46 {{ background-color: #24b6d2; }} /* cyan */
  .ansi-bg-47 {{ background-color: white; }}
  .ansi-intensity-1 {{ font-weight: bold; }}
  .ansi-intensity-2 {{ opacity: 0.6; }}
  @keyframes flash {{
    0% {{ background-color: #fff59d; }}
    100% {{ background-color: transparent; }}
  }}
  .jump-highlight {{
    animation: flash 1.5s ease-out forwards;
  }}
  #search-controls {{
    margin-bottom: 10px;
  }}
  #search-input {{
    width: 60%;
  }}
</style>
</head>
<body>

<div id="left-pane-wrapper">
  <div id="jaxpr-container">
    <div id="virtual-scroll-spacer" style="position: relative;">
      <div id="visible-lines-container" style="position: absolute; top: 0; left: 0; right: 0;"></div>
    </div>
  </div>
  <canvas id="mini-map"></canvas>
</div>

<div id="pane-divider"></div>

<div id="side-pane">
  <h3>Search</h3>
  <div id="search-controls">
    <input type="text" id="search-input" placeholder="Search jaxpr...">
    <button id="search-prev">&lt;</button>
    <button id="search-next">&gt;</button>
    <span id="search-count"></span>
  </div>
  <div id="total-lines"></div>
  <hr>
  <h3>Traceback</h3>
  <div id="traceback-content">Click on a shaded line to see the traceback.</div>
</div>

<script>
  async function decompress(base64Data) {{
    const binary = atob(base64Data);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {{
      bytes[i] = binary.charCodeAt(i);
    }}
    const stream = new Response(bytes).body.pipeThrough(new DecompressionStream('gzip'));
    const result = await new Response(stream).text();
    return JSON.parse(result);
  }}

  const base64Data = "{base64_data}";
  const sourceUrlSchema = "{source_url_schema}";

  decompress(base64Data).then(data => {{
    const frames = data.frames;
    const dag = data.dag;
    const strings = data.strings;
    const allLines = data.lines;
    const stringToLines = data.string_to_lines;

    const varDefinitions = {{}};
    const anchorRegex = /<a id="(?:v_|g_)([^"]+)"/g;
    allLines.forEach((line, idx) => {{
      let match;
      while ((match = anchorRegex.exec(line)) !== null) {{
        const varName = match[1];
        varDefinitions[varName] = idx;
      }}
    }});

    document.getElementById('total-lines').textContent = `Total lines: ${{allLines.length}}`;

    const lineHeight = 18;
    const container = document.getElementById('jaxpr-container');
    const spacer = document.getElementById('virtual-scroll-spacer');
    const visibleContainer = document.getElementById('visible-lines-container');
    const miniMap = document.getElementById('mini-map');
    const miniMapCtx = miniMap.getContext('2d');

    const MAX_HEIGHT = 10000000; // Reduce to 10M pixels to be safer with browser limits
    const totalHeight = allLines.length * lineHeight;
    const useScaling = totalHeight > MAX_HEIGHT;
    const spacerHeight = useScaling ? MAX_HEIGHT : totalHeight;

    spacer.style.height = spacerHeight + 'px';

    const buffer = 5;
    let matchingLines = [];
    let currentMatchIdx = -1;
    let highlightedLineIdx = -1;

    function renderVisibleLines() {{
      const scrollTop = container.scrollTop;
      const containerHeight = container.clientHeight;

      const scale = useScaling ? ((totalHeight - containerHeight) / (MAX_HEIGHT - containerHeight)) : 1.0;
      const virtualScrollTop = scrollTop * scale;

      const startIdx = Math.floor(virtualScrollTop / lineHeight);
      const offset = virtualScrollTop % lineHeight;

      const renderedStartIdx = Math.max(0, startIdx - buffer);
      const actualBuffer = startIdx - renderedStartIdx;

      const endIdx = Math.min(allLines.length, Math.ceil((virtualScrollTop + containerHeight) / lineHeight) + buffer);

      visibleContainer.innerHTML = allLines.slice(renderedStartIdx, endIdx).map((line, idx) => {{
        const lineAbsoluteIdx = renderedStartIdx + idx;
        const isMatch = matchingLines.includes(lineAbsoluteIdx);
        const isCurrent = currentMatchIdx !== -1 && lineAbsoluteIdx === matchingLines[currentMatchIdx];
        const isHighlighted = lineAbsoluteIdx === highlightedLineIdx;

        let className = "line";
        if (isMatch) className += " search-match";
        if (isCurrent) className += " current-match";
        if (isHighlighted) className += " jump-highlight";

        return `<div class="${{className}}">${{line}}</div>`;
      }}).join('');

      if (useScaling) {{
        visibleContainer.style.top = (scrollTop - offset - (actualBuffer * lineHeight)) + 'px';
      }} else {{
        visibleContainer.style.top = (renderedStartIdx * lineHeight) + 'px';
      }}
    }}

    let scrollTicking = false;
    container.addEventListener('scroll', () => {{
      if (!scrollTicking) {{
        window.requestAnimationFrame(() => {{
          renderVisibleLines();
          drawMiniMap();
          scrollTicking = false;
        }});
        scrollTicking = true;
      }}
    }});
    // Removed old resize listener, handled at the bottom
    renderVisibleLines();

    // Event Delegation
    let selectedElement = null;
    container.addEventListener('click', (e) => {{
      const link = e.target.closest('a[href^="#v_"], a[href^="#g_"]');
      if (link) {{
        e.preventDefault();
        const href = link.getAttribute('href');
        const varName = href.substring(3); // strip "#v_" or "#g_"
        const lineIdx = varDefinitions[varName];
        if (lineIdx !== undefined) {{
          scrollToLine(lineIdx);
        }}
        return;
      }}

      const traceable = e.target.closest('.traceable');
      if (traceable) {{
        if (selectedElement) {{
          selectedElement.classList.remove('selected');
        }}
        traceable.classList.add('selected');
        selectedElement = traceable;
        const tbIdx = parseInt(traceable.getAttribute('data-tb-idx'));
        renderTraceback(tbIdx);
      }}
    }});

    function renderTraceback(nodeIdx) {{
      const contentDiv = document.getElementById('traceback-content');
      contentDiv.innerHTML = '';

      let currentIdx = nodeIdx;
      const renderedFrames = [];

      while (currentIdx !== null && currentIdx !== undefined) {{
        const node = dag[currentIdx];
        const frame = frames[node.frame_idx];
        const file = strings[frame.file_idx];
        const func = strings[frame.func_idx];
        renderedFrames.push({{file: file, func: func, line: frame.line, col: frame.col}});
        currentIdx = node.parent;
      }}

      renderedFrames.reverse();

      renderedFrames.forEach(frame => {{
        const frameDiv = document.createElement('div');
        frameDiv.className = 'frame';
        if (sourceUrlSchema) {{
          const url = sourceUrlSchema.replace('{{file}}', frame.file).replace('{{line}}', frame.line);
          frameDiv.innerHTML = `
            <a href="${{url}}" target="_blank">${{escapeHtml(frame.file)}}:${{frame.line}}</a>
            in <span class="frame-func">${{escapeHtml(frame.func)}}</span>
          `;
        }} else {{
          frameDiv.innerHTML = `
            <span class="frame-file">${{escapeHtml(frame.file)}}:${{frame.line}}</span>
            in <span class="frame-func">${{escapeHtml(frame.func)}}</span>
          `;
        }}
        contentDiv.appendChild(frameDiv);
      }});

      if (renderedFrames.length === 0) {{
        contentDiv.innerHTML = 'No traceback information available.';
      }}
    }}

    function escapeHtml(text) {{
      const div = document.createElement('div');
      div.textContent = text;
      return div.innerHTML;
    }}

    // Search Logic
    const searchInput = document.getElementById('search-input');
    const searchPrev = document.getElementById('search-prev');
    const searchNext = document.getElementById('search-next');
    const searchCount = document.getElementById('search-count');

    function performSearch() {{
      const query = searchInput.value.trim().toLowerCase();
      matchingLines = [];
      currentMatchIdx = -1;

      if (query) {{
        // 1. Find matching lines from stringToLines reverse map
        const matchingLinesSet = new Set();
        strings.forEach((str, idx) => {{
          if (str.toLowerCase().includes(query)) {{
            const lines = stringToLines[idx];
            if (lines) {{
              lines.forEach(l => matchingLinesSet.add(l));
            }}
          }}
        }});

        // 2. Combine with direct text matches (fallback/addition)
        allLines.forEach((line, idx) => {{
          if (matchingLinesSet.has(idx)) {{
            matchingLines.push(idx);
          }} else {{
            const text = line.replace(/<[^>]*>/g, '').toLowerCase();
            if (text.includes(query)) {{
              matchingLines.push(idx);
            }}
          }}
        }});
      }}

      updateSearchUI();
      renderVisibleLines();
      drawMiniMap();
    }}

    function updateSearchUI() {{
      if (matchingLines.length > 0) {{
        if (currentMatchIdx === -1) currentMatchIdx = 0;
        searchCount.textContent = `${{currentMatchIdx + 1}} / ${{matchingLines.length}}`;
      }} else {{
        searchCount.textContent = searchInput.value.trim() ? "0 / 0" : "";
        currentMatchIdx = -1;
      }}
    }}

    function scrollToLine(lineIdx) {{
      const containerHeight = container.clientHeight;
      const scale = useScaling ? ((totalHeight - containerHeight) / (MAX_HEIGHT - containerHeight)) : 1.0;
      const virtualScrollTop = lineIdx * lineHeight;
      const scrollTop = useScaling ? (virtualScrollTop / scale) : virtualScrollTop;

      container.scrollTop = scrollTop;
      highlightedLineIdx = lineIdx;
      renderVisibleLines();

      setTimeout(() => {{
        if (highlightedLineIdx === lineIdx) {{
          highlightedLineIdx = -1;
        }}
      }}, 1500);
    }}

    function goToMatch(idx) {{
      if (matchingLines.length === 0) return;
      currentMatchIdx = (idx + matchingLines.length) % matchingLines.length;
      updateSearchUI();

      const lineIdx = matchingLines[currentMatchIdx];
      scrollToLine(lineIdx);
      drawMiniMap();
    }}

    function drawMiniMap() {{
      const width = miniMap.clientWidth;
      const height = miniMap.clientHeight;
      miniMap.width = width;
      miniMap.height = height;

      miniMapCtx.clearRect(0, 0, width, height);

      if (allLines.length === 0) return;

      // Draw search matches
      miniMapCtx.fillStyle = '#fff59d';
      matchingLines.forEach(lineIdx => {{
        const y = (lineIdx / allLines.length) * height;
        miniMapCtx.fillRect(0, y, width, 2);
      }});

      // Draw current match
      if (currentMatchIdx !== -1) {{
        const lineIdx = matchingLines[currentMatchIdx];
        const y = (lineIdx / allLines.length) * height;
        miniMapCtx.fillStyle = '#f57f17';
        miniMapCtx.fillRect(0, y - 1, width, 4);
      }}

      // Draw viewport highlight
      const scrollTop = container.scrollTop;
      const containerHeight = container.clientHeight;
      const scale = useScaling ? ((totalHeight - containerHeight) / (MAX_HEIGHT - containerHeight)) : 1.0;
      const virtualScrollTop = scrollTop * scale;

      const viewportStartLine = virtualScrollTop / lineHeight;
      const viewportEndLine = (virtualScrollTop + containerHeight) / lineHeight;

      const yStart = (viewportStartLine / allLines.length) * height;
      const yEnd = (viewportEndLine / allLines.length) * height;

      miniMapCtx.fillStyle = 'rgba(0, 0, 0, 0.1)';
      miniMapCtx.fillRect(0, yStart, width, yEnd - yStart);
      miniMapCtx.strokeStyle = 'rgba(0, 0, 0, 0.3)';
      miniMapCtx.strokeRect(0, yStart, width, yEnd - yStart);
    }}

    window.addEventListener('resize', () => {{
      renderVisibleLines();
      drawMiniMap();
    }});

    miniMap.addEventListener('click', (e) => {{
      const rect = miniMap.getBoundingClientRect();
      const y = e.clientY - rect.top;
      const height = rect.height;
      const lineIdx = Math.floor((y / height) * allLines.length);
      scrollToLine(Math.min(lineIdx, allLines.length - 1));
    }});

    searchInput.addEventListener('input', performSearch);
    searchPrev.addEventListener('click', () => goToMatch(currentMatchIdx - 1));
    searchNext.addEventListener('click', () => goToMatch(currentMatchIdx + 1));

    // Initial draw
    drawMiniMap();
  }});

  // Simple resizable pane logic
  const divider = document.getElementById('pane-divider');
  const leftPane = document.getElementById('jaxpr-container');
  const rightPane = document.getElementById('side-pane');

  let isResizing = false;

  divider.addEventListener('mousedown', (e) => {{
    isResizing = true;
    document.body.style.cursor = 'col-resize';
    e.preventDefault();
  }});

  document.addEventListener('mousemove', (e) => {{
    if (!isResizing) return;
    const offsetRight = document.body.clientWidth - e.clientX;

    if (offsetRight > 100 && offsetRight < document.body.clientWidth - 100) {{
      rightPane.style.flex = 'none';
      rightPane.style.width = offsetRight + 'px';
    }}
  }});

  document.addEventListener('mouseup', () => {{
    isResizing = false;
    document.body.style.cursor = 'default';
  }});
</script>

</body>
</html>
"""
  return html_content

