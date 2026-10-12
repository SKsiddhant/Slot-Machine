# Slot Machine

A console slot machine in Python (no dependencies).

```bash
python slot_machine.py
```

Deposit money, choose how many lines (1-5) to bet on and how much per line ($1-$100), then spin a 5x5 grid. A line pays `symbol_value x bet` when all five symbols on that row match.

## Known design caveat

All four symbols currently pay the same (`symbol_value` = 5 each) and a five-in-a-row match is rare, so the simulated return to player is about **2 cents per dollar wagered** (about 1.9% hit rate over 200,000 simulated spins). That makes the game practically unwinnable. Tune `symbol_count` / `symbol_value` in `slot_machine.py` (e.g. rarer symbols pay more, fewer columns or rows) to taste.

## Tests

```bash
pip install pytest && pytest
```
