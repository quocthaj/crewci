"""Todo API: sample repo used as an eval target for CrewCI."""

from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from todo_api.schemas import Todo, TodoCreate, TodoUpdate
from todo_api.store import TodoStore


def create_app(store: TodoStore | None = None) -> FastAPI:
    store = store or TodoStore()
    app = FastAPI(title="Todo API")

    @app.post("/todos", status_code=201, response_model=Todo)
    def create_todo(data: TodoCreate) -> Todo:
        return store.create(data)

    @app.get("/todos", response_model=list[Todo])
    def list_todos(
        done: bool | None = None,
        limit: Annotated[int, Query(ge=1, le=100)] = 50,
        offset: Annotated[int, Query(ge=0)] = 0,
    ) -> list[Todo]:
        return store.list_all(done, limit=limit, offset=offset)

    @app.get("/todos/{todo_id}", response_model=Todo)
    def get_todo(todo_id: int) -> Todo:
        todo = store.get(todo_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo

    @app.patch("/todos/{todo_id}", response_model=Todo)
    def update_todo(todo_id: int, data: TodoUpdate) -> Todo:
        todo = store.update(todo_id, data)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo

    return app
