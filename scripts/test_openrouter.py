#!/usr/bin/env python3
"""
Deprecated: OpenRouter support removed.

This repository is now intentionally simplified to use Google Gemini only,
to match the bundled FAISS index (768-dim embeddings).
"""



def main() -> int:
    print("This project no longer supports OpenRouter.")
    print("Use Google Gemini instead:")
    print("  - ensure GOOGLE_API_KEY is set in .env")
    print("  - run: python scripts/quick_start.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
