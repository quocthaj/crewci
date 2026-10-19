# CrewCI

Hệ thống điều phối đội AI agent: nhận một yêu cầu phần mềm, giao agent thực hiện, kiểm tra bằng CI, deploy có rollback, theo dõi trên dashboard.

Trạng thái: Story 0.1 (khung repo). Chưa có agent nào.

## Chạy nhanh (trong WSL2 Ubuntu)

Yêu cầu: git, make, Docker (đã nối với WSL), uv.

```bash
git init -b main      # nếu chưa là repo git
make setup            # cài phụ thuộc và pre-commit
make test             # chạy test
make lint             # kiểm tra ruff
make up               # chạy API bằng Docker Compose
make health           # gọi /health, kỳ vọng {"status":"ok"}
make down             # dừng
```

## Cấu trúc

Xem README trong từng thư mục. Cấu trúc theo mục 6 của PRD.

## Định nghĩa hoàn thành của Story 0.1

- `make up` chạy được, `make health` trả về ok
- `make test` và `make lint` pass
- GitHub Actions xanh trên commit đầu tiên
