"""Basic Honeypot Detector"""
import re


def check_threat(payload: str) -> bool:
    threats = [
        r"OR\s+1=1",     # SQLi
        r"<script>",     # XSS
        r"bin/sh",       # RCE
        r"nmap"         # Scanner
    ]
    return any(re.search(p, payload, re.I) for p in threats)
