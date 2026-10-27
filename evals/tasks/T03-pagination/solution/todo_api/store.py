"""In-memory store for todos."""

from todo_api.schemas import Todo, TodoCreate, TodoUpdate


class TodoStore:
    def __init__(self) -> None:
        self._items: dict[int, Todo] = {}
        self._next_id = 1

    def create(self, data: TodoCreate) -> Todo:
        todo = Todo(id=self._next_id, title=data.title, done=data.done)
        self._items[todo.id] = todo
        self._next_id += 1
        return todo

    def get(self, todo_id: int) -> Todo | None:
        return self._items.get(todo_id)

    def list_all(self, done: bool | None = None, limit: int = 50, offset: int = 0) -> list[Todo]:
        items = list(self._items.values())
        if done is not None:
            items = [t for t in items if t.done == done]
        return items[offset : offset + limit]

    def update(self, todo_id: int, data: TodoUpdate) -> Todo | None:
        todo = self._items.get(todo_id)
        if todo is None:
            return None
        if data.title is not None:
            todo.title = data.title
        if data.done is not None:
            todo.done = data.done
        return todo
