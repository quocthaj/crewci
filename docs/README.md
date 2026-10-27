# Tài liệu CrewCI

- `docs/prd.md`: PRD (xuất từ Claude Doc).
- `docs/adr/`: mỗi quyết định thiết kế lớn là một file ADR (mẫu: `0000-template.md`).
  - `0001-eval-hai-tang.md`: chiến lược eval hai tầng.
- ADR nên viết tiếp: lý do tự xây thay vì dùng framework agent có sẵn; đặt LLMClient và CodingAgent sau interface.
