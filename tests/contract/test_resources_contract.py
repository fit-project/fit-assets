from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
from PySide6.QtCore import QFile

import fit_assets.resources  # noqa: F401  # Registers Qt resources

pytestmark = pytest.mark.contract


def _exposed_resource_paths() -> list[str]:
    qrc_path = Path(__file__).resolve().parents[2] / "fit_assets" / "resources.qrc"
    tree = ET.parse(qrc_path)
    root = tree.getroot()

    exposed_paths: list[str] = []
    for qresource in root.findall("qresource"):
        prefix = (qresource.get("prefix") or "").rstrip("/")
        for file_node in qresource.findall("file"):
            resource_file = (file_node.text or "").strip()
            if not resource_file:
                continue
            exposed_paths.append(f":{prefix}/{resource_file}")

    return exposed_paths


def test_all_exposed_resources_are_readable() -> None:
    exposed_paths = _exposed_resource_paths()
    assert exposed_paths, "No exposed resources found in fit_assets/resources.qrc"

    missing_or_empty: list[str] = []
    for path in exposed_paths:
        qfile = QFile(path)
        if not qfile.exists() or qfile.size() <= 0:
            missing_or_empty.append(path)

    assert not missing_or_empty, (
        "Some exposed resources are missing or empty: "
        + ", ".join(missing_or_empty)
    )
