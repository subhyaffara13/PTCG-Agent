import sys
from pathlib import Path

# Verify Python 3.11 compatibility before running local match
def verify_compatibility(file_path: Path):
    if file_path.exists():
        import ast
        content = file_path.read_text(encoding="utf-8")
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            print(f"CRITICAL: SyntaxError in {file_path.name}: {e}")
            sys.exit(1)
        for node in ast.walk(tree):
            if isinstance(node, ast.JoinedStr):
                for val in node.values:
                    if isinstance(val, ast.FormattedValue):
                        expr_str = ast.unparse(val.value)
                        if "'" in expr_str or '"' in expr_str:
                            print(f"CRITICAL: Python 3.11 compatibility error in {file_path.name}: f-string expression contains quotes: {{{expr_str}}}")
                            sys.exit(1)

verify_compatibility(Path("submission.py"))

from kaggle_environments import make
from submission import agent

env = make("cabt", debug=True)
env.run([agent, agent])
print("Step 0 error:", env.steps[0][0].get('error', 'None'))
print("Game steps count:", len(env.steps))
print("Game finished. Status P1:", env.state[0].status, "Status P2:", env.state[1].status)
if env.state[0].status == "ERROR":
    print("P1 error detail:", env.steps[-1][0].get('error'))
if env.state[1].status == "ERROR":
    print("P2 error detail:", env.steps[-1][1].get('error'))
