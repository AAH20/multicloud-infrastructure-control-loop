import argparse
import json
from pathlib import Path

from .engine import compile_proposal, verify
from .render import write_bundle


def load(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile and verify multi-cloud remediation proposals")
    commands = parser.add_subparsers(dest="command", required=True)
    compile_cmd = commands.add_parser("compile")
    compile_cmd.add_argument("--input", required=True); compile_cmd.add_argument("--rules", required=True); compile_cmd.add_argument("--output", required=True)
    verify_cmd = commands.add_parser("verify")
    verify_cmd.add_argument("--proposal", required=True); verify_cmd.add_argument("--post-change", required=True); verify_cmd.add_argument("--output", required=True)
    args = parser.parse_args()
    if args.command == "compile":
        write_bundle(Path(args.output), compile_proposal(load(args.input), load(args.rules)))
        return 0
    receipt = verify(load(args.proposal), load(args.post_change))
    target = Path(args.output); target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if receipt["verified"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
