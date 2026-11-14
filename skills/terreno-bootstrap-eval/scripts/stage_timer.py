#!/usr/bin/env python3
"""Record wall time per bootstrap stage attempt.

    stage_timer.py start <eval-dir> <stage>
    stage_timer.py stop  <eval-dir> <stage> --status pass|fail|blocked [--tokens N]
    stage_timer.py show  <eval-dir>

Writes <eval-dir>/timings.json. Every start opens a new attempt, so reruns of a
stage after a fix round are kept beside the first attempt, never overwritten.
"""
import argparse
import datetime
import json
import pathlib
import sys

STATUSES = ("pass", "fail", "blocked")


def now():
    return datetime.datetime.now(datetime.timezone.utc)


def load(path):
    if path.exists():
        return json.loads(path.read_text())
    return {"stages": {}}


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def open_attempt(attempts):
    for attempt in reversed(attempts):
        if "stoppedAt" not in attempt:
            return attempt
    return None


def start(path, stage):
    data = load(path)
    attempts = data["stages"].setdefault(stage, [])
    if open_attempt(attempts):
        sys.exit(f"{stage}: an attempt is already running; stop it first")
    attempts.append({"attempt": len(attempts) + 1, "startedAt": now().isoformat()})
    save(path, data)
    print(f"{stage}: attempt {len(attempts)} started")


def stop(path, stage, status, tokens):
    data = load(path)
    attempt = open_attempt(data["stages"].get(stage, []))
    if not attempt:
        sys.exit(f"{stage}: no running attempt")
    stopped = now()
    started = datetime.datetime.fromisoformat(attempt["startedAt"])
    attempt["stoppedAt"] = stopped.isoformat()
    attempt["seconds"] = round((stopped - started).total_seconds())
    attempt["minutes"] = round(attempt["seconds"] / 60, 1)
    attempt["status"] = status
    if tokens is not None:
        attempt["tokens"] = tokens
    save(path, data)
    print(f"{stage}: attempt {attempt['attempt']} {status} in {attempt['minutes']} min")


def show(path):
    data = load(path)
    first_total = 0.0
    all_total = 0.0
    print(f"{'stage':<16}{'attempts':>9}{'first (min)':>13}{'all (min)':>11}  status")
    for stage, attempts in data["stages"].items():
        done = [a for a in attempts if "minutes" in a]
        if not done:
            continue
        first = done[0]["minutes"]
        total = sum(a["minutes"] for a in done)
        first_total += first
        all_total += total
        print(f"{stage:<16}{len(done):>9}{first:>13}{round(total, 1):>11}  {done[-1]['status']}")
    print(f"{'total':<16}{'':>9}{round(first_total, 1):>13}{round(all_total, 1):>11}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("start", "stop", "show"):
        command = sub.add_parser(name)
        command.add_argument("eval_dir", type=pathlib.Path)
        if name != "show":
            command.add_argument("stage")
        if name == "stop":
            command.add_argument("--status", choices=STATUSES, required=True)
            command.add_argument("--tokens", type=int)
    args = parser.parse_args()
    path = args.eval_dir / "timings.json"
    if args.command == "start":
        start(path, args.stage)
    elif args.command == "stop":
        stop(path, args.stage, args.status, args.tokens)
    else:
        show(path)


if __name__ == "__main__":
    main()
