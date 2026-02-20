from __future__ import annotations

import re
from pathlib import Path

import pytest


TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "fit_assets" / "templates"

EXPECTED_TEMPLATES = {
    "content.html": {
        "vars": {
            "application_short_name",
            "column",
            "document_title",
            "index",
            "logo",
            "loop.index",
            "note",
            "of",
            "page",
            "row.desc",
            "row.value",
            "section.content",
            "section.contents.chain_of_custody",
            "section.contents.hashes",
            "section.description",
            "section.note",
            "section.subtitles.chain_of_custody",
            "section.subtitles.hashes",
            "section.title",
            "section.type",
            "section.verification_result",
        },
        "stmts": {
            'elif section.type == "digital_forensics"',
            'elif section.type == "integrity_verification"',
            'elif section.type == "screenshot"',
            'elif section.type == "verification_report"',
            'elif section.type == "video"',
            'elif section.type == "wacz_description"',
            'elif section.type == "whois"',
            'elif section.type in ["case_info", "system_artifacts", "acquired_content"]',
            "endfor",
            "endif",
            "for column in section.columns",
            "for row in section.rows",
            "for section in sections",
            "if not loop.last",
            "if section.description",
            "if section.note",
            'if section.type == "fit_description"',
            "if section.verification_result",
        },
    },
    "front.html": {
        "vars": {
            "application_short_name",
            "document_subtitle",
            "document_title",
            "img",
            "version",
        },
        "stmts": set(),
    },
}


def _extract_template_tokens(content: str, pattern: str) -> set[str]:
    tokens = {re.sub(r"\s+", " ", match.strip()) for match in re.findall(pattern, content, re.S)}
    return tokens


@pytest.mark.parametrize("template_name, expected", EXPECTED_TEMPLATES.items())
def test_templates_contract(template_name: str, expected: dict[str, set[str]]) -> None:
    template_path = TEMPLATES_DIR / template_name

    assert template_path.exists(), f"Missing template: {template_path}"
    assert template_path.stat().st_size > 0, f"Template is empty: {template_path}"

    content = template_path.read_text(encoding="utf-8")

    assert "<!DOCTYPE html>" in content
    assert "<html" in content
    assert "</html>" in content

    actual_vars = _extract_template_tokens(content, r"\{\{\s*(.*?)\s*\}\}")
    actual_stmts = _extract_template_tokens(content, r"\{%\s*(.*?)\s*%\}")

    assert actual_vars == expected["vars"], (
        f"Template {template_name} has unexpected variable tokens. "
        f"Expected={sorted(expected['vars'])}, Actual={sorted(actual_vars)}"
    )
    assert actual_stmts == expected["stmts"], (
        f"Template {template_name} has unexpected statement tokens. "
        f"Expected={sorted(expected['stmts'])}, Actual={sorted(actual_stmts)}"
    )
