import glob
import os

for f in glob.glob('submission/cb_agents/*.py'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Fix the literal \n injected by powershell
    content = content.replace('"""\\nfrom __future__ import annotations\\n\\n', '"""\nfrom __future__ import annotations\n\n')
    
    # Fix imports
    content = content.replace('from agents.', 'from cb_agents.')
    content = content.replace('from bc_agents.', 'from cb_agents.')
    content = content.replace('import agents.', 'import cb_agents.')
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
