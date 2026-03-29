"""Prestartup Script (Clean version)."""
import logging
import shutil
from pathlib import Path

# Try to import optional helper packages
try:
    from comfy_3d_viewers import copy_viewer
except ImportError:
    copy_viewer = None

log = logging.getLogger("depthanythingv3")

def copy_assets():
    SCRIPT_DIR = Path(__file__).resolve().parent
    # ComfyUI directory is usually two levels up from custom_nodes/folder/
    COMFYUI_DIR = SCRIPT_DIR.parent.parent
    
    # 1. Copy pointcloud VTK viewer from comfy-3d-viewers
    if copy_viewer:
        try:
            copy_viewer("pointcloud_vtk", SCRIPT_DIR / "web")
        except Exception as e:
            log.warning(f"Failed to copy viewer: {e}")

    # 2. Copy dynamic widgets JS
    try:
        from comfy_dynamic_widgets import get_js_path
        src = Path(get_js_path())
        if src.exists():
            dst = SCRIPT_DIR / "web" / "js" / "dynamic_widgets.js"
            dst.parent.mkdir(parents=True, exist_ok=True)
            if not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime:
                shutil.copy2(src, dst)
                log.info(f"Copied dynamic widgets from {src} to {dst}")
    except (ImportError, Exception):
        pass

    # 3. Copy assets to ComfyUI input directory
    src = SCRIPT_DIR / "assets"
    dst = COMFYUI_DIR / "input"
    
    if src.exists():
        dst.mkdir(parents=True, exist_ok=True)
        copied_count = 0
        for item in src.rglob("*"):
            if item.is_file():
                rel_path = item.relative_to(src)
                target = dst / rel_path
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target)
                copied_count += 1
        if copied_count > 0:
            log.info(f"Copied {copied_count} asset(s) from {src} to {dst}")

if __name__ == "__main__":
    copy_assets()
