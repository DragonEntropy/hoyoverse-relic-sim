import numpy as np
from collections import defaultdict


from core.rates import Genshin, HSR, ZZZ


class Relic:
    def __init__(self, game="hsr", slot=0, upgrade_count=5):
        self.upgrade_count = upgrade_count
        if game == "genshin":
            self.rates = Genshin()
        elif game == "hsr":
            self.rates = HSR()
        elif game == "zzz":
            self.rates = ZZZ()

        self.slot = slot
        if slot == 0:
            self.slot = np.random.randint(1, self.rates.total_slots + 1)

        self.create()
        self.level_up()

    def create(self):
        self.main_stat = np.random.choice(
            list(self.rates.main_weights[self.slot - 1].keys()),
            p=list(np.array(list(self.rates.main_weights[self.slot - 1].values())) / sum(self.rates.main_weights[self.slot - 1].values())),
            size=1,
            replace=False
        ).item()
        sub_stat_pool = self.rates.sub_weights.copy()
        sub_stat_pool.pop(self.main_stat, None)

        self.sub_stats = np.random.choice(
            list(sub_stat_pool.keys()),
            p=list(np.array(list(sub_stat_pool.values())) / sum(sub_stat_pool.values())),
            size=4,
            replace=False
        )
        self.extra_roll = np.random.rand() < self.rates.extra_roll_rate
        self.sub_stats_values = defaultdict(lambda: 0, {stat: 1 for stat in self.sub_stats})
        if not self.extra_roll:
            self.sub_stats_values[self.sub_stats[-1]] = 0

    def level_up(self):
        if not self.extra_roll and self.upgrade_count > 0:
            self.sub_stats_values[self.sub_stats[-1]] = 1
            self.upgrade_count -= 1

        upgraded_stats = np.random.choice(
            self.sub_stats,
            size=self.upgrade_count,
            replace=True
        )

        for stat in upgraded_stats:
            self.sub_stats_values[stat] += 1

    def __repr__(self) -> str:
        return f"Relic(slot={self.slot}, upgrades={self.upgrade_count}, main_stat={self.main_stat}, sub_stats={dict(self.sub_stats_values)})"
