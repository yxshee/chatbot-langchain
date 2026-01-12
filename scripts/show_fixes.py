#!/usr/bin/env python3
"""Deprecated helper.

This script used to print a static list of "fixes" that quickly got stale.
Use these instead:

- Verify everything works: python scripts/quick_start.py
- Run diagnostics:         python scripts/check.py
- Full tests:              python -m pytest
"""


def main() -> int:
    print("Use the current verification commands instead:")
    print("  • python scripts/quick_start.py")
    print("  • python scripts/check.py")
    print("  • python -m pytest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
