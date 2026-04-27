"""
E-commerce User Funnel & Cohort Analyzer
=========================================
A Streamlit application for analyzing user behavior through:
1. FUNNEL ANALYSIS - tracks how users move through purchase stages
   (browse -> add to cart -> checkout -> purchase) and identifies drop-offs
2. COHORT ANALYSIS - groups users by acquisition week and tracks
   their retention behavior over time

Author: Akshay Sarwade
GitHub: https://github.com/AkshaySarwade
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# ----------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Funnel & Cohort Analyzer",
    page_icon="📈",
    layout="wide"
)

# ----------------------------------------------------------------------
# DATA GENERATION (for sample data mode)
# ----------------------------------------------------------------------

def generate_sample_data(n_users=2000, seed=42):
    """
    Generate realistic e-commerce event data.
    Each user has a sign-up date and progresses through stages
    with realistic drop-off rates.
    """
    np.random.seed(seed)
    events = []

    # Spread sign-ups across 12 weeks
    base_date = datetime(2025, 1, 1)
    for user_id in range(1, n_users + 1):
        signup_week = np.random.randint(0, 12)
        signup_date = base_date + timedelta(weeks=signup_week,
                                            days=np.random.randint(0, 7))

        # Stage 1: Browse (everyone browses)
        events.append({
            'user_id': user_id,
            'event_name': 'browse',
            'event_date': signup_date
        })

        # Stage 2: Add to cart (60% drop-off after browse)
        if np.random.random() < 0.40:
            cart_date = signup_date + timedelta(hours=np.random.randint(1, 48))
            events.append({
                'user_id': user_id,
                'event_name': 'add_to_cart',
                'event_date': cart_date
            })

            # Stage 3: Checkout (50% of cart adds reach checkout)
            if np.random.random() < 0.50:
                checkout_date = cart_date + timedelta(
                    hours=np.random.randint(1, 24))
                events.append({
                    'user_id': user_id,
                    'event_name': 'checkout',
                    'event_date': checkout_date
                })

                # Stage 4: Purchase (70% of checkouts complete purchase)
                if np.random.random() < 0.70:
                    purchase_date = checkout_date + timedelta(
                        minutes=np.random.randint(5, 60))
                    events.append({
                        'user_id': user_id,
                        'event_name': 'purchase',
                        'event_date': purchase_date
                    })

                    # Repeat purchases (for cohort retention)
                    n_repeat = np.random.choice([0, 0, 0, 1, 2, 3],
                                                p=[0.5, 0.1, 0.1, 0.15, 0.1, 0.05])
                    for _ in range(n_repeat):
                        repeat_date = purchase_date + timedelta(
                            weeks=np.random.randint(1, 12))
                        events.append({
                            'user_id': user_id,
                            'event_name': 'purchase',
                            'event_date': repeat_date
                        })

    df = pd.DataFrame(events)
    df['event_date'] = pd.to_datetime(df['event_date'])
    return df.sort_values(['user_id', 'event_date']).reset_index(drop=True)


# ----------------------------------------------------------------------
# FUNNEL ANALYSIS
# ----------------------------------------------------------------------

def calculate_funnel(df, stages):
    """
    For each stage in order, count unique users who reached it.
    Calculate stage-to-stage and overall conversion.
    """
    funnel_data = []
    previous_users = None

    for i, stage in enumerate(stages):
        users_at_stage = set(df[df['event_name'] == stage]['user_id'].unique())

        if i == 0:
            users_continuing = users_at_stage
        else:
            users_continuing = users_at_stage & previous_users

        count = len(users_continuing)

        if i == 0:
            stage_conversion = 100.0
            overall_conversion = 100.0
            top_count = count
        else:
            stage_conversion = (count / len(previous_users) * 100
                                if len(previous_users) > 0 else 0)
            overall_conversion = (count / top_count * 100
                                  if top_count > 0 else 0)

        funnel_data.append({
            'stage': stage,
            'users': count,
            'stage_conversion_pct': round(stage_conversion, 2),
            'overall_conversion_pct': round(overall_conversion, 2),
            'drop_off_pct': round(100 - stage_conversion, 2) if i > 0 else 0
        })

        previous_users = users_continuing

    return pd.DataFrame(funnel_data)


# ----------------------------------------------------------------------
# COHORT ANALYSIS
# ----------------------------------------------------------------------

def build_cohort_table(df, event_name='purchase'):
    """
    Build a retention cohort table.
    Rows: cohort week (when user first appeared)
    Cols: weeks since acquisition
    Values: % of users from that cohort still active
    """
    # Filter to specific event (e.g. purchases) for retention measurement
    event_df = df[df['event_name'] == event_name].copy()

    if event_df.empty:
        return None, None

    # Each user's cohort = week of FIRST event (any kind) - acquisition
    user_first = df.groupby('user_id')['event_date'].min().reset_index()
    user_first['cohort_week'] = (
        user_first['event_date']
        .dt.to_period('W').dt.start_time
    )

    # Add cohort to event data
    event_df = event_df.merge(
        user_first[['user_id', 'cohort_week']], on='user_id'
    )
    event_df['event_week'] = (
        event_df['event_date'].dt.to_period('W').dt.start_time
    )
    event_df['weeks_since_acquisition'] = (
        (event_df['event_week'] - event_df['cohort_week']).dt.days // 7
    )

    # Cohort sizes
    cohort_sizes = user_first.groupby('cohort_week')['user_id'].nunique()

    # Pivot: cohort vs weeks since
    cohort_table = (
        event_df.groupby(['cohort_week', 'weeks_since_acquisition'])
        ['user_id'].nunique().reset_index()
    )
    cohort_pivot = cohort_table.pivot(
        index='cohort_week',
        columns='weeks_since_acquisition',
        values='user_id'
    )

    # Convert to retention % of cohort size
    retention = cohort_pivot.divide(cohort_sizes, axis=0) * 100

    # Format index for readability
    retention.index = retention.index.strftime('%Y-%m-%d')
    return retention.round(1), cohort_sizes


# ----------------------------------------------------------------------
# UI
# ----------------------------------------------------------------------

st.title("📈 E-commerce Funnel & Cohort Analyzer")
st.markdown(
    "Analyze user behavior end-to-end. **Funnel analysis** shows where "
    "users drop off in your purchase flow; **cohort analysis** shows how "
    "different groups of users retain over time."
)

# --- Sidebar ---
st.sidebar.header("Configuration")
analysis_mode = st.sidebar.radio(
    "Analysis Mode",
    ["Funnel Analysis", "Cohort Analysis", "Both"]
)

# --- Data input ---
st.header("1. Load Your Data")
input_method = st.radio(
    "Data source",
    ("Use sample data", "Upload CSV"),
    horizontal=True
)

df = None
if input_method == "Upload CSV":
    st.markdown(
        "**Required columns:** `user_id`, `event_name`, `event_date`"
    )
    uploaded = st.file_uploader("Upload event data CSV", type="csv")
    if uploaded:
        df = pd.read_csv(uploaded)
        df['event_date'] = pd.to_datetime(df['event_date'])
else:
    df = generate_sample_data(n_users=2000)
    st.info(
        "Using simulated e-commerce data: 2,000 users moving through "
        "browse → add to cart → checkout → purchase, with realistic "
        "drop-off rates and repeat-purchase behavior over 12 weeks."
    )

if df is not None:
    st.dataframe(df.head(15), use_container_width=True)
    st.caption(f"Total events: {len(df):,} | Unique users: "
               f"{df['user_id'].nunique():,}")

    # --- FUNNEL ANALYSIS ---
    if analysis_mode in ["Funnel Analysis", "Both"]:
        st.header("2. 🪜 Funnel Analysis")
        st.markdown("How users progress through your purchase flow:")

        # Detect funnel stages
        unique_events = df['event_name'].unique().tolist()
        default_stages = [s for s in
                          ['browse', 'add_to_cart', 'checkout', 'purchase']
                          if s in unique_events]
        stages = st.multiselect(
            "Funnel stages (in order)",
            options=unique_events,
            default=default_stages
        )

        if len(stages) >= 2:
            funnel_df = calculate_funnel(df, stages)

            # Metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Users at top of funnel",
                        f"{funnel_df.iloc[0]['users']:,}")
            col2.metric("Users at bottom",
                        f"{funnel_df.iloc[-1]['users']:,}")
            col3.metric("Overall conversion",
                        f"{funnel_df.iloc[-1]['overall_conversion_pct']:.2f}%")

            # Funnel table
            st.dataframe(funnel_df, use_container_width=True)

            # Funnel chart
            fig, ax = plt.subplots(figsize=(10, 5))
            colors_list = sns.color_palette("Blues_r", len(funnel_df))
            ax.barh(funnel_df['stage'], funnel_df['users'],
                    color=colors_list, edgecolor='white')
            for i, row in funnel_df.iterrows():
                ax.text(row['users'] + max(funnel_df['users']) * 0.01, i,
                        f"  {row['users']:,} ({row['overall_conversion_pct']:.1f}%)",
                        va='center', fontweight='bold')
            ax.set_xlabel("Number of Users")
            ax.set_title("Purchase Funnel")
            ax.invert_yaxis()
            st.pyplot(fig)

            # Biggest drop-off insight
            funnel_with_drops = funnel_df.iloc[1:].copy()
            if not funnel_with_drops.empty:
                idx = funnel_with_drops['drop_off_pct'].idxmax()
                biggest_drop_stage = funnel_df.loc[idx, 'stage']
                biggest_drop_pct = funnel_df.loc[idx, 'drop_off_pct']
                prev_stage = funnel_df.loc[idx - 1, 'stage']
                st.warning(
                    f"**Biggest drop-off:** {biggest_drop_pct:.1f}% of users "
                    f"are lost between **{prev_stage}** and **{biggest_drop_stage}**. "
                    f"This is where to focus product improvements."
                )

    # --- COHORT ANALYSIS ---
    if analysis_mode in ["Cohort Analysis", "Both"]:
        st.header("3. 📊 Cohort Retention Analysis")
        st.markdown(
            "Each row is a cohort (users acquired in that week). Each column "
            "shows what % of that cohort was still active N weeks later."
        )

        cohort_event = st.selectbox(
            "Retention event",
            options=df['event_name'].unique(),
            index=list(df['event_name'].unique()).index('purchase')
                  if 'purchase' in df['event_name'].unique() else 0
        )

        retention, cohort_sizes = build_cohort_table(df, cohort_event)

        if retention is None or retention.empty:
            st.warning(f"No '{cohort_event}' events found.")
        else:
            # Cohort size sidebar
            st.markdown("**Cohort sizes:**")
            cohort_size_df = pd.DataFrame({
                'cohort_week': cohort_sizes.index.strftime('%Y-%m-%d'),
                'users_acquired': cohort_sizes.values
            })
            st.dataframe(cohort_size_df, use_container_width=True)

            # Cohort heatmap
            fig, ax = plt.subplots(
                figsize=(min(14, 2 + retention.shape[1]),
                         max(4, retention.shape[0] * 0.4))
            )
            sns.heatmap(
                retention, annot=True, fmt=".1f", cmap="Blues",
                cbar_kws={'label': 'Retention %'}, ax=ax
            )
            ax.set_title(f"Cohort Retention Heatmap ({cohort_event})")
            ax.set_xlabel("Weeks since acquisition")
            ax.set_ylabel("Cohort week")
            st.pyplot(fig)

            # Average retention curve
            st.markdown("**Average retention curve across all cohorts:**")
            avg_retention = retention.mean(axis=0).reset_index()
            avg_retention.columns = ['weeks_since', 'avg_retention_pct']
            fig2, ax2 = plt.subplots(figsize=(10, 4))
            ax2.plot(avg_retention['weeks_since'],
                     avg_retention['avg_retention_pct'],
                     marker='o', linewidth=2, color='#2E75B6')
            ax2.fill_between(avg_retention['weeks_since'], 0,
                             avg_retention['avg_retention_pct'],
                             alpha=0.2, color='#2E75B6')
            ax2.set_xlabel("Weeks since acquisition")
            ax2.set_ylabel("Average retention %")
            ax2.set_title("Average Retention Curve")
            ax2.grid(alpha=0.3)
            st.pyplot(fig2)

    with st.expander("📚 What does this mean?"):
        st.markdown("""
        - **Funnel analysis** identifies *where* in the user journey people drop off. The biggest drop-off is usually the highest-leverage place to improve.
        - **Cohort analysis** answers *whether retention is improving over time*. If cohorts acquired this month retain better than cohorts from three months ago, your product is getting stickier.
        - Together, these are the foundational tools of product analytics — they answer "where do we lose users?" and "are we keeping the ones we get?"
        """)
