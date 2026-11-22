"""Compare protected tokens in two self-contained TeX prose fragments."""

import argparse
import re
import sys
from itertools import zip_longest
from pathlib import Path

MATH = (r"(?<!\\)\$\$.*?(?<!\\)\$\$|(?<!\\)\$(?!\$).*?(?<!\\)\$|"
        r"\\\(.*?\\\)|\\\[.*?\\\]|"
        r"\\begin\{(?P<env>equation\*?|align\*?|gather\*?|multline\*?)\}.*?\\end\{(?P=env)\}")
REFERENCE = r"\\(?:cite[a-zA-Z]*|ref|eqref|autoref|cref|Cref|label)\*?(?:\s*\[[^\]]*\]){0,2}\s*\{[^{}]+\}"
UNITS = r"(?:\\%|(?:nm|mm|cm|km|mW|dBm|dB|THz|GHz|MHz|kHz|Hz|ns|ms|s|m|W)(?!\w))"
NUMBER = r"(?<![\w.])[+\-−]?(?:\d+(?:\.\d+)?|\.\d+)(?:[eE][+\-]?\d+)?(?:[ \t]*" + UNITS + r")?"
PROTECTED = re.compile(f"(?P<math>{MATH})|(?P<reference>{REFERENCE})|(?P<number>{NUMBER})", re.S)
UNSUPPORTED = re.compile(r"\\(?:input|include|includeonly|verb|newcommand|renewcommand|def|catcode)\b|"
                         r"\\begin\{(?:verbatim\*?|minted|lstlisting)\}")


def scan(text):
    visible = re.sub(r"(?<!\\)%[^\n]*", "", text)
    if UNSUPPORTED.search(visible):
        raise ValueError("Use self-contained text fragments; inspect included files and macros separately.")
    tokens = []
    tail_start = 0
    uncovered = []
    for item in PROTECTED.finditer(visible):
        uncovered.append(visible[tail_start:item.start()])
        tokens.append(item.group())
        tail_start = item.end()
    uncovered.append(visible[tail_start:])
    if re.search(r"(?<!\\)\$|\\[()[\]]|\\(?:begin|end)\{(?:align|equation|multline|gather)\*?\}", " ".join(uncovered)):
        raise ValueError("Unmatched math delimiters; inspect this fragment manually.")
    return tokens


def check(source, candidate, phrases):
    left, right = scan(source), scan(candidate)
    issues = []
    for index, (a, b) in enumerate(zip_longest(left, right), 1):
        if a != b:
            issues.append(f"protected item {index}: {a!r} -> {b!r}")
    for phrase in phrases:
        if not phrase.strip() or source.count(phrase) == 0:
            raise ValueError(f"Expected protected phrase in original: {phrase!r}")
        if source.count(phrase) != candidate.count(phrase):
            issues.append(f"protected wording changed: {phrase!r}")
    return issues


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path)
    parser.add_argument("edited", type=Path)
    parser.add_argument("--keep", action="append", default=[], help="also preserve this exact phrase")
    args = parser.parse_args(argv)
    try:
        findings = check(args.original.read_text(encoding="utf-8-sig"),
                         args.edited.read_text(encoding="utf-8-sig"), args.keep)
    except (ValueError, OSError) as error:
        print(f"Could not compare: {error}", file=sys.stderr)
        return 2
    for item in findings:
        print(item)
    if not findings:
        print("Protected tokens matched. Read both passages for scientific meaning and scope.")
    return int(bool(findings))


if __name__ == "__main__":
    sys.exit(main())
