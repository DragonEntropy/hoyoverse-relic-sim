from collections.abc import Callable, Sequence

from core.relic import Relic
from core.stat_goal import Condition, StatGoal


def farm(
    game: str,
    stat_goals: Sequence[StatGoal],
    drops: int,
    *,
    slot: int = 0,
    progress_callback: Callable[[int, int], None] | None = None,
) -> tuple[list[tuple[int, Relic]], int]:
    """Farm a fixed number of relics and return qualifying drops, best first."""
    if drops < 1:
        raise ValueError("drops must be at least 1")

    qualifying_relics = []
    desired_stats = {
        stat
        for goal in stat_goals
        if goal.condition != Condition.MAIN
        for stat in goal.stats
    }
    for trial in range(1, drops + 1):
        relic = Relic(game=game, slot=slot, upgrade_count=5)
        if all(goal.is_met(relic) for goal in stat_goals):
            score = sum(relic.sub_stats_values.get(stat, 0) for stat in desired_stats)
            qualifying_relics.append((score, relic))
        if progress_callback and (trial == drops or trial % max(1, drops // 100) == 0):
            progress_callback(trial, drops)

    qualifying_relics.sort(key=lambda result: result[0], reverse=True)
    return qualifying_relics, drops


def farm_until_targets(
    game: str,
    relic_targets: dict[int, tuple[Sequence[StatGoal], int]],
    *,
    progress_callback: Callable[[int, int, int], None] | None = None,
) -> tuple[dict[int, dict[str, int]], int]:
    """Farm uniformly across slots until every slot-specific target is met."""
    if not relic_targets:
        raise ValueError("at least one relic target is required")
    if any(target < 1 for _, target in relic_targets.values()):
        raise ValueError("each target must be at least 1")

    results = {
        slot: {"target": target, "matches": 0, "completed_at_trial": 0}
        for slot, (_, target) in relic_targets.items()
    }
    completed_slots: set[int] = set()
    trials = 0
    while len(completed_slots) < len(relic_targets):
        trials += 1
        relic = Relic(game=game, slot=0, upgrade_count=5)
        if relic.slot in relic_targets and relic.slot not in completed_slots:
            goals, target = relic_targets[relic.slot]
            if all(goal.is_met(relic) for goal in goals):
                results[relic.slot]["matches"] += 1
                if results[relic.slot]["matches"] == target:
                    results[relic.slot]["completed_at_trial"] = trials
                    completed_slots.add(relic.slot)
        if progress_callback and (trials % 1_000 == 0 or len(completed_slots) == len(relic_targets)):
            progress_callback(trials, len(completed_slots), len(relic_targets))

    return results, trials
