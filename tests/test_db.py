from orchestrator.db import init_db


def test_events_table_accepts_event(tmp_path):
    conn = init_db(str(tmp_path / "events.db"))
    conn.execute(
        "INSERT INTO events (run_id, event_type, status) VALUES (?, ?, ?)",
        ("run-1", "start", "ok"),
    )
    conn.commit()
    row = conn.execute("SELECT run_id, event_type, status FROM events").fetchone()
    conn.close()
    assert row == ("run-1", "start", "ok")
