import os, glob, re

# forward_model_gen fixes
fmg_dir = r'C:\Users\subhy\.gemini\antigravity\scratch\ptcg-agent\cb_agents\forward_model_gen'
for pyfile in glob.glob(os.path.join(fmg_dir, '*.py')):
    with open(pyfile, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'from . import' in content:
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if line.startswith('from . import'):
                imports = [x.strip() for x in line.replace('from . import', '').split(',')]
                for imp in imports:
                    if imp == 'CardRegistry': new_lines.append('try:\n    from cb_agents.card_registry import CardRegistry\nexcept ImportError:\n    CardRegistry = None')
                    elif imp == '_get_prize_yield': new_lines.append('from cb_agents.card_utils import _get_prize_yield')
                    elif imp == '_legal_actions_cache': new_lines.append('from cb_agents.forward_model_gen._cache_legal_helpers import _legal_actions_cache')
                    elif imp == 'logger': new_lines.append('import logging\nlogger = logging.getLogger(__name__)')
                    elif imp == 'Path': new_lines.append('from pathlib import Path')
                    elif imp == 'json': new_lines.append('import json')
                    elif imp == 'lru_cache': new_lines.append('from functools import lru_cache')
                    elif imp == 'Any': new_lines.append('from typing import Any')
            else:
                new_lines.append(line)
        with open(pyfile, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))

# turn_planner_sort fixes
tps_dir = r'C:\Users\subhy\.gemini\antigravity\scratch\ptcg-agent\cb_agents\turn_planner_sort'

with open(os.path.join(tps_dir, '__init__.py'), 'r', encoding='utf-8') as f:
    init_content = f.read()

# We need to extract _PRIORITY_RULES and _EARLY_BENCH_ORDER from __init__.py and move to _sort_constants.py
with open(os.path.join(tps_dir, '_sort_constants.py'), 'w', encoding='utf-8') as f:
    f.write('''import json
from pathlib import Path
_PRIORITY_RULES = []
try:
    for _pr_path in [Path("skills/priority_rules.json"), Path(__file__).resolve().parent.parent / "skills" / "priority_rules.json"]:
        if _pr_path.exists():
            _pr_data = json.loads(_pr_path.read_text(encoding="utf-8"))
            _PRIORITY_RULES = _pr_data.get("rules", [])
            break
except Exception:
    pass
_EARLY_BENCH_ORDER = ["play_trainer:", "ability:", "bench:", "retreat:", "attack:", "evolve:", "attach_energy:", "pass"]
''')

# Remove them from __init__.py
init_content = re.sub(r'_PRIORITY_RULES = \[\]\ntry:.*?except Exception:\n    pass\n', '', init_content, flags=re.DOTALL)
init_content = re.sub(r'_EARLY_BENCH_ORDER = \[.*?\]\n', '', init_content)
init_content = init_content.replace('from cb_agents.constants import SCALING_ATTACKERS', 'from cb_agents.constants import SCALING_ATTACKERS\nfrom ._sort_constants import _PRIORITY_RULES, _EARLY_BENCH_ORDER')
with open(os.path.join(tps_dir, '__init__.py'), 'w', encoding='utf-8') as f:
    f.write(init_content)

for pyfile in glob.glob(os.path.join(tps_dir, '*.py')):
    if os.path.basename(pyfile) == '_sort_constants.py': continue
    with open(pyfile, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'from . import' in content:
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if 'from . import' in line:
                imports = [x.strip() for x in line.replace('from . import', '').strip().split(',')]
                for imp in imports:
                    if imp == '_registry': new_lines.append('from cb_agents.turn_planner_heuristics import _registry')
                    elif imp == '_PRIORITY_RULES': new_lines.append('from cb_agents.turn_planner_sort._sort_constants import _PRIORITY_RULES')
                    elif imp == '_EARLY_BENCH_ORDER': new_lines.append('from cb_agents.turn_planner_sort._sort_constants import _EARLY_BENCH_ORDER')
                    elif imp == '_dead_weight_heuristic': new_lines.append('from cb_agents.heuristic_pipeline import _dead_weight_heuristic')
                    elif imp == 'List': new_lines.append('from typing import List')
                    elif imp == 'logger': new_lines.append('import logging\nlogger = logging.getLogger(__name__)')
            else:
                new_lines.append(line)
        with open(pyfile, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
