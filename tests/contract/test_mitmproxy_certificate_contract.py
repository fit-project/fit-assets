from __future__ import annotations

import ssl
from pathlib import Path


CERT_PATH = Path(__file__).resolve().parents[2] / "fit_assets" / "mitmproxy" / "mitmproxy-ca-cert.pem"


def _common_name(decoded_cert: dict) -> str | None:
    for rdn in decoded_cert.get("subject", ()):  # tuple of RDN tuples
        for attribute_name, attribute_value in rdn:
            if attribute_name == "commonName":
                return attribute_value
    return None


def test_mitmproxy_ca_certificate_contract() -> None:
    assert CERT_PATH.exists(), f"Certificate not found: {CERT_PATH}"
    assert CERT_PATH.stat().st_size > 0, f"Certificate is empty: {CERT_PATH}"

    cert_text = CERT_PATH.read_text(encoding="ascii")
    assert cert_text.startswith("-----BEGIN CERTIFICATE-----")
    assert cert_text.strip().endswith("-----END CERTIFICATE-----")

    decoded_cert = ssl._ssl._test_decode_cert(str(CERT_PATH))

    assert _common_name(decoded_cert) == "mitmproxy"
    assert decoded_cert.get("notBefore")
    assert decoded_cert.get("notAfter")
