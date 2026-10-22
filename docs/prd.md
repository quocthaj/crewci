# CrewCI – Product Requirements Document (PRD)

Oct 18, 2026 · @Thai Truong Cong Quoc

CrewCI là hệ thống chạy local nhận một yêu cầu phần mềm, giao cho đội agent thực hiện, kiểm tra bằng CI, deploy có rollback và hiển thị toàn bộ quá trình trên dashboard. Đây là PRD v1.1, bản chốt để bắt đầu làm, nguồn chuẩn cho mục tiêu, yêu cầu, epic và story của dự án; cấu trúc gần với PRD của BMAD (mục tiêu, yêu cầu FR/NFR, giả định kỹ thuật, epic và story có tiêu chí chấp nhận).

| Ngày | Phiên bản | Nội dung |
| --- | --- | --- |
| 18/10/2026 | 1.0 | Bản đầu tiên, tách ra từ tài liệu tổng quan |
| 18/10/2026 | 1.1 | Chốt quyết định mặc định cho các câu hỏi mở, thêm chiến lược eval hai tầng và kế hoạch bắt đầu |

## 1. Mục tiêu và bối cảnh

### 1.1 Mục tiêu

- Xây hệ thống multi-agent tự chia việc và thực thi công việc phát triển phần mềm trên một repo thật; đầu ra là Pull Request đã qua CI.
- Tự xây hạ tầng DevOps: cô lập công việc, CI, deploy tool, health check, rollback.
- Có số liệu khách quan: bộ eval và dashboard để so sánh model, agent và cấu hình trước/sau mỗi cải tiến.
- Làm dự án trung tâm trong CV: có tài liệu thiết kế, ADR và số liệu để trình bày khi phỏng vấn.
- Chạy với chi phí hạ tầng gần như bằng 0 trong giai đoạn phát triển (không dùng VPS).

### 1.2 Bối cảnh

Các agent lập trình hiện có (Claude Code, Codex, OpenHands, Devin...) đã viết được code. Phần khó và ít được thể hiện là lớp điều khiển xung quanh: điều phối, cổng kiểm soát tự động, deploy an toàn, quan sát và đo lường. CrewCI tập trung vào lớp đó. Tác giả là một AI engineer muốn bổ sung kỹ năng DevOps và LLMOps, nên dự án vừa là môi trường học vừa là sản phẩm portfolio.

### 1.3 Phi mục tiêu

- Không làm app desktop hay IDE riêng.
- Không thay thế lập trình viên hay xử lý dự án quy mô lớn.
- Không phục vụ nhiều người dùng đồng thời ở giai đoạn đầu.
- Không dùng code hay dữ liệu của công việc hiện tại làm đầu vào.
- Không huấn luyện model riêng và không dùng dịch vụ quyết định trả phí trong MVP (xem Epic 6).

## 2. Người dùng và kịch bản

Người dùng chính là tác giả, một nhà phát triển tự duyệt PR và tự deploy. Người xem thứ hai là nhà tuyển dụng hoặc người phỏng vấn xem repo, tài liệu và dashboard.

1. **Giao việc:** chạy `devteam run "<yêu cầu>" --repo <đường dẫn> --budget <token>`; hệ thống tạo task, agent làm việc, PR xuất hiện.
2. **Theo dõi:** mở dashboard xem run đang chạy, từng bước của agent, token và chi phí; dừng run khi cần.
3. **Duyệt và deploy:** duyệt PR đã qua CI, chạy deploy, xem health check; rollback khi lỗi.
4. **Đánh giá:** chạy bộ eval trên một cấu hình (model/agent) và so sánh với baseline.

## 3. Yêu cầu chức năng (FR)

**Điều phối và agent**

- **FR1.** Nhận yêu cầu qua CLI (tùy chọn qua GitHub issue) cùng repo đích và ràng buộc: ngân sách token, thời gian, số vòng lặp.
- **FR2.** Planner tách yêu cầu thành các task nhỏ, mỗi task có tiêu chí hoàn thành kiểm tra được, và ghi vào task board.
- **FR3.** Mỗi task chạy trên một git worktree/branch riêng và trong một Docker sandbox riêng.
- **FR4.** Coder sửa code và chạy lệnh qua bộ công cụ có kiểm soát (git, file, shell trong sandbox).
- **FR5.** Reviewer rà soát diff và có thể yêu cầu sửa; Tester viết hoặc chạy test.
- **FR6.** Task chỉ được coi là xong khi qua cổng kiểm soát tự động (lint, test, build trong CI); không dựa vào việc agent tự báo cáo.
- **FR7.** Dừng task khi vượt ngân sách token, thời gian hoặc số lần thử lại, và đánh dấu cần người xử lý.
- **FR8.** Lớp LLMClient cho phép đổi model/provider bằng cấu hình.
- **FR9.** Interface CodingAgent cho phép cắm agent tự viết hoặc agent có sẵn (ví dụ OpenHands, Aider) làm Coder.

