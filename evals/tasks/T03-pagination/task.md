# T03: Add pagination to the list endpoint

## Context

This is a small FastAPI todo service (`todo_api/`, in-memory store).

## Feature

Add pagination to `GET /todos` with the query parameters `limit` and `offset`.

## Requirements

- `limit`: integer from 1 to 100, default 50.
- `offset`: integer greater than or equal to 0, default 0.
- Results are ordered by id ascending.
- Values outside the allowed ranges return `422`.
- Pagination works together with the existing `done` filter: the filter is applied first, then
  `offset` and `limit`.

## Rules

- Keep the public API backwards compatible.
- Do not edit or delete the existing tests in `tests/`; you may add new tests.
- Run the tests with `python -m pytest`.
