from core.relic import Relic


def main():
    trials = 10000
    relics = [Relic(game="hsr", slot=1, upgrade_count=5) for _ in range(trials)]
    print(sum("spd" in relic.sub_stats_values for relic in relics) / trials)
    relics.sort(key=lambda x: x.sub_stats_values["spd"], reverse=True)
    print(relics[0])


if __name__ == "__main__":
    main()