**CI/CD và deploy**

- **FR10.** Tạo PR cho mỗi run đạt cổng kiểm soát; người dùng tự duyệt (self-approved) trước khi merge.
- **FR11.** Deploy tool nhận artifact đã qua CI, deploy bằng Docker và chạy health check.
- **FR12.** Rollback về bản trước khi health check thất bại hoặc khi người dùng yêu cầu.

**Quan sát**

- **FR13.** Mọi hành động của agent ghi thành sự kiện có cấu trúc vào cơ sở dữ liệu (mục 7).
- **FR14.** Dashboard liệt kê run, chi tiết run (dòng thời gian, diff, log test) và số liệu tổng hợp (tỉ lệ pass, token và chi phí, retry, thời gian).
- **FR15.** Dừng run từ CLI hoặc dashboard; run tự dừng khi vượt giới hạn.

**Eval**

- **FR16.** Bộ eval khoảng 20 task mẫu trên repo mẫu, có script chấm điểm tự động.
- **FR17.** Chạy eval cho từng cấu hình và lưu kết quả để so sánh trên dashboard.
- **FR18.** Tạo baseline đầu tiên trước khi thêm tính năng tối ưu.

**An toàn**

- **FR19.** Agent chỉ thấy workspace của task; lệnh nguy hiểm bị chặn hoặc cần xác nhận.
- **FR20.** Khóa API và bí mật không ghi vào log, sự kiện hay repo.

## 4. Yêu cầu phi chức năng (NFR)

- **NFR1.** Chạy toàn bộ bằng Docker Compose trên một máy cá nhân (WSL2), không cần VPS.
- **NFR2.** Chi phí token kiểm soát được: mỗi run có ngân sách tối đa và dashboard hiển thị chi phí ước tính.
- **NFR3.** Tái lập được: mỗi run lưu đủ cấu hình (model, prompt, phiên bản) để chạy lại và so sánh.
- **NFR4.** Mọi thay đổi do agent sinh ra đều đi qua CI; không có đường tắt vào nhánh main.
- **NFR5.** Kết quả eval ghi rõ độ nhiễu khi chạy lặp, vì đầu ra của LLM không hoàn toàn ổn định.
- **NFR6.** Dễ thay thế thành phần: model, agent, cơ sở dữ liệu (SQLite sang PostgreSQL) đều nằm sau interface.
- **NFR7.** Tài liệu đủ để người khác cài và chạy lại: README, kiến trúc, ADR cho các quyết định lớn.
- **NFR8.** Sandbox không mount thư mục cá nhân; dữ liệu công việc hiện tại không đưa vào hệ thống.
- **NFR9.** Mọi lỗi của agent hoặc pipeline đều có sự kiện và log để truy vết.

## 5. Mục tiêu giao diện

**CLI (đề xuất):** `devteam run`, `devteam status`, `devteam stop`, `devteam eval`, `devteam deploy`.

**Dashboard:** web nhẹ (FastAPI + Jinja + HTMX) với bốn màn: danh sách run, chi tiết run, số liệu tổng hợp, so sánh eval. Ưu tiên rõ ràng và có dữ liệu hơn là thẩm mỹ.

## 6. Giả định kỹ thuật

- **Cấu trúc repo:** monorepo gồm `agents/`, `orchestrator/`, `tools/`, `sandbox/`, `deployer/`, `dashboard/`, `evals/`, `infra/`, `docs/`.
- **Kiến trúc:** orchestrator (state machine mỏng bằng asyncio, đặt sau interface để có thể thay bằng LangGraph), worker agents, FastAPI, SQLite; deployer là CLI/daemon riêng.
- **Ngôn ngữ:** Python 3.12 cho toàn bộ MVP; Go là tùy chọn cho deployer ở giai đoạn sau.
- **Model:** gọi qua LLMClient (OpenRouter hoặc gateway); model mạnh cho Planner/Reviewer, model rẻ hoặc local cho việc đơn giản; chọn bằng eval.
- **Tool cho agent:** MCP server hoặc function calling.
- **Công cụ phát triển:** WSL2, Docker, uv, ruff, pytest, pre-commit, Makefile hoặc just, GitHub Actions.
- **Quan sát:** sự kiện trong cơ sở dữ liệu là nguồn chính; Langfuse, Prometheus, Grafana là tùy chọn nhận bản sao.
- **Kiểm thử:** unit test cho orchestrator và deployer; integration test chạy một run mẫu end-to-end trên repo mẫu; eval là kiểm thử chấp nhận.
- **Giả định khác:** máy đủ RAM chạy Docker Compose; có ngân sách token nhỏ cho API; OpenWork dùng ở giai đoạn 0 để làm quen và lập bảng so sánh model.

