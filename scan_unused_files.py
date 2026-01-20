import os
import re

# ===== CONFIG =====
PROJECT_DIR = "."  # path to your Django project root
TEMPLATE_DIRS = ["templates"]
STATIC_DIRS = ["static"]
PYTHON_EXT = ".py"

# ===== HELPER FUNCTIONS =====
def find_files(dirs, extensions):
    """Find all files with given extensions in dirs."""
    files = []
    for d in dirs:
        for root, _, filenames in os.walk(os.path.join(PROJECT_DIR, d)):
            for f in filenames:
                if any(f.endswith(ext) for ext in extensions):
                    files.append(os.path.join(root, f))
    return files

def search_references(file_path, search_paths):
    """Check if file name (without extension) is referenced in search paths."""
    name = os.path.splitext(os.path.basename(file_path))[0]
    pattern = re.compile(r"\b" + re.escape(name) + r"\b")
    for path in search_paths:
        for root, _, files in os.walk(path):
            for f in files:
                if f.endswith(PYTHON_EXT) or f.endswith(".html") or f.endswith(".js") or f.endswith(".css"):
                    full_path = os.path.join(root, f)
                    try:
                        with open(full_path, "r", encoding="utf-8") as file_content:
                            if pattern.search(file_content.read()):
                                return True
                    except:
                        pass
    return False

# ===== MAIN LOGIC =====
print("\n==== TEMPLATE FILES ====")
template_files = find_files(TEMPLATE_DIRS, [".html"])
for tpl in template_files:
    if not search_references(tpl, [PROJECT_DIR]):
        print(f"Possibly unused template: {tpl}")

print("\n==== STATIC FILES ====")
static_files = find_files(STATIC_DIRS, [".css", ".js", ".png", ".jpg", ".svg"])
for sf in static_files:
    if not search_references(sf, [PROJECT_DIR]):
        print(f"Possibly unused static file: {sf}")

print("\n==== PYTHON FILES ====")
python_files = find_files(["."], [PYTHON_EXT])
for pf in python_files:
    # skip manage.py and settings.py
    if pf.endswith(("manage.py", "settings.py")):
        continue
    if not search_references(pf, [PROJECT_DIR]):
        print(f"Possibly unused python file: {pf}")

print("\nScan complete! ⚠️ Review before deleting any files.")
