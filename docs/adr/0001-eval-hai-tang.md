# ADR 0001: Eval hai tầng, tầng chính là repo mẫu tự viết với test ẩn

- Trạng thái: đã chốt
- Ngày: 2026-10-22

## Bối cảnh

CrewCI cần một bộ eval để đo các cấu hình (model, agent) một cách khách quan. Bộ eval phải chạy được trên máy cá nhân, tốn ít token, cho kết quả lặp lại được, và không quá dễ bị model "học thuộc".

## Các lựa chọn

1. **SWE-bench (Verified, Lite hoặc Mini):** có điểm tham chiếu công khai, nhưng mỗi task cần môi trường Docker riêng, bản đầy đủ rất nặng, mỗi lần chạy tốn nhiều token, và điểm phụ thuộc vào harness nên khó so sánh trực tiếp. Repo công khai nổi tiếng cũng có nguy cơ đã nằm trong dữ liệu huấn luyện của model.
2. **Repo mẫu nhỏ tự viết với test ẩn:** nhanh, rẻ, chạy được ngay trên laptop, tự kiểm soát độ khó và tiêu chí đúng/sai. Nhược điểm: không có điểm tham chiếu bên ngoài và số lượng task ít nên độ nhiễu cao.

## Quyết định

- **Tầng 1 (chính):** repo mẫu `evals/repos/todo_api` cùng các task bug và tính năng, mỗi task có test ẩn làm tiêu chí đúng/sai. Test ẩn và lời giải không nằm trong workspace của agent; khi chấm, test hiển thị gốc và test ẩn được chạy từ thư mục tạm.
- **Tầng 2 (tùy chọn, làm sau khi tầng 1 chạy ổn):** lấy một ít mẫu từ SWE-bench Verified Mini để có điểm tham chiếu ngoài, ghi rõ harness đã dùng.
- Mỗi task phải qua `selftest`: trạng thái xuất phát trượt test ẩn, lời giải tham chiếu qua tất cả.

## Hệ quả

- Dễ lặp lại và rẻ, nên chạy eval thường xuyên được.
- Với số task ít, kết quả cần chạy lặp và nêu biên dao động trước khi kết luận cải thiện.
- Phải tự bảo trì bộ task; thêm task mới phải kèm lời giải và qua selftest.
