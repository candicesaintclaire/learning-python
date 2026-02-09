# Learning Python — Learn in Public

A minimal, terminal-first workflow for working through *Learn Python 3 the Hard Way* while documenting progress publicly.

This repository pairs a simple CLI (`learnpython`) with a structured GitHub repo so each chapter produces a durable, reviewable artifact: source code, terminal output, and notes.

---

## What this is

- Read the book **in the terminal**
- Write and run exercises as normal Python files
- Automatically capture terminal output
- Commit and push each chapter as you go

No web app. No dashboards. Just a repeatable loop.

---

## How it works (high level)

1. `learnpython start`
   - Opens a tmux workspace
   - Left pane: chapter text
   - Right pane: logged shell for exercises

2. Work the chapter
   - Edit files in `chapters/chXX/src/`
   - Run them normally (`python3 exX.py`)

3. `learnpython done`
   - Finalizes logs
   - Commits the chapter
   - Pushes to GitHub
   - Advances to the next chapter

---

## Repository layout

```text
book/                  # Source PDF
chapters/
  ch01/
    src/               # Exercise files
    session.log        # Raw terminal log
    output.txt         # Cleaned terminal output
  ch02/
    ...
tools/                 # CLI scripts
.learnpython_state.json # Current chapter tracker
.learnpython_chapters.json # Auto-generated chapter index
```

---

## Philosophy

This project is intentionally boring:

- Deterministic
- Local-first
- Text-only
- Version controlled

The goal is not polish — it’s **proof of work**.

---

## Status

Work in progress. Built for personal use, but structured so others can follow along.
