import os

def main():
    path = r"C:\Users\subhy\.gemini\antigravity\brain\47b3789d-c734-4a98-8b74-7c7f00217243\.system_generated\tasks\task-4378.log"
    if os.path.exists(path):
        print("Log file content:")
        print(open(path, "r", encoding="utf-8", errors="ignore").read())
    else:
        print("Log file not found at:", path)
        # Search the tasks folder for other logs
        tasks_dir = os.path.dirname(path)
        if os.path.exists(tasks_dir):
            print("Files in tasks directory:")
            for f in os.listdir(tasks_dir):
                print("  -", f)

if __name__ == "__main__":
    main()
