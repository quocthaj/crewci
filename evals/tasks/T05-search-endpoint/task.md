# T05: Add a search endpoint

## Context

This is a small FastAPI todo service (`todo_api/`, in-memory store).

## Feature

Add `GET /todos/search?q=<text>`.

## Requirements

- Returns the todos whose title contains `q`, case-insensitively, ordered by id ascending.
- No match returns `200` with an empty list.
- `q` is required: a missing or empty `q` returns `422`.
- Existing routes such as `GET /todos/{todo_id}` must keep working.

## Rules

- Keep the public API backwards compatible.
- Do not edit or delete the existing tests in `tests/`; you may add new tests.
- Run the tests with `python -m pytest`.
