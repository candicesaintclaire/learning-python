#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

REPO_ROOT = Path.cwd()
STATE_PATH = REPO_ROOT / ".learnpython_state.json"
CHAPTERS_PATH = REPO_ROOT / ".learnpython_chapters.json"
PDF_PATH = REPO_ROOT / "book" / "Learn Python 3 The Hard Way.pdf"

def die(msg: str, code: int = 1) -> None:
    print(f"ERROR: {msg}")
    raise SystemExit(code)

def sh(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=check, text=True)

def load_json(path: Path, default: Dict[str, Any]) -> Dict[str, Any]:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")

def ensure_repo_sanity() -> None:
    if not (REPO_ROOT / ".git").exists():
        die("This does not look like a git repo (missing .git). Run from repo root.")
    if not PDF_PATH.exists():
        die(f"Missing PDF at: {PDF_PATH}")

def chapter_dir(ch: int) -> Path:
    return REPO_ROOT / "chapters" / f"ch{ch:02d}"

def get_current_chapter(state: Dict[str, Any], override: Optional[int]) -> int:
    if override is not None:
        return override
    return int(state.get("current_chapter", 1))

def tmux_session_name(ch: int, suffix: Optional[int] = None) -> str:
    base = f"learnpython-ch{ch:02d}"
    return base if suffix is None else f"{base}-{suffix}"

def tmux_has_session(name: str) -> bool:
    cp = subprocess.run(["tmux", "has-session", "-t", name], text=True)
    return cp.returncode == 0

def prompt_existing_session(name: str) -> str:
    print(f"Existing tmux session found: {name}")
    print("Choose:")
    print("  1) Attach (resume)")
    print("  2) Kill & restart")
    print("  3) New session (keep old one)")
    choice = input("Enter 1, 2, or 3: ").strip()
    if choice not in {"1", "2", "3"}:
        return "1"
    return choice

def ensure_chapter_mapping(ch: int) -> Tuple[int, int, str]:
    chapters = load_json(CHAPTERS_PATH, default={"chapters": {}})
    key = str(ch)
    if key in chapters["chapters"]:
        info = chapters["chapters"][key]
        return int(info["start_page"]), int(info["end_page"]), str(info.get("title", f"Chapter {ch}"))

    print(f"No page range saved yet for Chapter {ch}.")
    print("Enter the PDF page range for this chapter (as shown in the book's TOC).")
    start_page = int(input("Start page (PDF page number): ").strip())
    end_page = int(input("End page (PDF page number): ").strip())
    title = input("Chapter title (optional): ").strip() or f"Chapter {ch}"

    chapters["chapters"][key] = {"start_page": start_page, "end_page": end_page, "title": title}
    save_json(CHAPTERS_PATH, chapters)
    return start_page, end_page, title

def extract_chapter_text(ch: int) -> Path:
    chdir = chapter_dir(ch)
    chdir.mkdir(parents=True, exist_ok=True)
    (chdir / "src").mkdir(parents=True, exist_ok=True)

    out_txt = chdir / "chapter.txt"
    if out_txt.exists() and out_txt.stat().st_size > 0:
        return out_txt

    start_page, end_page, _title = ensure_chapter_mapping(ch)
    # pdftotext is inclusive via -f/-l
    sh([
        "pdftotext",
        "-f", str(start_page),
        "-l", str(end_page),
        str(PDF_PATH),
        str(out_txt),
    ])
    if not out_txt.exists() or out_txt.stat().st_size == 0:
        die(f"Extraction produced empty chapter.txt for chapter {ch}. Check page range.")
    return out_txt

def start_tmux_workspace(ch: int, session: str) -> None:
    chdir = chapter_dir(ch)
    ch_txt = extract_chapter_text(ch)

    # Create session detached
    sh(["tmux", "new-session", "-d", "-s", session])

    # Left pane: read chapter
    sh(["tmux", "send-keys", "-t", session, f"less {ch_txt}", "C-m"])

    # Split right pane
    sh(["tmux", "split-window", "-h", "-t", session])

    # Right pane: logged shell in chapter folder
    # Note: using bash -lc to ensure cd works and script starts in that shell.
    session_log = chdir / "session.log"
    cmd = f'cd "{chdir}" && script -q -f "{session_log}" bash'
    sh(["tmux", "send-keys", "-t", f"{session}.1", cmd, "C-m"])

    # Attach
    sh(["tmux", "attach", "-t", session])

