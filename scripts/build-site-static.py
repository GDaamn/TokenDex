"""Generate the static export used only by the original hosted Site."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent.parent
shutil.copytree(root / "static", root / "dist", dirs_exist_ok=True)
print("Static Site export prepared in dist/")
