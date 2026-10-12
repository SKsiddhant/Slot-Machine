import builtins
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import slot_machine as sm  # noqa: E402


def test_importing_does_not_start_the_game():
    assert callable(sm.main)  # the old file ran main() at import time


def test_spin_shape_and_symbols():
    cols = sm.get_slot_machine_spin(sm.ROWS, sm.COLS, sm.symbol_count)
    assert len(cols) == sm.COLS and all(len(c) == sm.ROWS for c in cols)
    assert {s for c in cols for s in c} <= set(sm.symbol_count)


def test_no_symbol_exceeds_its_count_in_a_column():
    cols = sm.get_slot_machine_spin(sm.ROWS, sm.COLS, sm.symbol_count)
    for col in cols:
        for sym in set(col):
            assert col.count(sym) <= sm.symbol_count[sym]


def test_check_winnings():
    cols = [["A", "B"], ["A", "C"], ["A", "D"]]
    assert sm.check_winnings(cols, 2, 10, {"A": 5, "B": 1, "C": 1, "D": 1}) == (50, [1])
    assert sm.check_winnings(cols, 1, 10, {"A": 2}) == (20, [1])
    assert sm.check_winnings([["A"], ["B"]], 1, 10, {"A": 5, "B": 5}) == (0, [])


def feed(monkeypatch, answers):
    it = iter(answers)
    monkeypatch.setattr(builtins, "input", lambda *_: next(it))


def test_spin_reprompts_lines_when_balance_too_low(monkeypatch, capsys):
    # balance 2: 5 lines is unaffordable even at the minimum bet. The old code looped forever here.
    feed(monkeypatch, ["5", "2", "1"])
    monkeypatch.setattr(sm, "get_slot_machine_spin", lambda *a: [["A"] * 5 for _ in range(5)])
    result = sm.spin(2)
    assert "cannot afford 5" in capsys.readouterr().out
    assert result == 2 * 5 * 1 - 2  # 2 lines x $1, all lines win at 5x


def test_main_stops_when_broke(monkeypatch, capsys):
    feed(monkeypatch, ["1", "", "1", "1"])
    monkeypatch.setattr(sm, "get_slot_machine_spin", lambda *a: [["A", "B", "C", "D", "A"], ["B", "C", "D", "A", "B"]] * 2 + [["C"] * 5])
    sm.main()
    out = capsys.readouterr().out
    assert "out of money" in out and "You left with $0" in out


def test_deposit_rejects_bad_input(monkeypatch):
    feed(monkeypatch, ["abc", "0", "-5", "20"])
    assert sm.deposit() == 20