## 7. Định dạng sự kiện

| Trường | Ý nghĩa |
| --- | --- |
| run\_id, task\_id | Mã lần chạy và task con |
| agent | planner, coder, reviewer, tester, devops |
| event\_type | bắt đầu, gọi model, gọi công cụ, kết quả test, retry, kết thúc |
| model, tokens\_in, tokens\_out, cost | Model được gọi, số token và chi phí ước tính |
| duration\_ms, status | Thời gian và trạng thái |
| ref | Tham chiếu tới diff, log test hoặc commit |

## 8. Danh sách Epic

| Epic | Tên | Mục tiêu | Giai đoạn |
| --- | --- | --- | --- |
| E0 | Nền tảng và baseline | Repo, Compose, CI khung, repo mẫu, bảng so sánh model | 0 |
| E1 | Orchestrator và Coder | Chạy được một run từ yêu cầu đến commit trên branch | 1 |
| E2 | Đội agent đầy đủ và cổng CI | Reviewer, Tester, cổng CI, tạo PR | 2 |
| E3 | Deploy tool | Deploy Docker, health check, rollback | 3 |
| E4 | Dashboard và quan sát | Xem run, số liệu tổng hợp, dừng run | 4 |
| E5 | Eval và benchmark | Harness, baseline, so sánh cấu hình | 0 đến 4 |
| E6 | Mở rộng sau MVP (tùy chọn) | Agent có sẵn, nút quyết định, classifier riêng | Sau MVP |

Ghi sự kiện bắt đầu từ E1; dashboard ở E4 đọc lại dữ liệu đó.

## 9. Chi tiết Epic và Story

### Epic 0 – Nền tảng và baseline

Mục tiêu: có môi trường làm việc, repo mẫu và con số đầu tiên để so sánh.

**Story 0.1 – Khởi tạo repo và môi trường.** Là tác giả, tôi muốn một repo có sẵn cấu trúc và môi trường chạy, để bắt đầu viết code ngay.

- Repo có cấu trúc thư mục theo mục 6.
- `make up` chạy Docker Compose với FastAPI và SQLite.
- GitHub Actions chạy lint và test; pre-commit chạy ruff.

**Story 0.2 – Chọn repo mẫu và bộ task.** Là tác giả, tôi muốn repo mẫu có test sẵn, để đo kết quả khách quan.

- Tầng 1 (chính): 1 đến 2 repo mẫu nhỏ, khoảng 200 đến 500 dòng, do tác giả tự viết và có bộ test chạy được.
- Có ít nhất 5 task mẫu (cài sẵn một lỗi hoặc gỡ một tính năng), mỗi task có test ẩn làm tiêu chí đúng/sai; agent không thấy test chấm điểm.
- Tầng 2 (tùy chọn, chỉ sau khi tầng 1 chạy ổn): lấy một ít mẫu từ SWE-bench Verified Mini làm tham chiếu ngoài.
- Lựa chọn được ghi vào ADR.

**Story 0.3 – Bảng so sánh model đầu tiên.** Là tác giả, tôi muốn thử cùng một việc trên nhiều model bằng OpenWork, để hiểu khác biệt trước khi tự xây.

- Cùng 3 task chạy trên ít nhất 2 model.
- Bảng ghi pass/fail, thời gian, số lần phải sửa tay.
- Kết quả lưu trong `evals/`.

### Epic 1 – Orchestrator và Coder

Mục tiêu: một run đi từ yêu cầu đến commit trên branch riêng, có giới hạn an toàn.

**Story 1.1 – CLI nhận yêu cầu.** Là tác giả, tôi muốn giao việc bằng một lệnh, để không phải thao tác tay.

- `devteam run` tạo run\_id và lưu yêu cầu, repo, ngân sách.
- Từ chối khi thiếu tham số bắt buộc.
- Ghi sự kiện bắt đầu run.

**Story 1.2 – Planner tách task.** Là tác giả, tôi muốn yêu cầu được chia thành task có tiêu chí rõ ràng.

- Từ một yêu cầu mẫu sinh danh sách task có tiêu chí hoàn thành.
- Task được lưu vào task board và kiểm tra theo schema.

**Story 1.3 – Coder chạy trong sandbox.** Là tác giả, tôi muốn Coder làm việc cô lập, để agent không chạm vào máy của tôi.

