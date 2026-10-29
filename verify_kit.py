#!/usr/bin/env python3
"""Verify the Free Paperwork Organizer Kit builds correctly.

Checks:
- all expected files exist
- each HTML file is well-formed HTML5
- each HTML file has title, h1, Asdale Dynamics, LLC credit, print CSS, US Letter page size, print hint
- README.md credits Asdale Dynamics, LLC, includes copyright line, references all organizers
- LICENSE contains the exact line "Copyright (c) 2026 Asdale Dynamics, LLC" under the MIT header
- no secrets, API keys, or personal data patterns in any kit file
- no .github/workflows directory
Run: python3 verify_kit.py
"""
import html.parser
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
ORGANIZERS = [
    "bill-tracker",
    "appointment-log",
    "form-filling-cheat-sheet",
    "document-checklist",
]
HTML_FILES = [name + ".html" for name in ORGANIZERS]
MD_FILES = [name + ".md" for name in ORGANIZERS]
REQUIRED_FILES = HTML_FILES + MD_FILES + ["README.md", "LICENSE", "index.html"]


class HTMLChecker(html.parser.HTMLParser):
    """Small well-formedness checker. Void elements are self-closing by design."""
    def __init__(self):
        super().__init__()
        self.errors = []
        self.stack = []
        self.void = {
            "area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "param", "source", "track", "wbr",
        }

    def handle_starttag(self, tag, attrs):
        if tag not in self.void:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.void:
            return
        if not self.stack:
            self.errors.append(f"unexpected closing tag </{tag}>")
            return
        if self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.errors.append(f"mismatched close </{tag}> (expected </{self.stack[-1]}>)")

    def check(self, source):
        self.stack = []
        self.errors = []
        try:
            self.feed(source)
        except Exception as exc:  # noqa: BLE001
            self.errors.append(f"parse error: {exc}")
        for tag in reversed(self.stack):
            self.errors.append(f"unclosed tag <{tag}>")
        return not self.errors


def has_secrets_or_personal_data(text):
    patterns = [
        r"sk-[A-Za-z0-9]{20,}",
        r"(?i)api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9]{8,}",
        r"(?i)secret\s*[:=]\s*['\"]?[A-Za-z0-9]{8,}",
        r"(?i)password\s*[:=]\s*['\"]?[A-Za-z0-9]{6,}",
        r"-----BEGIN [A-Z ]+PRIVATE KEY-----",
        r"(?i)access[_-]?token\s*[:=]\s*['\"]?[A-Za-z0-9]{10,}",
        r"\b\d{3}-\d{2}-\d{4}\b",  # full SSN pattern
        r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",  # full card number
    ]
    for pat in patterns:
        if re.search(pat, text):
            return True
    return False


failures = []

# 1. All expected files exist
for name in REQUIRED_FILES:
    path = os.path.join(ROOT, name)
    if not os.path.isfile(path):
        failures.append(f"missing file: {name}")

# 2. HTML well-formedness + structure
checker = HTMLChecker()
for name in HTML_FILES:
    path = os.path.join(ROOT, name)
    if not os.path.isfile(path):
        continue
    with open(path, encoding="utf-8") as fh:
        source = fh.read()
    if not checker.check(source):
        for err in checker.errors:
            failures.append(f"{name}: {err}")
    if re.search(r"<title[^>]*>.*?</title>", source, re.DOTALL) is None:
        failures.append(f"{name}: missing <title>")
    if re.search(r"<h1[^>]*>", source) is None:
        failures.append(f"{name}: missing <h1>")
    if "Asdale Dynamics, LLC" not in source:
        failures.append(f"{name}: missing Asdale Dynamics, LLC credit")
    if "Background graphics" not in source:
        failures.append(f"{name}: missing print hint")
    if "@page" not in source:
        failures.append(f"{name}: missing print page setup")
    if "Letter" not in source:
        failures.append(f"{name}: missing US Letter page size")
    # large-print friendly check: base font size at least 15px
    if re.search(r"font-size:\s*(1[6-9]|[2-9][0-9])px", source) is None:
        failures.append(f"{name}: missing large-print base font size (>=15px)")

# 3. README quality checks
readme_path = os.path.join(ROOT, "README.md")
if os.path.isfile(readme_path):
    with open(readme_path, encoding="utf-8") as fh:
        readme = fh.read()
    if "Asdale Dynamics, LLC" not in readme:
        failures.append("README.md missing Asdale Dynamics, LLC credit")
    if "Copyright (c) 2026 Asdale Dynamics, LLC" not in readme:
        failures.append("README.md missing copyright line")
    for name in ORGANIZERS:
        if name not in readme:
            failures.append(f"README.md missing reference to {name}")
else:
    failures.append("missing file: README.md")

# 4. LICENSE exact copyright line
license_path = os.path.join(ROOT, "LICENSE")
if os.path.isfile(license_path):
    with open(license_path, encoding="utf-8") as fh:
        license_lines = fh.read().splitlines()
    if "Copyright (c) 2026 Asdale Dynamics, LLC" not in license_lines:
        failures.append("LICENSE missing exact copyright line")
    if "MIT License" not in license_lines[0]:
        failures.append("LICENSE missing MIT header")
else:
    failures.append("missing file: LICENSE")

# 5. No secrets or personal data anywhere
for name in REQUIRED_FILES:
    path = os.path.join(ROOT, name)
    if not os.path.isfile(path):
        continue
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if has_secrets_or_personal_data(text):
        failures.append(f"{name}: possible secret or personal data detected")

# 6. No .github/workflows
wf = os.path.join(ROOT, ".github", "workflows")
if os.path.isdir(wf):
    failures.append(".github/workflows directory present (must not exist)")

# Report
if failures:
    print("VERIFY FAIL:")
    for fail in failures:
        print(f"  - {fail}")
    sys.exit(1)

print("VERIFY PASS:")
print(f"  - {len(HTML_FILES)} HTML organizers well-formed with credits and print setup")
print(f"  - {len(MD_FILES)} Markdown mirrors present")
print(f"  - index.html landing page present")
print("  - README.md credits Asdale Dynamics, LLC with copyright line")
print("  - LICENSE has exact MIT copyright line")
print("  - no secrets or personal data detected")
print("  - no .github/workflows directory")
sys.exit(0)
