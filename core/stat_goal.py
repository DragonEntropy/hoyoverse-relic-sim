from enum import Enum

from core.relic import Relic


class Condition(Enum):
    NONE = 0
    MAIN = 1
    SUM = 2
    ALL = 3
    ANY = 4


class StatGoal:
    def __init__(self, stats: list[str], condition: Condition, threshold: int = 0):
        self.stats = [stats] if isinstance(stats, str) else list(stats)
        self.condition = Condition[condition.upper()] if isinstance(condition, str) else condition
        self.threshold = threshold

    def is_met(self, relic: Relic):
        if self.condition == Condition.MAIN:
            return relic.main_stat in self.stats
        elif self.condition == Condition.SUM:
            return sum(relic.sub_stats_values.get(stat, 0) for stat in self.stats) >= self.threshold
        elif self.condition == Condition.ALL:
            return bool(self.stats) and all(relic.sub_stats_values.get(stat, 0) >= self.threshold for stat in self.stats)
        elif self.condition == Condition.ANY:
            return any(relic.sub_stats_values.get(stat, 0) >= self.threshold for stat in self.stats)
        else:
            raise ValueError(f"Unknown condition: {self.condition}")
