from pathlib import Path
import semsearch

# Project Directories
PACKAGE_ROOT = Path(semsearch.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
DATASET_DIR = Path(PACKAGE_ROOT / "datasets")

print(PACKAGE_ROOT,ROOT)