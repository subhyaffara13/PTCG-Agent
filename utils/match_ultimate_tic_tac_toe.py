
def match_ultimate_tic_tac_toe(raw: str, legal_action_strings: Sequence[str]) -> str | None:
    """Game-specific matcher for Ultimate Tic-Tac-Toe actions."""
    if not legal_action_strings:
        return None

    raw = raw.strip().lower()

    # 1. Exact case-insensitive match check
    for legal in legal_action_strings:
        if raw == legal.lower():
            return legal

    # 2. Check if we are in choose_subgrid phase
    # Legal actions: "Choose local board <idx>"
    if legal_action_strings[0].lower().startswith("choose local board"):
        # Match single digit or "subgrid/board <digit>" (take the last occurrence)
        matches = list(re.finditer(r"\b([0-8])\b", raw))
        if matches:
            subgrid = matches[-1].group(1)
            target = f"choose local board {subgrid}"
            for legal in legal_action_strings:
                if legal.lower() == target:
                    return legal
        return None

    # 3. Check if we are in choose_cell phase
    # Legal actions: "Local board <subgrid>: <symbol>(<row>,<col>)"
    if legal_action_strings[0].lower().startswith("local board"):
        first_legal = legal_action_strings[0]
        m = re.match(r"^local board (\d):\s*([xo])\(", first_legal, re.IGNORECASE)
        if not m:
            return None
        subgrid, symbol = m.group(1), m.group(2).lower()

        # Parse row,col coordinates (take the last occurrence)
        m_coords = None
        matches_coords = list(re.finditer(r"\b([0-2])\s*[,.\s-]\s*([0-2])\b", raw))
        if not matches_coords:
            matches_coords = list(re.finditer(r"\(([0-2])\s*,\s*([0-2])\)", raw))
        if matches_coords:
            m_coords = matches_coords[-1]

        if m_coords:
            r, c = m_coords.group(1), m_coords.group(2)
            target = f"local board {subgrid}: {symbol}({r},{c})"
            for legal in legal_action_strings:
                if legal.lower() == target.lower():
                    return legal

        # Parse single cell index (0-8)
        m_cell = re.match(r"^([0-8])$", raw)
        if m_cell:
            cell_idx = int(m_cell.group(1))
            r, c = cell_idx // 3, cell_idx % 3
            target = f"local board {subgrid}: {symbol}({r},{c})"
            for legal in legal_action_strings:
                if legal.lower() == target.lower():
                    return legal

        # Fallback: search for row,col anywhere in the string (take the last occurrence)
        matches_fallback = list(re.finditer(r"([0-2])\s*,\s*([0-2])", raw))
        if matches_fallback:
            m_coords_fallback = matches_fallback[-1]
            r, c = m_coords_fallback.group(1), m_coords_fallback.group(2)
            target = f"local board {subgrid}: {symbol}({r},{c})"
            for legal in legal_action_strings:
                if legal.lower() == target.lower():
                    return legal

    return None

