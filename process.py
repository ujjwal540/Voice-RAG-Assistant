#!/usr/bin/env python3
"""Simple CLI wrapper to run a single prompt through the RAG engine.

Usage examples:
  python process.py sample-local-pdf.pdf -p 'tell me about country nepal'
  python process.py -p 'summarize in one line'
"""
import argparse
import sys

from rag_engine import RAGEngine


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]

    parser = argparse.ArgumentParser(description="Run a one-off prompt through the RAG engine")
    parser.add_argument("file", nargs="?", help="(optional) path to a document — currently unused")
    parser.add_argument("-p", "--prompt", required=True, help="Prompt to send to the RAG engine")
    args = parser.parse_args(argv)

    engine = RAGEngine(source_path=args.file)

    try:
        answer = engine.chat(args.prompt, history=[])
    except Exception as exc:
        print("Error running RAG engine:", exc)
        return 2

    print(answer)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
