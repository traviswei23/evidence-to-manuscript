"""Reconcile selected manuscript sentences to CSV cells and freeze the inputs actually checked."""

import argparse
import csv
import hashlib
import json
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path


def local(root, name):
    if not isinstance(name, str) or not name.strip() or Path(name).is_absolute():
        raise ValueError(f"Expected a case-relative path: {name!r}")
    path = (root / name).resolve()
    if root not in path.parents or not path.is_file():
        raise ValueError(f"Missing input or path outside case: {name}")
    return path


def objects(ledger, field):
    entries = ledger[field]
    if not isinstance(entries, list) or not all(isinstance(row, dict) for row in entries):
        raise ValueError(f"{field} must be an array of objects")
    ids = [entry["id"] for entry in entries]
    if any(not isinstance(key, str) or not key for key in ids) or len(ids) != len(set(ids)):
        raise ValueError(f"Invalid or duplicate ID in {field}")
    return entries


def read_cell(path, claim):
    selector = claim["where"]
    if not isinstance(selector, dict) or not selector:
        raise ValueError(f"{claim['id']}: provide row-selection columns")
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames or []
        required = set(selector) | {claim["column"], claim["unit_column"]}
        if len(set(fields)) != len(fields) or not required <= set(fields):
            raise ValueError(f"{claim['id']}: CSV columns missing or repeated")
        matches = [row for row in reader if all(row[k] == v for k, v in selector.items())]
    if len(matches) != 1:
        raise ValueError(f"{claim['id']}: CSV selector matched {len(matches)} rows")
    unit = matches[0][claim["unit_column"]]
    if not unit or unit != claim["unit"]:
        raise ValueError(f"{claim['id']}: CSV and manuscript units differ")
    places = claim["places"]
    if type(places) is not int or not 0 <= places <= 15:
        raise ValueError("places must be between 0 and 15")
    value = Decimal(matches[0][claim["column"]])
    if not value.is_finite():
        raise ValueError(f"{claim['id']}: expected a finite number")
    return format(value, f".{places}f") + unit


def audit(ledger_path):
    root = ledger_path.parent
    ledger = json.loads(ledger_path.read_text(encoding="utf-8-sig"))
    draft_path = local(root, ledger["draft"])
    draft = draft_path.read_text(encoding="utf-8-sig")
    if not draft.strip():
        raise ValueError("Manuscript is empty")
    inputs = {ledger_path, draft_path}
    issues = []
    for path in ledger.get("supporting_files", []):
        inputs.add(local(root, path))
    quantities = objects(ledger, "quantities")
    if not (quantities or ledger.get("figures") or ledger.get("citations")):
        raise ValueError("No checks declared")
    for claim in quantities:
        path = local(root, claim["csv"])
        inputs.add(path)
        printed = read_cell(path, claim)
        contexts = claim["contexts"]
        if not isinstance(contexts, list) or not contexts or len(contexts) != len(set(contexts)):
            raise ValueError(f"{claim['id']}: provide distinct sentence contexts")
        for template in contexts:
            if template.count("{value}") != 1 or not template.replace("{value}", "").strip():
                raise ValueError(f"{claim['id']}: surround the single value marker with actual text")
            expected = template.replace("{value}", printed)
            if draft.count(expected) != 1:
                issues.append(f"{claim['id']}: expected exactly once in draft: {expected}")
    for fig in objects(ledger, "figures"):
        path = local(root, fig["file"])
        inputs.add(path)
        if not path.stat().st_size or not fig["mention"].strip() or fig["mention"] not in draft:
            issues.append(f"{fig['id']}: missing figure data or discussion")
        image_links = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", draft)
        if fig["file"] not in image_links:
            issues.append(f"{fig['id']}: draft points to a different figure file")
    for ref in objects(ledger, "citations"):
        if not ref["locator"].strip() or not ref["supports"].strip():
            raise ValueError(f"{ref['id']}: missing source location or statement supported")
        for field in ("in_text", "bibliography"):
            segment = ref[field]
            if not segment.strip() or draft.count(segment) != 1:
                issues.append(f"{ref['id']}: missing or ambiguous {field} anchor")
        if ref["in_text"] == ref["bibliography"]:
            raise ValueError(f"{ref['id']}: cite the reference in prose and in the bibliography")
    hashes = {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
              for path in sorted(inputs)}
    return {"schema": 1, "inputs": hashes}, issues


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["check", "freeze"])
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--receipt", type=Path, help="compare to a saved receipt or save a new one")
    args = parser.parse_args(argv)
    try:
        current, issues = audit(args.ledger.resolve(strict=True))
        if args.action == "freeze" and not args.receipt:
            parser.error("freeze requires --receipt PATH")
        if args.action == "check" and args.receipt:
            old = json.loads(args.receipt.read_text(encoding="utf-8-sig"))
            if current != old:
                issues.append("STALE: the draft, evidence, figure or ledger has changed since review")
        if issues:
            for issue in issues:
                print(issue)
            return 1
        if args.action == "freeze":
            with args.receipt.open("x", encoding="utf-8") as stream:
                json.dump(current, stream, indent=2, ensure_ascii=False)
                stream.write("\n")
        print("Declared checks matched. Inspect uncatalogued claims, citations and figures independently.")
        return 0
    except (OSError, ValueError, TypeError, KeyError, InvalidOperation, csv.Error) as exc:
        print(f"Cannot verify: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
