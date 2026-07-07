import ast
import csv
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def check_syntax_and_inheritance(staged_path: Path, content: str, skills_dir: Path) -> tuple[bool, str]:
    if staged_path.suffix == ".csv":
        try:
            reader = csv.reader(content.strip().splitlines())
            header = next(reader, None)
            if header is None:
                return False, "CSV is empty — no header found"
            total_cards = 0
            card_counts = {}
            for row in reader:
                if not row or not any(cell.strip() for cell in row):
                    continue
                card_id = row[0].strip()
                card_name = row[1].strip()
                count = int(row[3])
                float(row[4])
                total_cards += count
                card_counts[card_id] = card_counts.get(card_id, 0) + count
            if total_cards != 60:
                return False, f"Deck must contain exactly 60 cards, found {total_cards}"

            # Rule of Four & Basic Pokemon check
            raw_csv_path = skills_dir / "card_pool_raw.csv"
            basic_pkmn_ids, basic_energy_ids = set(), set()
            card_name_by_id = {}
            if raw_csv_path.exists():
                try:
                    with open(raw_csv_path, mode="r", encoding="utf-8") as f:
                        raw_reader = csv.DictReader(f)
                        stage_col = next((col for col in raw_reader.fieldnames if "Stage" in col and "Type" in col), None) if raw_reader.fieldnames else None
                        for r_row in raw_reader:
                            cid = r_row.get("Card ID", "").strip()
                            if cid:
                                name = r_row.get("Card Name", "").strip()
                                card_name_by_id[cid] = name
                                stage_val = r_row.get(stage_col, "").strip() if stage_col else ""
                                if "Basic" in stage_val and "Pok" in stage_val:
                                    basic_pkmn_ids.add(cid)
                                if ("Energy" in r_row.get("Category", "") or "Energy" in stage_val) and "Basic" in name:
                                    basic_energy_ids.add(cid)
                except Exception as e:
                    logger.error(f"Validator failed to load card_pool_raw.csv for checks: {e}")

            has_basic_pkmn = False
            for cid, count in card_counts.items():
                name = str(card_name_by_id.get(cid, cid) or "")
                if cid in basic_pkmn_ids:
                    has_basic_pkmn = True
                is_basic_energy = (cid in basic_energy_ids) or ("Basic" in name and "Energy" in name)
                if not is_basic_energy and count > 4:
                    return False, f"Card '{name}' (ID: {cid}) exceeds Rule of Four limit (found {count} copies)"
            if not has_basic_pkmn:
                return False, "Deck must contain at least one Basic Pokémon"
            return True, ""
        except (ValueError, IndexError) as e:
            return False, f"CSV parsing error: {e}"

    # Python validation
    try:
        tree = ast.parse(content, filename=staged_path.name)
    except SyntaxError as e:
        return False, f"SyntaxError on line {e.lineno}: {e.msg}"

    # Verify Python 3.11 compatibility (PEP 701 nested-quote f-strings checker)
    for node in ast.walk(tree):
        if isinstance(node, ast.JoinedStr):
            for val in node.values:
                if isinstance(val, ast.FormattedValue):
                    expr_str = ast.unparse(val.value)
                    if "'" in expr_str or '"' in expr_str:
                        return False, f"PEP 701 f-string compatibility error: f-string expression contains quotes: {{{expr_str}}}"

    has_class = any(isinstance(node, ast.ClassDef) for node in ast.walk(tree))
    inherits_base = any(isinstance(base, ast.Name) and base.id == "BaseAgent" for node in ast.walk(tree) if isinstance(node, ast.ClassDef) for base in node.bases)
    if has_class and not inherits_base:
        return False, "Class definition found but does not inherit from BaseAgent"

    # Check receive method
    is_factory = any(x in staged_path.name for x in ["logger", "runner", "eval", "improvement", "builder", "validator"])
    has_receive = False
    receive_raises_nie = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "receive":
            has_receive = True
            for sub_node in ast.walk(node):
                if isinstance(sub_node, ast.Raise) and (
                   (isinstance(sub_node.exc, ast.Call) and isinstance(sub_node.exc.func, ast.Name) and sub_node.exc.func.id == "NotImplementedError") or
                   (isinstance(sub_node.exc, ast.Name) and sub_node.exc.id == "NotImplementedError")):
                    receive_raises_nie = True

    if is_factory:
        if not has_receive or not receive_raises_nie:
            return False, "Factory component receive() must raise NotImplementedError"
    elif not has_receive:
        return False, "Player agent receive() is missing or not implemented"

    return True, ""