- Mỗi task có worktree và container riêng.
- Coder sửa code, chạy test và commit lên branch của task.
- Sandbox bị hủy sau khi task kết thúc.

**Story 1.4 – Giới hạn và dừng an toàn.** Là tác giả, tôi muốn task tự dừng khi vượt giới hạn, để không đốt token.

- Vượt ngân sách token, thời gian hoặc số retry thì task dừng ở trạng thái cần người xử lý.
- Lý do dừng được ghi thành sự kiện.

**Story 1.5 – LLMClient.** Là tác giả, tôi muốn đổi model bằng cấu hình, để chạy eval so sánh dễ dàng.

- Đổi model không cần sửa code agent.
- Mỗi lời gọi ghi token, chi phí và thời gian.

### Epic 2 – Đội agent đầy đủ và cổng CI

Mục tiêu: thêm review, kiểm thử và cổng CI để task chỉ xong khi có bằng chứng.

**Story 2.1 – Reviewer.** Là tác giả, tôi muốn diff được rà soát trước khi lên CI.

- Reviewer nhận diff và yêu cầu task, trả về chấp nhận hoặc danh sách cần sửa.
- Số vòng review tối đa cấu hình được.

**Story 2.2 – Tester.** Là tác giả, tôi muốn thay đổi có test đi kèm.

- Tester viết hoặc chạy test cho thay đổi.
- Kết quả test được ghi thành sự kiện.

**Story 2.3 – Cổng CI.** Là tác giả, tôi muốn không có đường tắt vào main.

- PR chỉ được tạo khi lint, test và build đều qua.
- Agent không thể merge.
- Task fail CI quay lại Coder trong giới hạn retry.

**Story 2.4 – Tạo PR.** Là tác giả, tôi muốn PR có đủ thông tin để duyệt nhanh.

- PR có mô tả gồm yêu cầu, task, kết quả test và chi phí.
- Tôi duyệt thủ công trước khi merge.

### Epic 3 – Deploy tool

Mục tiêu: deploy an toàn, có kiểm tra và đường lùi.

**Story 3.1 – Deploy bằng Docker.** Là tác giả, tôi muốn deploy artifact đã qua CI bằng một lệnh.

- `devteam deploy` nhận artifact và chạy bản thử ở local.
- Sự kiện deploy được ghi lại.

**Story 3.2 – Health check.** Là tác giả, tôi muốn biết bản mới có sống không.

- Kiểm tra endpoint sức khỏe sau deploy với thời gian chờ cấu hình.
- Kết quả được ghi thành sự kiện.

**Story 3.3 – Rollback.** Là tác giả, tôi muốn quay lại bản trước khi có lỗi.

- Health check thất bại thì tự trở về bản trước.
- Có lệnh rollback thủ công.
- Có test mô phỏng deploy lỗi.

### Epic 4 – Dashboard và quan sát

Mục tiêu: nhìn thấy agent đang làm gì và làm tốn bao nhiêu.

**Story 4.1 – API sự kiện.** Là tác giả, tôi muốn dashboard đọc trực tiếp từ cơ sở dữ liệu qua API.

- FastAPI có endpoint liệt kê run, chi tiết run và số liệu tổng hợp.

**Story 4.2 – Danh sách và chi tiết run.** Là tác giả, tôi muốn xem từng bước của từng agent.

- Thấy trạng thái từng task, dòng thời gian, diff và log test.

**Story 4.3 – Số liệu tổng hợp.** Là tác giả, tôi muốn có con số để ra quyết định.

- Hiển thị tỉ lệ pass, token và chi phí mỗi task, số retry, thời gian trung bình.

**Story 4.4 – Dừng run và cảnh báo.** Là tác giả, tôi muốn có phanh khẩn cấp.

- Nút dừng run hoạt động.
- Có cảnh báo khi gần chạm ngân sách.

### Epic 5 – Eval và benchmark

Mục tiêu: mọi cải tiến đều có số liệu trước và sau.

**Story 5.1 – Harness eval.** Là tác giả, tôi muốn chạy toàn bộ task mẫu bằng một lệnh.

- `devteam eval` chạy các task mẫu cho một cấu hình và tính điểm.
- Kết quả lưu vào cơ sở dữ liệu.

**Story 5.2 – Baseline.** Là tác giả, tôi muốn có mốc để so sánh.

- Baseline đầu tiên được ghi cùng cấu hình đã dùng.

**Story 5.3 – So sánh cấu hình.** Là tác giả, tôi muốn thấy cấu hình nào tốt hơn.

