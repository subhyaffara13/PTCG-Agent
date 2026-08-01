
def _build_authorize_html(
    server_name: str,
    server_initial: str,
    client_id: str,
    redirect_uri: str,
    code_challenge: str,
    code_challenge_method: str,
    state: str,
    server_id: str,
    access_items: list,
    help_url: str,
) -> str:
    """Build the 2-step BYOK OAuth authorization page HTML."""

    # Escape all user-supplied / externally-derived values before interpolation
    e = _html_module.escape
    server_name = e(server_name)
    server_initial = e(server_initial)
    client_id = e(client_id)
    redirect_uri = e(redirect_uri)
    code_challenge = e(code_challenge)
    code_challenge_method = e(code_challenge_method)
    state = e(state)
    server_id = e(server_id)

    # Build access checklist rows
    access_rows = "".join(
        f'<div class="access-item"><span class="check">&#10003;</span>{e(item)}</div>'
        for item in access_items
    )
    access_section = ""
    if access_rows:
        access_section = f"""
        <div class="access-box">
          <div class="access-header">
            <span class="shield">&#9646;</span>
            <span>Requested Access</span>
          </div>
          {access_rows}
        </div>"""

    # Help link for step 2
    help_link_html = ""
    if help_url:
        help_link_html = f'<a class="help-link" href="{e(help_url)}" target="_blank">Where do I find my API key? &#8599;</a>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Connect {server_name} &mdash; LiteLLM</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #0f172a;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
  }}
  .modal {{
    background: #ffffff;
    border-radius: 20px;
    padding: 36px 32px 32px;
    width: 440px;
    max-width: 100%;
    position: relative;
    box-shadow: 0 25px 60px rgba(0,0,0,0.35);
  }}
  /* Progress dots */
  .dots {{
    display: flex;
    justify-content: center;
    gap: 7px;
    margin-bottom: 28px;
  }}
  .dot {{
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #e2e8f0;
  }}
  .dot.active {{ background: #38bdf8; }}
  /* Close button */
  .close-btn {{
    position: absolute;
    top: 16px; right: 16px;
    background: none; border: none;
    font-size: 16px; color: #94a3b8;
    cursor: pointer; line-height: 1;
    width: 28px; height: 28px;
    border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
  }}
  .close-btn:hover {{ background: #f1f5f9; color: #475569; }}
  /* Logo pair */
  .logos {{
    display: flex; align-items: center; justify-content: center;
    gap: 12px; margin-bottom: 20px;
  }}
  .logo {{
    width: 52px; height: 52px;
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; font-weight: 800; color: white;
  }}
  .logo-img {{
    width: 52px; height: 52px;
    border-radius: 14px;
    object-fit: cover;
    border: 1.5px solid #e2e8f0;
  }}
  .logo-s {{ background: linear-gradient(135deg, #818cf8 0%, #4f46e5 100%); }}
  .logo-arrow {{ color: #cbd5e1; font-size: 20px; font-weight: 300; }}
  /* Headings */
  .step-title {{
    text-align: center;
    font-size: 21px; font-weight: 700;
    color: #0f172a; margin-bottom: 8px;
  }}
  .step-subtitle {{
    text-align: center;
    font-size: 14px; color: #64748b;
    line-height: 1.55; margin-bottom: 22px;
  }}
  /* Info box */
  .info-box {{
    background: #f8fafc;
    border-radius: 12px;
    padding: 14px 16px;
    display: flex; gap: 12px;
    margin-bottom: 14px;
  }}
  .info-icon {{ font-size: 17px; flex-shrink: 0; margin-top: 1px; color: #38bdf8; }}
  .info-box h4 {{ font-size: 13px; font-weight: 600; color: #1e293b; margin-bottom: 4px; }}
  .info-box p {{ font-size: 13px; color: #64748b; line-height: 1.5; }}
  /* Access checklist */
  .access-box {{
    background: #f8fafc;
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 22px;
  }}
  .access-header {{
    display: flex; align-items: center; gap: 8px;
    margin-bottom: 10px;
  }}
  .shield {{ color: #22c55e; font-size: 15px; }}
  .access-header > span:last-child {{
    font-size: 11px; font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: #475569;
  }}
  .access-item {{
    display: flex; align-items: center; gap: 9px;
    font-size: 13.5px; color: #374151;
    padding: 3px 0;
  }}
  .check {{ color: #22c55e; font-weight: 700; font-size: 13px; }}
  /* Primary CTA */
  .btn-primary {{
    width: 100%; padding: 15px;
    background: #0f172a; color: white;
    border: none; border-radius: 12px;
    font-size: 15px; font-weight: 600;
    cursor: pointer; margin-bottom: 10px;
  }}
  .btn-primary:hover {{ background: #1e293b; }}
  .btn-cancel {{
    width: 100%; padding: 8px;
    background: none; border: none;
    font-size: 13.5px; color: #94a3b8;
    cursor: pointer;
  }}
  .btn-cancel:hover {{ color: #64748b; }}
  /* Step 2 nav */
  .step2-nav {{
    display: flex; align-items: center;
    justify-content: space-between;
    margin-bottom: 24px;
  }}
  .back-btn {{
    background: none; border: none;
    font-size: 13.5px; color: #64748b;
    cursor: pointer; display: flex; align-items: center; gap: 4px;
  }}
  .back-btn:hover {{ color: #374151; }}
  /* Key icon */
  .key-icon-wrap {{
    width: 46px; height: 46px;
    background: #e0f2fe;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 14px;
  }}
  .key-icon-wrap svg {{ width: 22px; height: 22px; color: #0284c7; }}
  /* Form elements */
  .field-label {{
    font-size: 13.5px; font-weight: 600;
    color: #1e293b; display: block;
    margin-bottom: 7px;
  }}
  .key-input {{
    width: 100%; padding: 11px 13px;
    border: 1.5px solid #e2e8f0;
    border-radius: 10px;
    font-size: 14px; color: #0f172a;
    outline: none; transition: border-color 0.15s, box-shadow 0.15s;
  }}
  .key-input:focus {{
    border-color: #38bdf8;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.12);
  }}
  .help-link {{
    display: inline-flex; align-items: center; gap: 4px;
    color: #0ea5e9; font-size: 13px;
    text-decoration: none; margin: 8px 0 16px;
  }}
  .help-link:hover {{ text-decoration: underline; }}
  /* Save toggle card */
  .save-card {{
    border: 1.5px solid #e2e8f0;
    border-radius: 12px;
    padding: 13px 15px;
    margin-bottom: 6px;
  }}
  .save-row {{
    display: flex; align-items: center; gap: 10px;
  }}
  .save-icon {{ font-size: 16px; }}
  .save-label {{
    flex: 1;
    font-size: 14px; font-weight: 500; color: #1e293b;
  }}
  /* Toggle switch */
  .toggle {{ position: relative; width: 44px; height: 24px; flex-shrink: 0; }}
  .toggle input {{ opacity: 0; width: 0; height: 0; }}
  .slider {{
    position: absolute; inset: 0;
    background: #e2e8f0;
    border-radius: 24px; cursor: pointer;
    transition: background 0.18s;
  }}
  .slider::before {{
    content: '';
    position: absolute;
    width: 18px; height: 18px;
    left: 3px; bottom: 3px;
    background: white;
    border-radius: 50%;
    transition: transform 0.18s;
    box-shadow: 0 1px 3px rgba(0,0,0,0.18);
  }}
  input:checked + .slider {{ background: #38bdf8; }}
  input:checked + .slider::before {{ transform: translateX(20px); }}
  /* Duration pills */
  .duration-section {{ margin-top: 14px; }}
  .duration-label {{
    font-size: 12px; font-weight: 600;
    color: #64748b; margin-bottom: 8px;
    text-transform: uppercase; letter-spacing: 0.05em;
  }}
  .pills {{ display: flex; flex-wrap: wrap; gap: 7px; }}
  .pill {{
    padding: 6px 13px;
    border: 1.5px solid #e2e8f0;
    border-radius: 20px;
    font-size: 13px; color: #475569;
    cursor: pointer; background: white;
    transition: all 0.13s;
    user-select: none;
  }}
  .pill:hover {{ border-color: #94a3b8; }}
  .pill.sel {{
    border-color: #38bdf8;
    color: #0284c7;
    background: #e0f2fe;
  }}
  /* Security note */
  .sec-note {{
    background: #f8fafc;
    border-radius: 10px;
    padding: 11px 14px;
    display: flex; gap: 9px; align-items: flex-start;
    margin: 16px 0;
  }}
  .sec-icon {{ font-size: 13px; color: #94a3b8; margin-top: 1px; flex-shrink: 0; }}
  .sec-note p {{ font-size: 12.5px; color: #64748b; line-height: 1.5; }}
  /* Connect button */
  .btn-connect {{
    width: 100%; padding: 15px;
    border: none; border-radius: 12px;
    font-size: 15px; font-weight: 600;
    cursor: pointer;
    background: #bae6fd; color: #0369a1;
    transition: background 0.15s, color 0.15s;
  }}
  .btn-connect.ready {{
    background: #0ea5e9; color: white;
  }}
  .btn-connect.ready:hover {{ background: #0284c7; }}
  /* Step visibility */
  .step {{ display: none; }}
  .step.show {{ display: block; }}
</style>
</head>
<body>
<div class="modal">

  <!-- ── STEP 1: Connect ─────────────────────────────────────── -->
  <div id="s1" class="step show">
    <div class="dots">
      <div class="dot active"></div>
      <div class="dot"></div>
    </div>
    <button class="close-btn" type="button" onclick="doCancel()" title="Close">&times;</button>

    <div class="logos">
      <img src="/ui/assets/logos/litellm_logo.jpg" class="logo-img" alt="LiteLLM">
      <span class="logo-arrow">&#8594;</span>
      <div class="logo logo-s">{server_initial}</div>
    </div>

    <h2 class="step-title">Connect {server_name} MCP</h2>
    <p class="step-subtitle">LiteLLM needs access to {server_name} to complete your request.</p>

    <div class="info-box">
      <span class="info-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      </span>
      <div>
        <h4>How it works</h4>
        <p>LiteLLM acts as a secure bridge. Your requests are routed through our MCP client directly to {server_name}&rsquo;s API.</p>
      </div>
    </div>

    {access_section}

    <button class="btn-primary" type="button" onclick="goStep2()">
      Continue to Authentication &rarr;
    </button>
    <button class="btn-cancel" type="button" onclick="doCancel()">Cancel</button>
  </div>

  <!-- ── STEP 2: Provide API Key ──────────────────────────────── -->
  <div id="s2" class="step">
    <div class="step2-nav">
      <button class="back-btn" type="button" onclick="goStep1()">&#8592; Back</button>
      <div class="dots">
        <div class="dot active"></div>
        <div class="dot active"></div>
      </div>
      <button class="close-btn" style="position:static;" type="button" onclick="doCancel()" title="Close">&times;</button>
    </div>

    <div class="key-icon-wrap">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/></svg>
    </div>
    <h2 class="step-title" style="text-align:left;">Provide API Key</h2>
    <p class="step-subtitle" style="text-align:left;">Enter your {server_name} API key to authorize this connection.</p>

    <form method="POST" id="authForm" onsubmit="prepareSubmit()">
      <input type="hidden" name="client_id"            value="{client_id}">
      <input type="hidden" name="redirect_uri"          value="{redirect_uri}">
      <input type="hidden" name="code_challenge"        value="{code_challenge}">
      <input type="hidden" name="code_challenge_method" value="{code_challenge_method}">
      <input type="hidden" name="state"                 value="{state}">
      <input type="hidden" name="server_id"             value="{server_id}">
      <input type="hidden" name="duration" id="durInput" value="until_revoked">

      <label class="field-label">{server_name} API Key</label>
      <input
        type="password"
        name="api_key"
        id="apiKey"
        class="key-input"
        placeholder="Enter your API key"
        required
        autofocus
        oninput="syncBtn()"
      >

      {help_link_html}

      <div class="save-card">
        <div class="save-row">
          <span class="save-label">Save key for future use</span>
          <label class="toggle">
            <input type="checkbox" id="saveToggle" onchange="toggleDur()">
            <span class="slider"></span>
          </label>
        </div>
        <div id="durSection" class="duration-section" style="display:none;">
          <div class="duration-label">Duration</div>
          <div class="pills">
            <div class="pill" onclick="selDur('1h',this)">1 hour</div>
            <div class="pill sel" onclick="selDur('24h',this)">24 hours</div>
            <div class="pill" onclick="selDur('7d',this)">7 days</div>
            <div class="pill" onclick="selDur('30d',this)">30 days</div>
            <div class="pill" onclick="selDur('until_revoked',this)">Until I revoke</div>
          </div>
        </div>
      </div>

      <div class="sec-note">
        <span class="sec-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
        </span>
        <p>Your key is stored securely and transmitted over HTTPS. It is never shared with third parties.</p>
      </div>

      <button type="submit" class="btn-connect" id="connectBtn">
        Connect &amp; Authorize
      </button>
    </form>
  </div>

</div>
<script>
  function goStep2() {{
    document.getElementById('s1').classList.remove('show');
    document.getElementById('s2').classList.add('show');
  }}
  function goStep1() {{
    document.getElementById('s2').classList.remove('show');
    document.getElementById('s1').classList.add('show');
  }}
  function doCancel() {{
    if (window.opener) window.close();
    else window.history.back();
  }}
  function toggleDur() {{
    const on = document.getElementById('saveToggle').checked;
    document.getElementById('durSection').style.display = on ? 'block' : 'none';
  }}
  function selDur(val, el) {{
    document.querySelectorAll('.pill').forEach(p => p.classList.remove('sel'));
    el.classList.add('sel');
    document.getElementById('durInput').value = val;
  }}
  function syncBtn() {{
    const btn = document.getElementById('connectBtn');
    if (document.getElementById('apiKey').value.length > 0) {{
      btn.classList.add('ready');
    }} else {{
      btn.classList.remove('ready');
    }}
  }}
  function prepareSubmit() {{
    // nothing extra needed — duration is already in the hidden input
  }}
</script>
</body>
</html>"""

