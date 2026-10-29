# STATUS

## What was built

Free Paperwork Organizer Kit — fillable paperwork organizers for accessible life-admin help. Printable, large-print friendly, no account needed, local-first (runs entirely in the browser; nothing is collected or sent anywhere).

Files:
- `index.html` — landing page linking to all four organizers with descriptions and how-to steps.
- `bill-tracker.html` / `bill-tracker.md` — monthly bill tracker: account, due date, amount, payment method, date paid, confirmation number, paid checkbox, totals row, notes.
- `appointment-log.html` / `appointment-log.md` — appointment log: date, time, provider/office, reason, phone, address, what to bring, confirmed checkbox, follow-up notes.
- `form-filling-cheat-sheet.html` / `form-filling-cheat-sheet.md` — personal info filled once (name, DOB, SSN last-4 only, address, phone, email, emergency contact, doctors, pharmacy, insurance IDs) plus common form fields and quick reminders.
- `document-checklist.html` / `document-checklist.md` — 24-item document checklist (ID, medical, financial, housing, legal, auto) with "Have it?", original location, and copy location columns.
- `README.md` — kit description, how to use, design notes, safety reminder, license, credit.
- `LICENSE` — MIT License, Copyright (c) 2026 Asdale Dynamics, LLC.
- `verify_kit.py` — committed verification script (run with `python3 verify_kit.py`).

Each HTML file is standalone with embedded CSS: US Letter, large-print base text (16–17 px), big 22 px checkboxes, shaded fillable fields, high contrast, print-optimized (@page Letter, background graphics preserved).

Credit: created and published by Asdale Dynamics, LLC (Dylan Asdale, founder; Indiana, formed October 2026). Education only — not medical or legal advice.

## How to run

1. Open `index.html` in a web browser (Chrome, Edge, Firefox, Safari), or open any organizer `.html` file directly. No account, no install, no internet needed.
2. Click into shaded fields and type, or print first and write by hand.
3. Print (Ctrl+P / Cmd+P), enable "Print background graphics" so headers render.
4. The `.md` files can be read or printed from any Markdown reader or text editor.
5. To verify: `python3 verify_kit.py`

## Verification results

Ran `python3 verify_kit.py` — VERIFY PASS:

- All 4 HTML organizers parse as well-formed HTML5 (title, h1, print page setup, US Letter, print hint, Asdale Dynamics, LLC credit, large-print base font >=15px in each).
- All 4 Markdown mirrors present.
- `index.html` landing page well-formed.
- `README.md` credits Asdale Dynamics, LLC, includes the copyright line, and references every organizer.
- `LICENSE` contains the exact line "Copyright (c) 2026 Asdale Dynamics, LLC" under the MIT header.
- No secrets, API keys, or personal data patterns detected in any kit file.
- No `.github/workflows` directory present.

Browser visual/print rendering was not executed (no browser in this environment); print CSS uses standard @page Letter rules and should be spot-checked by opening and printing in a browser before wide distribution.

## Known gaps

- Print rendering not machine-tested in an actual browser.
- No automated test runner beyond `verify_kit.py`; verification is a one-shot Python script.
- Markdown versions are plain-text mirrors and are not fillable on screen (use the HTML versions for typing).
