# fit-assets

Shared assets for the **FIT Project**: icons, fonts, QSS themes, images, and Qt resource files used across external modules (`fit-configuration`, `fit-cases`, `fit-instagram`, etc.).

---

## Purpose
- Provide a single source for **reusable assets** shared among FIT modules.
- Offer a clear structure for managing **Qt Resource Collections** (`.qrc` files), compiled either as **Python modules** (`*_rc.py`) or **binary bundles** (`.rcc`).

---

## Requirements
- **Python** >=3.11,<3.14
- **PySide6** ≥ 6.9.0 (for `pyside6-rcc`)  
- **Poetry** (recommended for development)

---

## Installation

### As dependency (recommended)
```bash
poetry add git+https://github.com/fit-project/fit-assets.git@main
# or using pip
pip install git+https://github.com/fit-project/fit-assets.git@main
```

### For local development
```bash
git clone https://github.com/fit-project/fit-assets.git
cd fit-assets
poetry install
```

---

## Local Testing

### What each tool does
- `pytest`: runs contract tests

### 1) Base setup
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install . pytest
```

### 2) Test suite
```bash
# contract tests
pytest -m contract -q tests
```

---

## 🔧 Compile Qt Resources with **PySide**

Compile the `.qrc` file into a Python module:
```bash
pyside6-rcc fit_assets/resources.qrc -o fit_assets/resources.py
```
Then, simply **import** it in your Python code before using `:/` paths:
```python
# Import the generated resources (side-effect: registers the RCC)
import fit_assets.resources

from PySide6.QtGui import QIcon
btn.setIcon(QIcon(':/icons/fit.svg'))
```
---
