import numpy as np
from collections import defaultdict
from collections.abc import Sequence


from core.rates import Genshin, HSR, ZZZ


class Relic:
    def __init__(
        self,
        game="hsr",
        slot=0,
        upgrade_count=5,
        *,
        fixed_main_stat: str | None = None,
        fixed_substats: Sequence[str] = (),
    ):
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

        self.fixed_main_stat = fixed_main_stat
        self.fixed_substats = tuple(fixed_substats)

        self.create()
        self.level_up()

    def create(self):
        main_weights = self.rates.main_weights[self.slot - 1]
        if self.fixed_main_stat:
            if self.fixed_main_stat not in main_weights:
                raise ValueError("fixed main stat is not available for this slot")
            self.main_stat = self.fixed_main_stat
        else:
            self.main_stat = np.random.choice(
                list(main_weights),
                p=list(np.array(list(main_weights.values())) / sum(main_weights.values())),
                size=1,
                replace=False,
            ).item()
        sub_stat_pool = self.rates.sub_weights.copy()
        sub_stat_pool.pop(self.main_stat, None)

        if len(set(self.fixed_substats)) != len(self.fixed_substats):
            raise ValueError("fixed substats must be unique")
        if len(self.fixed_substats) > 4 or any(stat not in sub_stat_pool for stat in self.fixed_substats):
            raise ValueError("fixed substats are not available for this relic")

        remaining_pool = {stat: weight for stat, weight in sub_stat_pool.items() if stat not in self.fixed_substats}
        if len(self.fixed_substats) == 4:
            random_substats = []
        else:
            random_substats = np.random.choice(
                list(remaining_pool),
                p=list(np.array(list(remaining_pool.values())) / sum(remaining_pool.values())),
                size=4 - len(self.fixed_substats),
                replace=False,
            )
        self.sub_stats = np.array([*self.fixed_substats, *random_substats])
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