- Dashboard so sánh ít nhất 2 cấu hình trên cùng bộ eval.
- Ghi độ nhiễu khi chạy lặp.

**Story 5.4 – Mở rộng bộ eval.** Là tác giả, tôi muốn bộ eval đủ lớn để đáng tin.

- Bộ eval đạt khoảng 20 task mẫu.

### Epic 6 – Mở rộng sau MVP (tùy chọn)

Mục tiêu: thử các hướng tối ưu chỉ khi số liệu từ E5 cho thấy đáng làm. Dịch vụ quyết định trả phí như Jev chưa dùng ở MVP vì ngân sách; có thể đánh giá lại sau.

**Story 6.1 – Adapter agent có sẵn.** Là tác giả, tôi muốn so sánh agent của tôi với agent có sẵn.

- Ít nhất một agent mã nguồn mở (như OpenHands hoặc Aider) chạy sau interface CodingAgent.
- Được eval trên cùng bộ task.

**Story 6.2 – Nút quyết định.** Là tác giả, tôi muốn một bước phân loại rẻ và nhanh giữa các bước.

- Dùng model rẻ trả lời theo danh sách đáp án cố định kèm xác suất, cho một việc (ví dụ phân loại lỗi CI hoặc định tuyến model).
- So sánh chi phí và tỉ lệ pass trước/sau trên eval.

**Story 6.3 – Classifier tự huấn luyện.** Chỉ làm nếu 6.2 cho thấy đáng tối ưu.

- Có tập dữ liệu có nhãn từ dashboard, chia train/test theo repo.
- Có hiệu chỉnh xác suất (calibration).
- So sánh với kết quả của 6.2.

## 10. Rủi ro

| Rủi ro | Giảm thiểu |
| --- | --- |
| Lỗi chồng chất giữa các agent | Cổng test tự động, Reviewer, CI |
| Chi phí token vượt ngân sách | Giới hạn mỗi run, giới hạn retry, hiển thị chi phí |
| Model rẻ hoặc local quá yếu | Đo bằng eval; dùng model mạnh cho vai trò quan trọng |
| Agent chạy lệnh nguy hiểm | Sandbox, không mount thư mục cá nhân, chặn lệnh nguy hiểm |
| Phạm vi phình to | Làm đúng thứ tự giai đoạn; mỗi giai đoạn đứng độc lập |
| Phụ thuộc nhà cung cấp | Đặt LLMClient và CodingAgent sau interface |

## 11. Tiêu chí thành công

- Hoàn thành các task mẫu và tạo PR qua CI mà không cần can thiệp tay ở các task đơn giản.
- Có baseline và ít nhất một bảng so sánh hai cấu hình trên cùng bộ eval.
- Deploy tool chạy end-to-end, có health check và rollback.
- Dashboard hiển thị tỉ lệ pass, thời gian và chi phí token.
- Có tài liệu kiến trúc và ADR cho các quyết định lớn.

Các ngưỡng số cụ thể được đặt sau khi có baseline.

## 12. Quyết định mặc định và câu hỏi còn mở

Quyết định mặc định để bắt đầu (có thể đổi sau khi có số liệu):

- Nhận yêu cầu qua CLI; GitHub issue là tùy chọn sau MVP.
- Theo dõi CI bằng polling GitHub API, không dùng webhook hay tunnel.
- Dashboard cập nhật bằng polling của HTMX; SSE chỉ thêm khi cần.
- Lúc đầu dùng một model cho mọi vai trò; tách theo vai trò sau khi có dữ liệu từ Epic 0 và Epic 5.
- Không dùng BMAD trong MVP; PRD này là nguồn chính.
- Eval hai tầng như Story 0.2.
- Deploy tool viết bằng Python.

Còn mở:

- Viết repo mẫu gì cụ thể (thuộc Story 0.2).
- Kiểm tra tên CrewCI trước khi công khai repo, vì gần với CrewAI.
- Ngưỡng số liệu cụ thể, đặt sau khi có baseline.

## 13. Kế hoạch bắt đầu

1. Story 0.1: tạo repo, cấu trúc thư mục, `make up` và CI khung.
2. Story 0.2: viết repo mẫu đầu tiên (một API FastAPI nhỏ có test) và 5 task cài lỗi hoặc gỡ tính năng kèm test ẩn.
3. Story 0.3: chạy 3 task trên ít nhất 2 model bằng OpenWork và ghi bảng so sánh.
4. Viết hai ADR đầu tiên: lý do tự xây thay vì dùng framework agent có sẵn; và quyết định đặt LLMClient và CodingAgent sau interface.
5. Chỉ mở Epic 1 khi đã có bảng so sánh và baseline.
