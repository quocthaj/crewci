# T02: Add a DELETE endpoint

## Context

This is a small FastAPI todo service (`todo_api/`, in-memory store).

## Feature

Add `DELETE /todos/{todo_id}`.

## Requirements

- Success: status `204` with an empty body.
- Unknown id: status `404` with a JSON body containing `detail`.
- After deletion the todo no longer appears in `GET /todos` and `GET /todos/{id}` returns `404`.
- Ids are never reused: creating a todo after a deletion gets a new, higher id.

## Rules

- Keep the public API backwards compatible.
- Do not edit or delete the existing tests in `tests/`; you may add new tests.
- Run the tests with `python -m pytest`.
