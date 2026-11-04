#!/usr/bin/env python3
"""ARTEMIS offline-first Android/Termux task and diagnostics prototype.

This prototype manages local tasks and checks its runtime. It does not control
Android UI, access private device data, or require network connectivity.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

APP_HOME = Path(os.environ.get("ARTEMIS_HOME", Path.home() / ".artemis"))
TASKS_FILE = APP_HOME / "tasks.json"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_tasks(path: Path = TASKS_FILE) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Cannot read task store {path}: {exc}") from exc
    if not isinstance(data, list) or any(not isinstance(item, dict) for item in data):
        raise RuntimeError(f"Task store has an invalid format: {path}")
    return data


def save_tasks(tasks: list[dict[str, Any]], path: Path = TASKS_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(tasks, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def add_task(title: str, path: Path = TASKS_FILE) -> dict[str, Any]:
    cleaned = title.strip()
    if not cleaned:
        raise ValueError("Task title cannot be empty.")
    tasks = load_tasks(path)
    next_id = max((int(item.get("id", 0)) for item in tasks), default=0) + 1
    task = {"id": next_id, "title": cleaned, "done": False, "created_at": now_utc()}
    tasks.append(task)
    save_tasks(tasks, path)
    return task


def complete_task(task_id: int, path: Path = TASKS_FILE) -> dict[str, Any]:
    tasks = load_tasks(path)
    for task in tasks:
        if task.get("id") == task_id:
            task["done"] = True
            task["completed_at"] = now_utc()
            save_tasks(tasks, path)
            return task
    raise KeyError(f"No task with ID {task_id}.")


def diagnostics() -> dict[str, Any]:
    termux = bool(os.environ.get("PREFIX", "").startswith("/data/data/com.termux"))
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "termux_detected": termux,
        "storage_path": str(APP_HOME),
        "storage_exists": APP_HOME.exists(),
        "network_required": False,
        "android_ui_automation": "not implemented; requires a separately tested permission bridge",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ARTEMIS offline-first local assistant prototype")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="Check local runtime and Termux detection")
    sub.add_parser("status", help="Show local task counts")
    add = sub.add_parser("add", help="Add a local task")
    add.add_argument("title")
    sub.add_parser("list", help="List local tasks")
    done = sub.add_parser("done", help="Mark a task complete")
    done.add_argument("task_id", type=int)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "doctor":
            print(json.dumps(diagnostics(), indent=2))
        elif args.command == "status":
            tasks = load_tasks()
            complete = sum(bool(task.get("done")) for task in tasks)
            print(f"Tasks: {len(tasks)} | completed: {complete} | open: {len(tasks) - complete}")
        elif args.command == "add":
            task = add_task(args.title)
            print(f"Added task #{task['id']}: {task['title']}")
        elif args.command == "list":
            tasks = load_tasks()
            if not tasks:
                print("No tasks yet.")
            for task in tasks:
                marker = "x" if task.get("done") else " "
                print(f"[{marker}] {task['id']}: {task['title']}")
        elif args.command == "done":
            task = complete_task(args.task_id)
            print(f"Completed task #{task['id']}: {task['title']}")
        return 0
    except (RuntimeError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
