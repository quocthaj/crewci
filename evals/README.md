# evals

Bộ đo cho CrewCI: repo mẫu, các task, và harness chấm điểm (Story 0.2).

## Cấu trúc

```
evals/
├── repos/todo_api/        repo mẫu: API todo nhỏ bằng FastAPI, có test hiển thị
├── tasks/T0x-.../
│   ├── task.md            đề bài đưa cho agent (tiếng Anh)
│   ├── meta.json          loại (bug/feature), độ khó
│   ├── overlay/           file làm thay đổi trạng thái xuất phát (ví dụ cài sẵn lỗi)
│   ├── solution/          lời giải tham chiếu (KHÔNG đưa cho agent)
│   └── hidden/            test ẩn dùng để chấm điểm (KHÔNG đưa cho agent)
└── harness.py             list / prepare / grade / selftest
```

## Cách dùng

```bash
make eval-list                                   # liệt kê task
uv run python -m evals.harness prepare T01 --dest /tmp/ws1
# ... để agent (hoặc bạn) sửa code trong /tmp/ws1 theo TASK.md ...
uv run python -m evals.harness grade T01 --workspace /tmp/ws1
make eval-selftest                               # kiểm tra chính các task
```

`grade` in JSON gồm `visible_passed`, `hidden_passed`, `passed`; mã thoát 0 khi qua, 1 khi trượt.

## Quy ước

- Workspace của agent chỉ gồm repo mẫu, overlay và `TASK.md`. Test ẩn và lời giải không bao giờ nằm trong đó.
- Khi chấm, test hiển thị gốc và test ẩn đều được chép ra thư mục tạm rồi chạy với code trong workspace, nên sửa hoặc xóa test trong workspace không làm đổi kết quả.
- Một task hợp lệ khi: trạng thái xuất phát qua test hiển thị nhưng trượt test ẩn, và lời giải tham chiếu qua tất cả. `make eval-selftest` kiểm tra điều này và cũng chạy trong CI.
- Thêm task mới: tạo thư mục `tasks/T0x-ten`, đủ `task.md`, `meta.json`, `hidden/`, `solution/` (và `overlay/` nếu cần), rồi chạy selftest.

## Task hiện có

Xem `make eval-list`. Hiện có 5 task trên `todo_api`: 2 bug (T01, T04) và 3 tính năng (T02, T03, T05).
