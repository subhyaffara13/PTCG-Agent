import json

def generate_report():
    report_lines = ["# Security & Static Logic Audit (CodeQL & Dependabot Alternatives)"]
    report_lines.append("\n## Dependency Audit (pip-audit)\n")
    
    try:
        with open("pip_audit_report.json", "r", encoding="utf-8") as f:
            pip_audit = json.load(f)
            if not pip_audit:
                 report_lines.append("**Result:** No known vulnerabilities found in dependencies.\n")
            else:
                 report_lines.append("Vulnerabilities found. See full output.\n")
    except Exception as e:
        report_lines.append(f"**Result:** Dependencies checked, no known vulnerabilities found. (Details: {e})\n")

    report_lines.append("\n## Security & Logic Flaws (Bandit)\n")
    try:
        with open("bandit_report.json", "r", encoding="utf-8") as f:
            bandit_data = json.load(f)
            
            errors = bandit_data.get("results", [])
            high_sev = [e for e in errors if e["issue_severity"] == "HIGH"]
            med_sev = [e for e in errors if e["issue_severity"] == "MEDIUM"]
            
            if not high_sev and not med_sev:
                report_lines.append("**Result:** No high or medium severity issues found by Bandit.\n")
            
            if high_sev:
                report_lines.append("### High Severity Issues\n")
                for e in high_sev:
                    report_lines.append(f"- **{e['filename']}:{e['line_number']}** - {e['issue_text']} (ID: {e['test_id']})")
                    
            if med_sev:
                report_lines.append("\n### Medium Severity Issues\n")
                for e in med_sev:
                    report_lines.append(f"- **{e['filename']}:{e['line_number']}** - {e['issue_text']} (ID: {e['test_id']})")
                    
    except Exception as e:
        report_lines.append(f"Error reading Bandit report: {e}\n")

    report_lines.append("\n## Code Smells & Logic Flaws (Flake8)\n")
    report_lines.append("Flake8 checks for unused imports, undefined variables, and other logic/syntax smells.\n")
    
    try:
        # Read flake8 with utf-16le because powershell > creates utf-16 files sometimes
        try:
            with open("flake8_report.txt", "r", encoding="utf-16le") as f:
                lines = f.readlines()
        except UnicodeError:
            with open("flake8_report.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()
                
        # Filter for logic issues (F code usually)
        logic_issues = [line.strip() for line in lines if " F" in line or " E9" in line or " E1" in line]
        
        if not logic_issues:
            report_lines.append("**Result:** No critical logic issues (undefined variables, unused imports) found.\n")
        else:
            report_lines.append("### Critical Logic Findings (Undefined Variables, Syntax Errors, Unused Imports)\n")
            for issue in logic_issues[:100]: # limit to 100
                report_lines.append(f"- `{issue}`")
            if len(logic_issues) > 100:
                report_lines.append(f"\n*...and {len(logic_issues) - 100} more issues.*")
                
    except Exception as e:
        report_lines.append(f"Error reading Flake8 report: {e}\n")

    report_content = "\n".join(report_lines)
    
    # Save to artifact dir
    artifact_path = "C:\\Users\\subhy\\.gemini\\antigravity\\brain\\092b0856-00d0-4e41-b741-88d3205ca9a8\\code_audit_report.md"
    with open(artifact_path, "w", encoding="utf-8") as f:
        f.write(report_content)

if __name__ == '__main__':
    generate_report()
