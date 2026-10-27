# T04: Cannot reopen a completed todo

## Context

This is a small FastAPI todo service (`todo_api/`, in-memory store).

## Problem

Sending `PATCH /todos/{id}` with `{"done": false}` to a completed todo leaves it completed.

## Requirements

- Fix the bug so a todo can be marked as not done again.
- Partial updates must still work: a field that is not sent must not change.

## Rules

- Keep the public API backwards compatible.
- Do not edit or delete the existing tests in `tests/`; you may add new tests.
- Run the tests with `python -m pytest`.