def strip_ansi(s: str) -> str:
    # Remove ANSI escape sequences
    ansi = re.compile(r"\x1B\\[[0-?]*[ -/]*[@-~]")
    return ansi.sub("", s)

def make_output_txt(ch: int) -> Path:
    chdir = chapter_dir(ch)
    session_log = chdir / "session.log"
    if not session_log.exists():
        die(f"Missing session.log at {session_log}. Did you run learnpython start and work in the right pane?")
    raw = session_log.read_text(errors="ignore")
    lines = raw.splitlines()

    cleaned: list[str] = []
    for line in lines:
        line = strip_ansi(line)
        if line.startswith("Script started") or line.startswith("Script done"):
            continue
        cleaned.append(line.rstrip())

    out = chdir / "output.txt"
    out.write_text("\n".join(cleaned).strip() + "\n", encoding="utf-8")
    return out

def git_commit_push(ch: int, title: str) -> None:
    chdir = chapter_dir(ch)
    sh(["git", "add", str(chdir), str(STATE_PATH), str(CHAPTERS_PATH)], check=True)
    msg = f"Chapter {ch:02d}: {title} (logs + exercises)"
    # If nothing to commit, git returns non-zero; handle gracefully.
    cp = subprocess.run(["git", "commit", "-m", msg], text=True)
    if cp.returncode != 0:
        print("Nothing to commit (or commit failed). Continuing to push attempt anyway.")
    sh(["git", "push"], check=True)

def cmd_start(args: argparse.Namespace) -> None:
    ensure_repo_sanity()
    state = load_json(STATE_PATH, default={"current_chapter": 1})
    ch = get_current_chapter(state, args.chapter)

    # Determine session name and handle existing
    session = tmux_session_name(ch)
    if tmux_has_session(session):
        choice = prompt_existing_session(session)
        if choice == "1":
            sh(["tmux", "attach", "-t", session])
            return
        if choice == "2":
            sh(["tmux", "kill-session", "-t", session])
        if choice == "3":
            suffix = 2
            while tmux_has_session(tmux_session_name(ch, suffix)):
                suffix += 1
            session = tmux_session_name(ch, suffix)

    # Save state (current chapter + last session name)
    state["current_chapter"] = ch
    state["last_session"] = session
    save_json(STATE_PATH, state)

    start_tmux_workspace(ch, session)

def cmd_done(args: argparse.Namespace) -> None:
    ensure_repo_sanity()
    state = load_json(STATE_PATH, default={"current_chapter": 1})
    ch = get_current_chapter(state, args.chapter)

    # Generate output.txt from session.log
    _ = extract_chapter_text(ch)  # ensure dirs exist
    start_page, end_page, title = ensure_chapter_mapping(ch)
    _out = make_output_txt(ch)

    # Commit + push
    git_commit_push(ch, title)

    # Advance chapter
    state["current_chapter"] = ch + 1
    save_json(STATE_PATH, state)

    print(f"Done. Advanced from chapter {ch:02d} to {ch+1:02d}.")
    print("Next: learnpython start")

def main() -> None:
    ap = argparse.ArgumentParser(prog="learnpython", description="LPTHW terminal workflow helper")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_start = sub.add_parser("start", help="Start a chapter tmux workspace (left=chapter, right=logged shell)")
    ap_start.add_argument("chapter", nargs="?", type=int, help="Chapter number (default: current chapter from state)")
    ap_start.set_defaults(func=cmd_start)

    ap_done = sub.add_parser("done", help="Finalize current chapter: output.txt + git commit + push + advance")
    ap_done.add_argument("chapter", nargs="?", type=int, help="Chapter number (default: current chapter from state)")
    ap_done.set_defaults(func=cmd_done)

    args = ap.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
