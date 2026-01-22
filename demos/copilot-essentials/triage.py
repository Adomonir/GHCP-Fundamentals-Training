#!/usr/bin/env python3
"""
Quick log triage utility
────────────────────────
  • Accepts   *.log  or  *.log.gz
  • Filters   last N minutes (sliding window)
  • Tallies   (status‑code, endpoint) pairs
  • Optional  --status 499,321 for focused searching

  A noisy incident page reveals a spike in 321 or 499 errors, but the observability stack is lagging. You need a quick, local log sweep to spot patterns and counts.
"""

from pathlib import Path
from datetime import datetime, timedelta, timezone
import argparse
import gzip
import re
import sys
from collections import Counter
from typing import Iterable, Tuple

# ---------------------------------------------------------------------------
# ✨ Function placeholders – let Copilot write the bodies ✨
# ---------------------------------------------------------------------------

def read_lines(file_path: Path) -> Iterable[str]:
    """Open plain or gzipped log file and yield each line (stripped)."""
    pass
def read_lines(file_path: Path) -> Iterable[str]:
    """Open plain or gzipped log file and yield each line (stripped)."""
    if file_path.suffix == '.gz':
        open_func = gzip.open
        mode = 'rt'  # text mode
    else:
        open_func = open
        mode = 'r'

    with open_func(file_path, mode, encoding='utf-8') as f:
        for line in f:
            yield line.strip()  

                


def parse_line(line: str) -> Tuple[datetime, int, str] | None:
    """Return (timestamp_utc, status_code_int, url_path) or None if malformed."""
    pass  # ← Copilot will fill this in
def parse_line(line: str) -> Tuple[datetime, int, str] | None:
    """Return (timestamp_utc, status_code_int, url_path) or None if malformed."""
    log_pattern = re.compile(
        r'^\S+ \S+ \S+ \[(?P<timestamp>[^\]]+)\] "\S+ (?P<path>\S+) \S+" (?P<status>\d{3}) \d+'
    )
    match = log_pattern.match(line)
    if not match:
        return None

    timestamp_str = match.group('timestamp')
    path = match.group('path')
    status_str = match.group('status')

    try:
        timestamp = datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M:%S %z')
        timestamp_utc = timestamp.astimezone(timezone.utc)
        status_code = int(status_str)
    except (ValueError, TypeError):
        return None

    return (timestamp_utc, status_code, path)


def triage(
    lines: Iterable[str],
    minutes: int,
    wanted_status: set[int] | None
) -> Counter[Tuple[int, str]]:
    """Aggregate counts for lines within the window and matching status filter."""
    pass
def triage(
    lines: Iterable[str],
    minutes: int,
    wanted_status: set[int] | None
) -> Counter[Tuple[int, str]]:
    """Aggregate counts for lines within the window and matching status filter."""
    counter: Counter[Tuple[int, str]] = Counter()
    now_utc = datetime.now(timezone.utc)
    time_threshold = now_utc - timedelta(minutes=minutes)

    for line in lines:
        parsed = parse_line(line)
        if not parsed:
            continue

        timestamp_utc, status_code, path = parsed

        if timestamp_utc < time_threshold:
            continue

        if wanted_status is not None and status_code not in wanted_status:
            continue

        counter[(status_code, path)] += 1

    return counter



def render(counter: Counter[Tuple[int, str]], top: int) -> None:
    """Pretty‑print a Markdown‑style table of the top offenders."""
    pass 
    """Pretty‑print a Markdown‑style table of the top offenders."""
    print("| Rank | Status | Path | Hits |")
    print("|------|--------|------|------|")
    for rank, ((status, path), hits) in enumerate(counter.most_common(top),
                                                    start=1):
            print(f"| {rank} | {status} | {path} | {hits} |")




def main() -> None:
    """Wire everything together with argparse CLI options."""
    pass  # ← Copilot will fill this in
def main() -> None:
    """Wire everything together with argparse CLI options."""
    parser = argparse.ArgumentParser(description="Quick log triage utility")
    parser.add_argument("file", type=Path, help="Path to the log file (.log or .log.gz)")
    parser.add_argument("--minutes", type=int, default=15, help="Time window in minutes (default: 15)")
    parser.add_argument("--status", type=str, help="Comma-separated list of status codes to filter")
    parser.add_argument("--top", type=int, default=10, help="Number of top results to display (default: 10)")

    args = parser.parse_args()

    wanted_status = None
    if args.status:
        wanted_status = set(int(code) for code in args.status.split(","))

    lines = read_lines(args.file)
    counter = triage(lines, args.minutes, wanted_status)

    if not counter:
        print("No matching log entries found.", file=sys.stderr)
        sys.exit(1)

    render(counter, args.top)


if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------
# 📝 Copilot prompts – copy these into each empty function or keep them here
# ---------------------------------------------------------------------------
# read_lines prompt:
#   "Implement read_lines(file_path) so it transparently handles .log or .log.gz,
#    opens in text mode (UTF‑8), and yields one stripped line at a time."

# parse_line prompt:
#   "Use a compiled regex for common/combined log format; pull timestamp,
#    status, and path. Convert the timestamp '[15/Jul/2025:14:23:41 +0000]'
#    to a timezone‑aware UTC datetime. Return None if the line doesn't match."

# triage prompt:
#   "Stream through lines, parse each; skip malformed. Keep only entries whose
#    timestamp is within <minutes> of datetime.utcnow() and, if wanted_status
#    is provided, whose status is in that set. Use a Counter keyed by
#    (status_code, path)."

# render prompt:
#   "Print the top <top> (status, path) pairs from the Counter in descending
#    order of hits, formatted as a Markdown table: Rank | Status | Path | Hits."

# main prompt:
#   "Add argparse arguments:
#       --file (positional, required)
#       --minutes (int, default 15)
#       --status  (comma‑separated list of ints, optional)
#       --top     (int, default 10)
#    Parse args, build wanted_status set, call triage(), then render().
#    Exit with status‑code 1 if no matches were found."
