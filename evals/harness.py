"""Harness eval cho CrewCI (Story 0.2).

Lệnh:
    python -m evals.harness list
    python -m evals.harness prepare T01 --dest /tmp/ws1
    python -m evals.harness grade T01 --workspace /tmp/ws1
    python -m evals.harness selftest

Nguyên tắc: test chấm điểm (hidden) KHÔNG nằm trong workspace của agent. Chỉ khi chấm điểm
chúng mới được chạy, từ một thư mục tạm, nên agent không thể sửa test để qua.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

EVALS_DIR = Path(__file__).resolve().parent
BASE_REPO = EVALS_DIR / "repos" / "todo_api"
TASKS_DIR = EVALS_DIR / "tasks"
IGNORE = shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.pyc")


@dataclass
class GradeResult:
    task: str
    visible_passed: bool
    hidden_passed: bool
    passed: bool
    visible_output: str
    hidden_output: str


def list_tasks() -> list[str]:
    return sorted(p.name for p in TASKS_DIR.iterdir() if (p / "meta.json").exists())


def resolve_task(task_id: str) -> Path:
    matches = [
        p for p in TASKS_DIR.iterdir() if p.name == task_id or p.name.startswith(f"{task_id}-")
    ]
    if len(matches) != 1:
        raise SystemExit(
            f"Không tìm thấy task duy nhất cho '{task_id}'. Có: {', '.join(list_tasks())}"
        )
    return matches[0]


def _copy_tree(src: Path, dst: Path) -> None:
    shutil.copytree(src, dst, dirs_exist_ok=True, ignore=IGNORE)


def _git(path: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=path, check=True, capture_output=True)


def _init_git(path: Path) -> None:
    """Khởi tạo git cho workspace để xem được diff. Không bắt buộc."""
    try:
        _git(path, "init", "-q")
        _git(path, "add", "-A")
        _git(
            path,
            "-c",
            "user.name=crewci",
            "-c",
            "user.email=crewci@example.invalid",
            "commit",
            "-q",
            "-m",
            "initial state",
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass


def prepare(task_id: str, dest: str | Path) -> Path:
    """Tạo workspace: repo mẫu + overlay của task + TASK.md. Không chứa test ẩn."""
    task_dir = resolve_task(task_id)
    dest = Path(dest)
    if dest.exists() and any(dest.iterdir()):
        raise SystemExit(f"Thư mục đích không rỗng: {dest}")
    _copy_tree(BASE_REPO, dest)
    overlay = task_dir / "overlay"
    if overlay.exists():
        _copy_tree(overlay, dest)
    shutil.copy(task_dir / "task.md", dest / "TASK.md")
    _init_git(dest)
    return dest


def _run_pytest(workspace: Path, tests_dir: Path) -> tuple[bool, str]:
    env = {**os.environ, "PYTHONPATH": str(workspace), "PYTHONDONTWRITEBYTECODE": "1"}
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", str(tests_dir), "-q", "-p", "no:cacheprovider"],
            cwd=workspace,
            env=env,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        return False, "timeout sau 120s"
    return proc.returncode == 0, (proc.stdout + proc.stderr)[-2000:]


def grade(task_id: str, workspace: str | Path) -> GradeResult:
    """Chấm điểm: test hiển thị gốc (chống hồi quy) + test ẩn của task.

    Cả hai bộ test đều được chép ra thư mục tạm và chạy với code trong workspace, nên
    việc agent sửa hoặc xóa test trong workspace không ảnh hưởng kết quả.
    """
    task_dir = resolve_task(task_id)
    ws = Path(workspace).resolve()
    with tempfile.TemporaryDirectory() as tmp:
        visible_dir = Path(tmp) / "visible"
        hidden_dir = Path(tmp) / "hidden"
        _copy_tree(BASE_REPO / "tests", visible_dir)
        _copy_tree(task_dir / "hidden", hidden_dir)
        visible_ok, visible_out = _run_pytest(ws, visible_dir)
        hidden_ok, hidden_out = _run_pytest(ws, hidden_dir)
    return GradeResult(
        task=task_dir.name,
        visible_passed=visible_ok,
        hidden_passed=hidden_ok,
        passed=visible_ok and hidden_ok,
        visible_output=visible_out,
        hidden_output=hidden_out,
    )


def selftest(task_ids: list[str] | None = None) -> list[str]:
    """Kiểm tra bản thân các task. Trả về danh sách vấn đề (rỗng nếu ổn).

    Với mỗi task: (1) trạng thái xuất phát phải qua test hiển thị nhưng trượt test ẩn;
    (2) áp dụng lời giải tham chiếu thì phải qua tất cả.
    """
    problems: list[str] = []
    for name in task_ids or list_tasks():
        task_dir = resolve_task(name)
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "ws"
            prepare(name, ws)
            start = grade(name, ws)
            if not start.visible_passed:
                problems.append(f"{task_dir.name}: test hiển thị trượt ở trạng thái xuất phát")
            if start.hidden_passed:
                problems.append(f"{task_dir.name}: test ẩn đã qua sẵn, task vô nghĩa")
            solution = task_dir / "solution"
            if not solution.exists():
                problems.append(f"{task_dir.name}: thiếu lời giải tham chiếu")
                continue
            _copy_tree(solution, ws)
            solved = grade(name, ws)
            if not solved.passed:
                problems.append(
                    f"{task_dir.name}: lời giải tham chiếu vẫn trượt\n{solved.hidden_output}"
                )
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="evals.harness")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="liệt kê task")
    p_prepare = sub.add_parser("prepare", help="tạo workspace cho một task")
    p_prepare.add_argument("task")
    p_prepare.add_argument("--dest", required=True)
    p_grade = sub.add_parser("grade", help="chấm điểm một workspace")
    p_grade.add_argument("task")
    p_grade.add_argument("--workspace", required=True)
    p_self = sub.add_parser("selftest", help="kiểm tra các task hợp lệ")
    p_self.add_argument("tasks", nargs="*")
    args = parser.parse_args(argv)

    if args.cmd == "list":
        for name in list_tasks():
            meta = json.loads((TASKS_DIR / name / "meta.json").read_text(encoding="utf-8"))
            print(f"{name}  [{meta['type']}, {meta['difficulty']}]  {meta['title']}")
        return 0
    if args.cmd == "prepare":
        ws = prepare(args.task, args.dest)
        print(f"Workspace: {ws}\nĐề bài: {ws / 'TASK.md'}")
        return 0
    if args.cmd == "grade":
        result = grade(args.task, args.workspace)
        summary = {
            "task": result.task,
            "visible_passed": result.visible_passed,
            "hidden_passed": result.hidden_passed,
            "passed": result.passed,
        }
        print(json.dumps(summary, indent=2))
        if not result.passed:
            print(result.hidden_output[-800:], file=sys.stderr)
        return 0 if result.passed else 1
    problems = selftest(args.tasks or None)
    if problems:
        print("\n".join(problems))
        return 1
    print(f"OK: {len(args.tasks or list_tasks())} task hợp lệ")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
