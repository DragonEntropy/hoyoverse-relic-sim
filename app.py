import pandas as pd
import streamlit as st

from core.constants import STAT_ABBREVS
from core.rates import GAME_CLASSES
from core.stat_goal import Condition, StatGoal
from simulation import farm, farm_until_targets


st.set_page_config(page_title="Hoyoverse Artifact Odds Calculator", page_icon="D", layout="wide")
st.title("Hoyoverse Artifact / Relic Odds Calculator")

with st.sidebar:
    st.header("Simulation")
    game = st.selectbox("Game", list(GAME_CLASSES))
    mode = st.radio("Mode", ["Farm one slot", "Farm all slots"])

game_class = GAME_CLASSES[game]


def requirement_inputs(
    slot: int, prefix: str, *, include_fixed_stats: bool = False
) -> tuple[list[StatGoal], str | None, list[str]]:
    """Render one slot's criteria and return its corresponding goals."""
    main_stats = list(game_class.main_weights[slot - 1])
    selected_mains = st.multiselect(
        "Target main stats",
        main_stats,
        format_func=lambda stat: STAT_ABBREVS.get(stat, stat),
        key=f"{prefix}_mains",
        help="Leave empty to accept any main stat.",
    )

    substats = st.multiselect(
        "Target substats",
        list(game_class.sub_weights),
        format_func=lambda stat: STAT_ABBREVS.get(stat, stat),
        key=f"{prefix}_substats",
    )

    fixed_main = None
    fixed_substats: list[str] = []
    if include_fixed_stats:
        fixed_main = st.selectbox(
            "Fixed main stat",
            [None, *main_stats],
            format_func=lambda stat: "None" if stat is None else STAT_ABBREVS.get(stat, stat),
            key=f"{prefix}_fixed_main",
            help="Generate every simulated relic with this main stat.",
        )
        fixed_substats = st.multiselect(
            "Fixed substats",
            list(game_class.sub_weights),
            format_func=lambda stat: STAT_ABBREVS.get(stat, stat),
            key=f"{prefix}_fixed_substats",
            help="Generate every simulated relic with these substats.",
        )

    goals = []
    if selected_mains:
        goals.append(StatGoal(selected_mains, Condition.MAIN))
    if substats:
        condition_name = st.selectbox("Substat condition", ["Sum", "All", "Any"], key=f"{prefix}_condition")
        maximum_rolls = 6 // len(substats) if condition_name == "All" else 6
        threshold = st.number_input(
            "Minimum rolls",
            min_value=1,
            max_value=maximum_rolls,
            value=min(4, maximum_rolls),
            key=f"{prefix}_threshold_{condition_name}_{len(substats)}",
        )
        goals.append(StatGoal(substats, Condition[condition_name.upper()], int(threshold)))
    return goals, fixed_main, fixed_substats


if mode == "Farm one slot":
    st.caption("Farm a fixed number of relics, then inspect the best drops that meet your requirements.")
    with st.sidebar:
        drops = st.number_input("Relics to farm", min_value=1, max_value=1_000_000, value=10_000, step=100)
        top_k = st.number_input("Top qualifying relics to show", min_value=1, max_value=100, value=10)

    slot = st.selectbox("Slot", range(1, game_class.total_slots + 1), format_func=lambda value: f"Slot {value}")
    st.header("Relic Requirements")
    goals, fixed_main, fixed_substats = requirement_inputs(
        slot, f"single_{game}_{slot}", include_fixed_stats=True
    )

    if st.button("Farm relics", type="primary"):
        progress = st.progress(0)
        status = st.empty()

        def update_progress(completed: int, total: int) -> None:
            progress.progress(completed / total)
            status.write(f"Farming relic {completed:,} of {total:,}")

        qualifying_relics, trials = farm(
            game,
            goals,
            int(drops),
            slot=slot,
            fixed_main_stat=fixed_main,
            fixed_substats=fixed_substats,
            progress_callback=update_progress,
        )
        status.empty()
        st.success("Farming complete")
        first, second = st.columns(2)
        first.metric("Qualifying drop rate", f"{len(qualifying_relics) / trials:.4%}")
        second.metric("Relics simulated", f"{trials:,}")

        st.subheader(f"Top {min(int(top_k), len(qualifying_relics))} qualifying relics")
        if not qualifying_relics:
            st.info("No relics met every requirement in this farming run.")
        else:
            st.dataframe(
                pd.DataFrame(
                    [
                        {
                            "Rank": rank,
                            "Desired rolls": score,
                            "Main stat": STAT_ABBREVS.get(relic.main_stat, relic.main_stat),
                            "Substats": ", ".join(
                                f"{STAT_ABBREVS.get(stat, stat)} +{value}"
                                for stat, value in relic.sub_stats_values.items()
                            ),
                        }
                        for rank, (score, relic) in enumerate(qualifying_relics[: int(top_k)], start=1)
                    ]
                ),
                hide_index=True,
                use_container_width=True,
            )
else:
    st.caption("Each trial creates one uniformly random slot. Configure its requirements, then farm until every slot has reached the same target.")
    relic_targets = {}
    st.header("Per-slot targets")
    target = st.number_input("Target matching relics per slot", min_value=1, max_value=100_000, value=1)
    columns = st.columns(3)
    for index, slot in enumerate(range(1, game_class.total_slots + 1)):
        prefix = f"multi_{game}_{slot}"
        with columns[index % 3]:
            with st.expander(f"Slot {slot}"):
                enabled = st.checkbox("Farm this slot", value=True, key=f"{prefix}_enabled")
                goals, _, _ = requirement_inputs(slot, prefix)
                if enabled:
                    relic_targets[slot] = (goals, int(target))

    if st.button("Farm all targets", type="primary"):
        if not relic_targets:
            st.error("Enable at least one slot target.")
        else:
            progress = st.progress(0)
            status = st.empty()

            def update_progress(trials: int, completed: int, total: int) -> None:
                progress.progress(completed / total)
                status.write(f"Simulated {trials:,} relics; completed {completed} of {total} slot targets")

            results, total_trials = farm_until_targets(game, relic_targets, progress_callback=update_progress)
            status.empty()
            st.success("All slot targets met")
            st.metric("Total relics simulated", f"{total_trials:,}")
            st.subheader("Trials required per slot")
            st.dataframe(
                pd.DataFrame(
                    [
                        {
                            "Slot": slot,
                            "Target matching relics": result["target"],
                            "Matches found": result["matches"],
                            "Trial completed": result["completed_at_trial"],
                        }
                        for slot, result in results.items()
                    ]
                ),
                hide_index=True,
                use_container_width=True,
            )
