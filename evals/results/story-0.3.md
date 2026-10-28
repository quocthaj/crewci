# Ghi chép Story 0.3: chạy thủ công bằng OpenWork

Ngày chạy: 2026-10-28. Dữ liệu chưa đủ để so sánh hai model.

## Kết quả từng lượt

| Workspace | Model | Task | Kết quả chấm | Độ tin cậy | Ghi chú |
|---|---|---|---|---|---|
| T01-a | Auto (model thực tế không rõ) | T01 | pass | trung bình | sửa đúng 1 dòng, thêm 2 test |
| T02-a | Auto (model thực tế không rõ) | T02 | pass | trung bình | giống đáp án, thêm 3 test |
| T01-b | Gemini Flash 3 (tên đầy đủ chưa xác nhận) | T01 | pass | khá | chưa xác nhận quota còn khi chạy |
| T03-b | Lẫn model | T03 | pass | thấp | agent sau chỉ xác minh và thêm tests/test_pagination_extra.py; không dùng để so sánh |
| T02-b | Gemini Flash 3, rồi chuyển model khác | T02 | chưa có kết quả hợp lệ | không dùng | hết quota khi đang chạy; workspace không có thay đổi khi kiểm tra; cần chạy lại sạch |

## Phát hiện

- Gói miễn phí của Google hết quota giữa chừng, khi đang chạy T02-b. Một task agent gồm nhiều lần gọi model nên tốn nhanh hơn chat thường.
- Agent trong OpenWork chạy lệnh trên Windows (không có `uv`), chỉ chạm tới Ubuntu qua lệnh `wsl`. Lệnh test chuẩn đổi thành `py -3.10 -m pytest -q`.
- Gemini 3.1 Pro báo `limit: 0` ở gói miễn phí, tức không có hạn mức miễn phí cho model đó.
- Test `test_ids_are_not_reused` của T02 qua ngay cả khi chưa có tính năng; nên thêm kiểm tra mã trả về của DELETE.

## Việc cần làm

- Xác nhận tên đầy đủ của model Gemini đã dùng (đọc ở ô chọn model của phiên T01-b).
- Chạy lại T02 và T03 từ workspace sạch, một model duy nhất, khi quota được đặt lại.
- Chạy cùng ba task với Model B.
