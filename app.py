import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from core.rates import Genshin, HSR, ZZZ, GAME_CLASSES
from core.constants import STAT_ABBREVS
from simulation import simulate
from core.stat_goal import StatGoal, Condition

# ======================================================
# Replace these imports with your project modules
# ======================================================
# from relic import Relic
# from stat_goal import StatGoal
# from simulate import simulate

games = ["genshin", "hsr", "zzz"]

st.set_page_config(
    page_title="Hoyoverse Artifact Odds Calculator",
    page_icon="🎲",
    layout="wide"
)


st.title("🎲 Hoyoverse Artifact / Relic Odds Calculator")

with st.sidebar:
    st.header("Simulation")
    game = st.selectbox("Game", list(games))
    mode = st.radio("Mode", ["Farm until complete", "Best after N drops"])
    mc_runs = st.number_input("Monte Carlo repetitions", 100, 1000000, 10000, 100)
    target = st.number_input("Target successes", 1, 100000, 1000)
    drops = st.number_input("Drops (Best after N)", 1, 1000000, 10000)

game_class = game_classes[game]
piece_count = game_class.total_slots
subs = game_class.sub_weights.keys()

stat_goals = []

st.header("Build Configuration")

for i in range(piece_count):
    with st.expander(str(i), expanded=False):

        # Add main stat condition
        mains = game_class.main_weights[i]
        main = st.selectbox(
            "Main Stat",
            map(lambda stat: STAT_ABBREVS[stat], mains),
            key=f"{i}_main"
        )
        stat_goals.append(StatGoal(main, Condition.MAIN))

        # Add sub stats condition
        subs = st.multiselect(
            "Desired Substats",
            map(lambda stat: STAT_ABBREVS[stat], subs),
            key=f"{i}_subs"
        )

        condition = st.selectbox(
            "Condition",
            ["sum", "all", "any"],
            key=f"{i}_cond"
        )

        threshold = st.number_input(
            "Threshold",
            1,
            20,
            7,
            key=f"{i}_thresh"
        )

        enabled = st.checkbox(
            "Include Piece",
            True,
            key=f"{i}_enabled"
        )

        stat_goals.append(StatGoal(subs, condition, threshold))

run = st.button("Run Simulation", type="primary")
print(stat_goals)

if run:
    progress = st.progress(0)
    status = st.empty()

    success_rate = simulate(game, stat_goals, target)

    st.success("Simulation complete")
    st.metric(
        "Success Rate",
        f"{success_rate:.4%}"
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Success Rate", f"{success_rate:.3%}")
    # c2.metric("Average Trials", f"{avg_trials:,}")
    # c3.metric("Median Trials", f"{median:,}")

    st.subheader("Piece Configuration")

    df = pd.DataFrame(stat_goals)
    st.dataframe(df, use_container_width=True)

    st.subheader("Example Distribution")

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist([650, 700, 720, 740, 760, 780, 820, 900, 950, 1000], bins=8)
    ax.set_xlabel("Trials")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    st.subheader("Integration")

    st.info("""
Replace the placeholder simulation section with your own code.

Typical workflow:

1. Convert each config dict into your PieceGoal / StatGoal objects.
2. Call your simulator.
3. Update the progress bar during execution.
4. Display the returned statistics and distributions.
""")
