"""Command line interface entry point."""

from __future__ import annotations

from .runner import main

__all__ = ["main"]

if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
