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
        self.stats = stats
        self.condition = condition
        self.threshold = threshold

    def is_met(self, relic: Relic):
        if self.condition == Condition.MAIN:
            return relic.main_stat in self.stats
        elif self.condition == Condition.SUM:
            return sum(relic.sub_stats) >= self.threshold
        elif self.condition == Condition.ALL:
            return all(value >= self.threshold for value in relic.sub_stats)
        elif self.condition == Condition.ANY:
            return any(value >= self.threshold for value in relic.sub_stats)
        else:
            raise ValueError(f"Unknown condition: {self.condition}")
