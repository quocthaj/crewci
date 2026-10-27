# T01: Filtering by done returns the wrong todos

## Context

This is a small FastAPI todo service (`todo_api/`, in-memory store).

## Problem

`GET /todos?done=true` should return only completed todos and `GET /todos?done=false` only the
open ones, but the results are wrong.

## Requirements

- Fix the bug so the `done` filter behaves as described.
- Requests without the `done` parameter must still return every todo.

## Rules

- Keep the public API backwards compatible.
- Do not edit or delete the existing tests in `tests/`; you may add new tests.
- Run the tests with `python -m pytest`.
