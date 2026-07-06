from tqdm import tqdm

from core.relic import Relic
from core.stat_goal import StatGoal


def simulate(game, stat_goals, target):
    trials = 0
    successes = 0

    with tqdm(total=successes, desc=f"Simulating {game}") as bar:
        satisfies = [None] * 
        while successes < target:
            relic = Relic(game=game, upgrade_count=5)
            if all(goal.is_met(relic) for goal in stat_goals):
                successes += 1
                bar.update(1)
            trials += 1

    success_rate = successes / trials
    print(f"Game: {game},\t Trials: {trials},\t Successes: {successes}, Success Rate: {success_rate:.4%}")

    return success_rate


if __name__ == "__main__":
    games = ["genshin", "hsr", "zzz"]
    goals = {
        "genshin": [
            StatGoal(stats=["cr", "cd", "atk_p"], condition="sum", threshold=7),
            StatGoal(stats=["cr", "cd", "atk_p"], condition="all", threshold=1)
        ],
        "hsr": [
            StatGoal(stats=["cr", "cd", "atk_p"], condition="sum", threshold=7),
            StatGoal(stats=["cr", "cd", "atk_p"], condition="all", threshold=1)
        ],
        "zzz": [
            StatGoal(stats=["cr", "cd", "atk_p"], condition="sum", threshold=7),
            StatGoal(stats=["cr", "cd", "atk_p"], condition="all", threshold=1)
        ]
    }
    target = 1000
    simulate("genshin", goals, target)
