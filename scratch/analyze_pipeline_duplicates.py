import os
from pathlib import Path

def main():
    print("==================================================")
    print("CODEBASE LOGIC & FILE DUPLICATION ANALYSIS")
    print("==================================================")
    
    # 1. Compare orchestration agent scripts
    scratch_agent = Path("scratch/orchestration_agent.py")
    factory_agent = Path("factory/orchestration_agent.py")
    
    print("\n[1] Orchestration Agent Comparison:")
    if scratch_agent.exists() and factory_agent.exists():
        s_size = scratch_agent.stat().st_size
        f_size = factory_agent.stat().st_size
        print(f"  - scratch/orchestration_agent.py: {s_size} bytes")
        print(f"  - factory/orchestration_agent.py: {f_size} bytes")
        if s_size != f_size:
            print("  - NOTICE: File sizes differ. factory/ version appears to be the newer, more sophisticated agent.")
        else:
            print("  - Files are identical in size.")
    else:
        print("  - Error: One of the orchestration scripts is missing.")

    # 2. Compare submission/auto-submit helper logics
    scratch_submit = Path("scratch/orchestration_auto_submit.py")
    factory_submit = Path("factory/orchestration_agent_helpers.py")
    
    print("\n[2] Auto-Submission Helpers Comparison:")
    if scratch_submit.exists() and factory_submit.exists():
        s_size = scratch_submit.stat().st_size
        f_size = factory_submit.stat().st_size
        print(f"  - scratch/orchestration_auto_submit.py: {s_size} bytes")
        print(f"  - factory/orchestration_agent_helpers.py: {f_size} bytes")
        
        # Analyze parameters in scratch
        s_content = scratch_submit.read_text(encoding="utf-8")
        f_content = factory_submit.read_text(encoding="utf-8")
        
        print("\n  Spacing & Breakthrough parameters:")
        print("  * scratch/orchestration_auto_submit.py:")
        for line in s_content.splitlines():
            if "elapsed_hours" in line or "Breakthrough" in line:
                if any(x in line for x in ("5.5", "should_submit", "elapsed")):
                    print(f"    {line.strip()}")
                    
        print("  * factory/orchestration_agent_helpers.py:")
        for line in f_content.splitlines():
            if "elapsed_hours" in line or "Breakthrough" in line:
                if any(x in line for x in ("1.0", "4.0", "should_submit", "elapsed")):
                    print(f"    {line.strip()}")
    else:
        print("  - Error: One of the auto-submit helper scripts is missing.")

    # 3. Check for failed submission spacing bugs
    print("\n[3] Spacing Logic Bug Checks (Failed Submissions):")
    for name, p in [("scratch", scratch_submit), ("factory", factory_submit)]:
        if p.exists():
            content = p.read_text(encoding="utf-8")
            if "status" in content or "SubmissionStatus" in content or "ERROR" in content:
                print(f"  - {name}: Spacing check filters by submission status: YES")
            else:
                print(f"  - {name}: Spacing check filters by submission status: NO (BUG: includes failed/error submissions in spacing check)")
                
    print("\n==================================================")

if __name__ == "__main__":
    main()
