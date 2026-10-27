from evals.harness import list_tasks, selftest


def test_there_are_at_least_five_tasks():
    assert len(list_tasks()) >= 5


def test_all_tasks_are_valid():
    problems = selftest()
    assert problems == [], "\n".join(problems)
