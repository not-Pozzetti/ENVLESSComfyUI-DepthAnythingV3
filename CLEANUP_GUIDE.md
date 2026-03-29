# ComfyUI Node Cleanup Guide: Removing comfy-env and comfy-test

This guide provides instructions for an AI or developer to remove `comfy-env` and `comfy-test` dependencies from a ComfyUI custom node repository.

## 1. Dependency Cleanup

### requirements.txt

- **Action**: Search for and remove the `comfy-env` line.
- **Example**: Remove `comfy-env==0.2.10`.
- **Important Note**: Do NOT remove other `comfy-*` helper packages such as `comfy-3d-viewers` or `comfy-dynamic-widgets` unless they are explicitly listed here.

## 2. Configuration File Deletion

Delete the following files if they exist in the root directory:

- `comfy-env-root.toml`
- `comfy-test.toml`
- `comfy-env.toml` (Delete ALL instances of this throughout the entire repository)

## 3. GitHub Workflows

Delete the entire `.github` directory.

- **Reason**: These repositories often contain workflows and settings that rely on the original author's infrastructure (like `comfy-test`).

## 4. Execution Scripts Cleanup

### install.py

- **Action**: Delete `install.py` if its only purpose was calling `comfy_env.install()`.

### prestartup_script.py

- **Action**: Rewrite to use the Python standard library (`shutil`, `pathlib`) for asset copying, removing the `comfy_env` dependency.
- **Clean Code Pattern**:

```python
"""Prestartup Script (Clean version)."""
import shutil
from pathlib import Path

def copy_assets():
    SCRIPT_DIR = Path(__file__).resolve().parent
    # Adjust COMFYUI_DIR as needed; usually two levels up from custom_nodes/folder/
    COMFYUI_DIR = SCRIPT_DIR.parent.parent
    
    src = SCRIPT_DIR / "assets"
    dst = COMFYUI_DIR / "input"
    
    if src.exists():
        dst.mkdir(parents=True, exist_ok=True)
        for item in src.iterdir():
            if item.is_file():
                shutil.copy2(item, dst / item.name)
            elif item.is_dir():
                shutil.copytree(item, dst / item.name, dirs_exist_ok=True)
        print(f"Copied assets from {src} to {dst}")

if __name__ == "__main__":
    copy_assets()
```

### **init**.py (Node Registration)

- **Action**: Replace `comfy_env.register_nodes()` with manual aggregation of node mappings.
- **Clean Code Pattern**:

```python
"""Node registration (Clean version)."""
# Import mappings from sub-packages in the nodes directory
from .nodes.main import NODE_CLASS_MAPPINGS as MAIN_CLASS, NODE_DISPLAY_NAME_MAPPINGS as MAIN_DISPLAY
# Add other sub-packages as needed (e.g., blender, gpu)

NODE_CLASS_MAPPINGS = {**MAIN_CLASS}
NODE_DISPLAY_NAME_MAPPINGS = {**MAIN_DISPLAY}

WEB_DIRECTORY = "./web"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
```

## 5. File System and Git Cleanup

### .gitignore

- **Action**: Remove any entries relating to `comfy-env` or `comfy-test`, and add standard ignores.
- **Entries to remove**:
  - `.comfy-test-logs/`
  - `_root_env`

## 6. Rebranding and Removing Pozzetti References

Replace all mentions of the original author and their GitHub organization to reflect the new "not-pozzetti" repository.

### Global Replacements

Execute the following sort of replacements across the entire repository (except this file!):

1. `https://github.com/pozzettiandrea` -> `https://github.com/not-pozzetti/ENVLESS`
2. `https://pozzettiandrea.github.io/` -> `https://not-pozzetti.github.io/ENVLESS`
3. `Andrea Pozzetti` -> `NOTPozzetti`
4. `PozzettiAndrea/ComfyUI` -> `not-pozzetti/ENVLESSComfyUI`
5. `ComfyUI-<reponame>` -> `ENVLESSComfyUI-<reponame>`

### README.md Note

Add the following warning to the top of the `README.md` file:

```markdown
> [!IMPORTANT]
> These were forks to avoid the abusive ComfyENV code that was added by Mr Pozzetti to thousands of unsuspecting users.
```

## 7. Turbo Execution (Optimized for AI)

To avoid hitting token limits during global rebranding, use these one-liner shell commands. These are safe and efficient for repositories of any size.

### Global File Deletion

```bash
# Delete all comfy-env and comfy-test files and directories
rm -rf .github .comfy-test-logs/ _root_env
rm -f comfy-env-root.toml comfy-test.toml
find . -name "comfy-env.toml" -type f -delete
```

### Global Rebranding (Perl One-Liners)

Use `perl` for consistent in-place editing across macOS and Linux:

```bash
# 1. Update GitHub Organization and Repository URLs
# Note: -not -name "CLEANUP_GUIDE.md" prevents the guide from editing itself!
find . -type f -not -path '*/.*' -not -name "CLEANUP_GUIDE.md" -exec perl -i -pe 's|https://github.com/pozzettiandrea|https://github.com/not-pozzetti/ENVLESS|g' {} +
find . -type f -not -path '*/.*' -not -name "CLEANUP_GUIDE.md" -exec perl -i -pe 's|https://pozzettiandrea.github.io/|https://not-pozzetti.github.io/ENVLESS/|g' {} +
find . -type f -not -path '*/.*' -not -name "CLEANUP_GUIDE.md" -exec perl -i -pe 's|PozzettiAndrea/ComfyUI|not-pozzetti/ENVLESSComfyUI|g' {} +

# 2. Update Author Name
find . -type f -not -path '*/.*' -not -name "CLEANUP_GUIDE.md" -exec perl -i -pe 's|Andrea Pozzetti|NOTPozzetti|g' {} +

# 3. Update Repository Name Prefix (example for ComfyUI-Sharp)
# REPLACE <reponame> with the actual repository suffix (e.g. Sharp, GeometryPack)
# The (?<!ENVLESS) lookbehind prevents double-prefixing if already partially rebranded.
find . -type f -not -path '*/.*' -not -name "CLEANUP_GUIDE.md" -exec perl -i -pe 's|(?<!ENVLESS)ComfyUI-Sharp|ENVLESSComfyUI-Sharp|g' {} +
```

## 8. Verification Checklist

- [ ] `comfy-env` and `comfy-test` are removed from `requirements.txt`.
- [ ] All `comfy-env.toml` and  `comfy-test.toml` configuration files are deleted (including all instances of `comfy-env.toml` deeper in the repo).
- [ ] The entire `.github` directory is deleted.
- [ ] `prestartup_script.py` is modernized.
- [ ] `.comfy-test-logs/` and `_root_env` are removed from `.gitignore`.
- [ ] `README.md` contains the mandatory fork note.

