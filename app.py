import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Nassau Candy | Route Intelligence",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM DESIGN
# ============================================================

st.markdown("""
<style>
    :root {
        --bg: #100d16;
        --bg2: #15111d;
        --panel: #1d1726;
        --panel2: #241c2f;
        --ink: #f7f3fa;
        --muted: #b8adbf;
        --plum: #7b3f91;
        --berry: #d34b88;
        --pink: #ff5c78;
        --line: #3b2d48;
        --soft: #2a2134;
    }

    .stApp {
        background:
            radial-gradient(circle at 90% 0%, rgba(211,75,136,.14), transparent 24%),
            radial-gradient(circle at 8% 18%, rgba(123,63,145,.14), transparent 24%),
            linear-gradient(180deg, var(--bg) 0%, var(--bg2) 55%, #0d0b12 100%);
        color: var(--ink);
    }

    /* Remove Streamlit's top chrome/black strip */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    #MainMenu, footer { visibility: hidden; }

    [data-testid="stAppViewContainer"] > .main {
        padding-top: 0 !important;
    }

    .block-container {
        padding-top: 1.1rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    /* Global readable typography */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4,
    .stApp p, .stApp label, .stApp li,
    .stApp [data-testid="stCaptionContainer"],
    .stApp [data-testid="stMarkdownContainer"] {
        color: var(--ink) !important;
    }

    .stApp [data-testid="stCaptionContainer"] {
        color: var(--muted) !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1c1224 0%, #25152f 100%) !important;
        border-right: 1px solid #3a2945;
    }
    [data-testid="stSidebar"] * { color: #f7f3fa; }
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 { color: #ffffff !important; }

    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stDateInput label,
    [data-testid="stSidebar"] .stSlider label {
        color: #f8f1fa !important;
        font-weight: 800 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: #0f0d14 !important;
        border: 1px solid #4a3857 !important;
        color: #ffffff !important;
        border-radius: 10px !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] span {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] input {
        background: #0f0d14 !important;
        color: #ffffff !important;
        border-color: #4a3857 !important;
    }
    [data-testid="stSidebar"] [data-testid="stDateInput"] > div > div {
        background: #0f0d14 !important;
        border-color: #4a3857 !important;
    }
    [data-testid="stSidebar"] [data-testid="stSlider"] {
        padding-top: .35rem;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: #1b1622;
        padding: 5px;
        border-radius: 15px;
        border: 1px solid #3a2b46;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 14px;
        font-weight: 800;
        color: #c9bfce !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: #33203d !important;
        color: #ffffff !important;
        box-shadow: 0 2px 10px rgba(0,0,0,.25);
    }

    /* Hero */
    .hero {
        position: relative;
        overflow: hidden;
        background: linear-gradient(120deg, #351646 0%, #653276 52%, #9f3c70 100%);
        border: 1px solid #8d4a9a;
        border-radius: 26px;
        padding: 30px 36px 32px;
        color: #ffffff;
        margin-bottom: 22px;
        box-shadow: 0 18px 45px rgba(0,0,0,.32);
    }
    .hero:after {
        content: "🍬";
        position: absolute;
        right: 48px;
        top: 12px;
        font-size: 6.5rem;
        opacity: .14;
        transform: rotate(-12deg);
    }
    .hero * { color: #ffffff !important; }
    .hero-kicker { font-size: .76rem; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; opacity: .82; margin-bottom: 8px; }
    .hero-title { font-size: 2.35rem; font-weight: 900; line-height: 1.05; margin: 0; }
    .hero-subtitle { font-size: 1rem; opacity: .92; margin-top: 10px; max-width: 980px; line-height: 1.5; }
    .hero-badge { display: inline-block; margin-top: 17px; padding: 7px 13px; border-radius: 999px; background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.25); font-size: .8rem; }

    /* KPI cards */
    .kpi-card {
        background: linear-gradient(180deg, #241b2e 0%, #1d1726 100%);
        border: 1px solid #44324f;
        border-top: 4px solid var(--berry);
        border-radius: 18px;
        padding: 16px 17px;
        min-height: 116px;
        box-shadow: 0 9px 25px rgba(0,0,0,.22);
    }
    .kpi-label { color: #c6bacb !important; font-size: .75rem; font-weight: 850; text-transform: uppercase; letter-spacing: .055em; }
    .kpi-value { color: #ffffff !important; font-size: 1.45rem; font-weight: 900; margin-top: 8px; line-height: 1.2; }
    .kpi-sub { color: #d58bb0 !important; font-size: .74rem; margin-top: 4px; }

    /* Section headings */
    .section-title { color: #ffffff !important; font-size: 1.35rem; font-weight: 900; margin-top: .35rem; }
    .section-note { color: #b8adbf !important; margin-bottom: .8rem; }

    /* Tables */
    [data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid #46344f;
        box-shadow: 0 8px 22px rgba(0,0,0,.22);
        background: #17131c;
    }

    /* Expanders */
    [data-testid="stExpander"] {
        border: 1px solid #46344f;
        border-radius: 13px;
        background: #1b1622;
    }
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary p {
        color: #ffffff !important;
    }

    .stButton > button { border-radius: 10px; font-weight: 800; }
    hr { border-color: #3a2c45 !important; }

    /* Native selectboxes in main content */
    [data-baseweb="select"] > div {
        background: #1b1622 !important;
        border-color: #46344f !important;
        color: #ffffff !important;
        border-radius: 10px !important;
    }
    [data-baseweb="select"] span { color: #ffffff !important; }

    /* Slider */
    [data-testid="stSlider"] label { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# LOAD DATA
# ============================================================

file_path = "Nassau Candy Distributor.csv"
df = pd.read_csv(file_path)
records_loaded = len(df)

# ============================================================
# DATA CLEANING & VALIDATION
# ============================================================

df["Order Date"] = pd.to_datetime(
    df["Order Date"], format="%d-%m-%Y", errors="coerce"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"], format="%d-%m-%Y", errors="coerce"
)

df["Shipping Lead Time (days)"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

missing_order_dates = df["Order Date"].isna().sum()
missing_ship_dates = df["Ship Date"].isna().sum()

invalid_lead_times = (
    df["Shipping Lead Time (days)"].isna()
    | (df["Shipping Lead Time (days)"] < 0)
)

invalid_lead_time_count = invalid_lead_times.sum()
df = df[~invalid_lead_times].copy()

geographic_columns = [
    "Country/Region", "City", "State/Province", "Region"
]

for column in geographic_columns:
    df[column] = df[column].astype(str).str.strip()

# ============================================================
# FEATURE ENGINEERING
# ============================================================

factory_mapping = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Kazookles": "The Other Factory"
}

df["Factory"] = df["Product Name"].map(factory_mapping)
df["Route Region"] = df["Factory"] + " → " + df["Region"]
df["Route State"] = df["Factory"] + " → " + df["State/Province"]

# ============================================================
# SIDEBAR FILTERS
# ============================================================

ship_mode_order = [
    "Same Day", "First Class", "Second Class", "Standard Class"
]

st.sidebar.markdown("## 🍬 Route Controls")
st.sidebar.caption("Use the controls below to explore the shipment network.")

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

st.sidebar.caption(
    f"Available dates: {min_date.strftime('%d/%m/%Y')} → "
    f"{max_date.strftime('%d/%m/%Y')}"
)

date_range = st.sidebar.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    format="DD/MM/YYYY",
    help="Select the starting and ending order dates.",
    key="order_date_range_v3"
)

region_options = ["All Regions"] + sorted(
    df["Region"].dropna().unique().tolist()
)

selected_region = st.sidebar.selectbox(
    "Region", region_options, index=0, key="region_filter_v3"
)

if selected_region == "All Regions":
    state_options = ["All States"] + sorted(
        df["State/Province"].dropna().unique().tolist()
    )
else:
    state_options = ["All States"] + sorted(
        df.loc[
            df["Region"] == selected_region,
            "State/Province"
        ].dropna().unique().tolist()
    )

selected_state = st.sidebar.selectbox(
    "State / Province", state_options, index=0, key="state_filter_v3"
)

ship_mode_options = ["All Ship Modes"] + ship_mode_order

selected_ship_mode = st.sidebar.selectbox(
    "Ship Mode",
    ship_mode_options,
    index=0,
    key="ship_mode_filter_v3"
)

min_lead_time = int(df["Shipping Lead Time (days)"].min())
max_lead_time = int(df["Shipping Lead Time (days)"].max())

lead_time_threshold = st.sidebar.slider(
    "Lead-Time Threshold (days)",
    min_value=min_lead_time,
    max_value=max_lead_time,
    value=int(df["Shipping Lead Time (days)"].median()),
    step=1,
    help="Used to identify shipments whose recorded lead time exceeds the selected threshold."
)

# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df["Order Date"].dt.date >= start_date)
        & (filtered_df["Order Date"].dt.date <= end_date)
    ]

if selected_region != "All Regions":
    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]

if selected_state != "All States":
    filtered_df = filtered_df[
        filtered_df["State/Province"] == selected_state
    ]

if selected_ship_mode != "All Ship Modes":
    filtered_df = filtered_df[
        filtered_df["Ship Mode"] == selected_ship_mode
    ]

st.sidebar.divider()
st.sidebar.metric("Shipments in Current View", f"{len(filtered_df):,}")
st.sidebar.caption(f"of {len(df):,} valid shipments")

if filtered_df.empty:
    st.warning(
        "No shipments match the selected filters. Please adjust the filters."
    )
    st.stop()

# ============================================================
# AGGREGATIONS
# ============================================================

route_region_summary = (
    filtered_df.groupby(["Factory", "Region"], dropna=False)
    .agg(
        Total_Shipments=("Shipping Lead Time (days)", "count"),
        Average_Lead_Time=("Shipping Lead Time (days)", "mean"),
        Lead_Time_Variability=("Shipping Lead Time (days)", "std")
    )
    .reset_index()
)

route_state_summary = (
    filtered_df.groupby(["Factory", "State/Province"], dropna=False)
    .agg(
        Total_Shipments=("Shipping Lead Time (days)", "count"),
        Average_Lead_Time=("Shipping Lead Time (days)", "mean"),
        Lead_Time_Variability=("Shipping Lead Time (days)", "std")
    )
    .reset_index()
)

route_region_summary["Lead_Time_Variability"] = (
    route_region_summary["Lead_Time_Variability"].fillna(0)
)

route_state_summary["Lead_Time_Variability"] = (
    route_state_summary["Lead_Time_Variability"].fillna(0)
)

fastest_route_time = route_state_summary["Average_Lead_Time"].min()
slowest_route_time = route_state_summary["Average_Lead_Time"].max()

if slowest_route_time == fastest_route_time:
    route_state_summary["Route_Efficiency_Score"] = 100.0
else:
    route_state_summary["Route_Efficiency_Score"] = (
        (
            slowest_route_time
            - route_state_summary["Average_Lead_Time"]
        )
        / (slowest_route_time - fastest_route_time)
        * 100
    )

route_state_summary["Route_Efficiency_Score"] = (
    route_state_summary["Route_Efficiency_Score"].round(2)
)

route_region_summary["Route"] = (
    route_region_summary["Factory"]
    + " → "
    + route_region_summary["Region"]
)

route_state_summary["Route"] = (
    route_state_summary["Factory"]
    + " → "
    + route_state_summary["State/Province"]
)

# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">
    <div class="hero-kicker">Nassau Candy Distributor • Logistics Intelligence</div>
    <div class="hero-title">🍬 Route Intelligence Control Center</div>
    <div class="hero-subtitle">
        Explore factory-to-customer shipping performance, geographic bottlenecks,
        route efficiency and ship-mode behavior through one interactive dashboard.
    </div>
    <div class="hero-badge">Interactive analysis • Recorded shipment lead time</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# EXECUTIVE KPI STRIP
# ============================================================

avg_lead = filtered_df["Shipping Lead Time (days)"].mean()
unique_orders = filtered_df["Order ID"].nunique()
unique_customers = filtered_df["Customer ID"].nunique()

best_route = route_state_summary.loc[
    route_state_summary["Average_Lead_Time"].idxmin(), "Route"
]

worst_route = route_state_summary.loc[
    route_state_summary["Average_Lead_Time"].idxmax(), "Route"
]

kpis = st.columns(5)

kpi_data = [
    ("📦", "Shipments", f"{len(filtered_df):,}", "Current filtered view"),
    ("🧾", "Orders", f"{unique_orders:,}", "Unique order IDs"),
    ("⏱️", "Avg Lead Time", f"{avg_lead:,.1f} days", "Recorded lead time"),
    ("🏆", "Fastest Route", best_route, "Lowest route average"),
    ("⚠️", "Slowest Route", worst_route, "Highest route average")
]

for col, (icon, label, value, sub) in zip(kpis, kpi_data):
    with col:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{icon} {label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-sub">{sub}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.write("")

# ============================================================
# SHARED GEOGRAPHIC SUMMARIES
# ============================================================

region_summary = (
    filtered_df.groupby("Region")
    .agg(
        Total_Shipments=("Shipping Lead Time (days)", "count"),
        Average_Lead_Time=("Shipping Lead Time (days)", "mean"),
        Lead_Time_Variability=("Shipping Lead Time (days)", "std")
    )
    .reset_index()
)

region_summary["Lead_Time_Variability"] = (
    region_summary["Lead_Time_Variability"].fillna(0)
)

state_summary = (
    filtered_df.groupby("State/Province")
    .agg(
        Total_Shipments=("Shipping Lead Time (days)", "count"),
        Average_Lead_Time=("Shipping Lead Time (days)", "mean"),
        Lead_Time_Variability=("Shipping Lead Time (days)", "std")
    )
    .reset_index()
)

state_summary["Lead_Time_Variability"] = (
    state_summary["Lead_Time_Variability"].fillna(0)
)

# ============================================================
# INTERACTIVE ANALYSIS TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🧭 Route Intelligence",
    "🗺️ Geographic View",
    "🚚 Ship Modes",
    "🔎 Route Explorer",
    "ℹ️ Data & Methodology"
])

# ============================================================
# TAB 1 — ROUTE INTELLIGENCE
# ============================================================

with tab1:
    st.markdown('<div class="section-title">Route Intelligence</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-note">Benchmark factory-to-region and factory-to-state performance.</div>',
        unsafe_allow_html=True
    )

    with st.expander("📋 View factory-to-region route table", expanded=False):
        st.dataframe(
            route_region_summary[
                ["Route", "Total_Shipments", "Average_Lead_Time", "Lead_Time_Variability"]
            ]
            .sort_values("Average_Lead_Time")
            .rename(columns={
                "Total_Shipments": "Total Shipments",
                "Average_Lead_Time": "Average Lead Time (days)",
                "Lead_Time_Variability": "Lead-Time Variability (days)"
            })
            .style.format({
                "Total Shipments": "{:,.0f}",
                "Average Lead Time (days)": "{:,.1f}",
                "Lead-Time Variability (days)": "{:,.1f}"
            }),
            width="stretch",
            hide_index=True
        )

    with st.expander("📋 View factory-to-state route table + efficiency score", expanded=False):
        st.dataframe(
            route_state_summary[
                ["Route", "Total_Shipments", "Average_Lead_Time",
                 "Lead_Time_Variability", "Route_Efficiency_Score"]
            ]
            .sort_values("Average_Lead_Time")
            .rename(columns={
                "Total_Shipments": "Total Shipments",
                "Average_Lead_Time": "Average Lead Time (days)",
                "Lead_Time_Variability": "Lead-Time Variability (days)",
                "Route_Efficiency_Score": "Route Efficiency Score"
            })
            .style.format({
                "Total Shipments": "{:,.0f}",
                "Average Lead Time (days)": "{:,.1f}",
                "Lead-Time Variability (days)": "{:,.1f}",
                "Route Efficiency Score": "{:.2f}"
            }),
            width="stretch",
            hide_index=True
        )

    st.divider()

    ranked_routes = route_state_summary.sort_values(
        "Average_Lead_Time", ascending=True
    ).copy()

    top_10_routes = ranked_routes.head(10).copy()
    bottom_10_routes = ranked_routes.tail(10).sort_values(
        "Average_Lead_Time", ascending=False
    ).copy()

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("🏆 Top 10 Most Efficient")
        st.dataframe(
            top_10_routes[
                ["Route", "Total_Shipments", "Average_Lead_Time",
                 "Lead_Time_Variability", "Route_Efficiency_Score"]
            ]
            .rename(columns={
                "Total_Shipments": "Total Shipments",
                "Average_Lead_Time": "Average Lead Time (days)",
                "Lead_Time_Variability": "Lead-Time Variability (days)",
                "Route_Efficiency_Score": "Route Efficiency Score"
            })
            .style.format({
                "Total Shipments": "{:,.0f}",
                "Average Lead Time (days)": "{:,.1f}",
                "Lead-Time Variability (days)": "{:,.1f}",
                "Route Efficiency Score": "{:.2f}"
            }),
            width="stretch",
            hide_index=True
        )

    with c2:
        st.subheader("⚠️ Bottom 10 Least Efficient")
        st.dataframe(
            bottom_10_routes[
                ["Route", "Total_Shipments", "Average_Lead_Time",
                 "Lead_Time_Variability", "Route_Efficiency_Score"]
            ]
            .rename(columns={
                "Total_Shipments": "Total Shipments",
                "Average_Lead_Time": "Average Lead Time (days)",
                "Lead_Time_Variability": "Lead-Time Variability (days)",
                "Route_Efficiency_Score": "Route Efficiency Score"
            })
            .style.format({
                "Total Shipments": "{:,.0f}",
                "Average Lead Time (days)": "{:,.1f}",
                "Lead-Time Variability (days)": "{:,.1f}",
                "Route Efficiency Score": "{:.2f}"
            }),
            width="stretch",
            hide_index=True
        )

    st.subheader("Route Performance Distribution")
    st.caption("Use the controls to focus the chart on the routes you want to compare.")

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        chart_factories = ["All Factories"] + sorted(route_state_summary["Factory"].dropna().unique().tolist())
        selected_chart_factory = st.selectbox("Factory", chart_factories, key="route_chart_factory")
    with fc2:
        state_base = route_state_summary.copy()
        if selected_chart_factory != "All Factories":
            state_base = state_base[state_base["Factory"] == selected_chart_factory]
        chart_states = ["All States"] + sorted(state_base["State/Province"].dropna().unique().tolist())
        selected_chart_state = st.selectbox("Customer State / Province", chart_states, key="route_chart_state")
    with fc3:
        chart_display = st.selectbox("Routes to Display", [10, 20, 30, "All"], index=1, key="route_chart_display")

    route_chart = route_state_summary.copy()
    if selected_chart_factory != "All Factories":
        route_chart = route_chart[route_chart["Factory"] == selected_chart_factory]
    if selected_chart_state != "All States":
        route_chart = route_chart[route_chart["State/Province"] == selected_chart_state]
    route_chart = route_chart.sort_values("Average_Lead_Time")
    if chart_display != "All":
        route_chart = route_chart.head(chart_display)

    fig_routes = px.bar(
        route_chart,
        x="Average_Lead_Time",
        y="Route",
        orientation="h",
        color="Route_Efficiency_Score",
        hover_data=[
            "Total_Shipments",
            "Lead_Time_Variability",
            "Route_Efficiency_Score"
        ],
        labels={
            "Average_Lead_Time": "Average Lead Time (days)",
            "Route": "Factory → Customer State",
            "Route_Efficiency_Score": "Efficiency Score"
        },
        title="Factory-to-State Route Performance"
    )
    fig_routes.update_layout(
        height=max(520, min(760, 110 + len(route_chart) * 24)),
        template="plotly_dark",
        paper_bgcolor="#15111d",
        plot_bgcolor="#15111d",
        font=dict(color="#f7f3fa"),
        title_font=dict(color="#ffffff", size=18),
        xaxis=dict(title_font=dict(color="#ffffff"), tickfont=dict(color="#d8cfdd"), gridcolor="#3a3142"),
        yaxis=dict(title_font=dict(color="#ffffff"), tickfont=dict(color="#d8cfdd"), gridcolor="#3a3142", categoryorder="total ascending"),
        legend=dict(font=dict(color="#ffffff"))
    )
    st.plotly_chart(fig_routes, width="stretch")

# ============================================================
# TAB 2 — GEOGRAPHIC VIEW
# ============================================================

# ============================================================
# TAB 2 — GEOGRAPHIC VIEW
# ============================================================

with tab2:
    st.markdown(
        '<div class="section-title">Geographic Shipping Intelligence</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-note">Identify high-volume areas, slower regions and potential geographic bottlenecks.</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Regional Shipping Performance")
        st.dataframe(
            region_summary[
                [
                    "Region",
                    "Total_Shipments",
                    "Average_Lead_Time",
                    "Lead_Time_Variability"
                ]
            ]
            .sort_values("Average_Lead_Time")
            .rename(columns={
                "Total_Shipments": "Total Shipments",
                "Average_Lead_Time": "Average Lead Time (days)",
                "Lead_Time_Variability": "Lead-Time Variability (days)"
            })
            .style.format({
                "Total Shipments": "{:,.0f}",
                "Average Lead Time (days)": "{:,.1f}",
                "Lead-Time Variability (days)": "{:,.1f}"
            }),
            width="stretch",
            hide_index=True
        )

    with c2:
        st.subheader("High-Volume States")

        high_volume_states = state_summary.sort_values(
            "Total_Shipments",
            ascending=False
        ).head(10)

        st.dataframe(
            high_volume_states[
                [
                    "State/Province",
                    "Total_Shipments",
                    "Average_Lead_Time",
                    "Lead_Time_Variability"
                ]
            ]
            .rename(columns={
                "Total_Shipments": "Total Shipments",
                "Average_Lead_Time": "Average Lead Time (days)",
                "Lead_Time_Variability": "Lead-Time Variability (days)"
            })
            .style.format({
                "Total Shipments": "{:,.0f}",
                "Average Lead Time (days)": "{:,.1f}",
                "Lead-Time Variability (days)": "{:,.1f}"
            }),
            width="stretch",
            hide_index=True
        )

    # --------------------------------------------------------
    # POTENTIAL GEOGRAPHIC BOTTLENECKS
    # --------------------------------------------------------

    st.subheader("Potential Geographic Bottlenecks")

    volume_median = state_summary["Total_Shipments"].median()
    lead_time_median = state_summary["Average_Lead_Time"].median()

    potential_bottlenecks = state_summary[
        (state_summary["Total_Shipments"] > volume_median)
        & (state_summary["Average_Lead_Time"] > lead_time_median)
    ].copy()

    potential_bottlenecks = potential_bottlenecks.sort_values(
        ["Average_Lead_Time", "Total_Shipments"],
        ascending=[False, False]
    )

    st.caption(
        "Potential bottleneck states are identified as states with both "
        "above-median shipment volume and above-median average recorded "
        "lead time within the current filtered dataset."
    )

    if potential_bottlenecks.empty:
        st.info(
            "No states meet both bottleneck criteria under the current filters."
        )
    else:
        st.dataframe(
            potential_bottlenecks[
                [
                    "State/Province",
                    "Total_Shipments",
                    "Average_Lead_Time",
                    "Lead_Time_Variability"
                ]
            ]
            .rename(columns={
                "Total_Shipments": "Total Shipments",
                "Average_Lead_Time": "Average Lead Time (days)",
                "Lead_Time_Variability": "Lead-Time Variability (days)"
            })
            .style.format({
                "Total Shipments": "{:,.0f}",
                "Average Lead Time (days)": "{:,.1f}",
                "Lead-Time Variability (days)": "{:,.1f}"
            }),
            width="stretch",
            hide_index=True
        )

    # --------------------------------------------------------
    # STATE VOLUME VS LEAD TIME
    # --------------------------------------------------------

    fig_scatter = px.scatter(
        state_summary,
        x="Total_Shipments",
        y="Average_Lead_Time",
        size="Total_Shipments",
        hover_name="State/Province",
        hover_data=["Lead_Time_Variability"],
        labels={
            "Total_Shipments": "Total Shipments",
            "Average_Lead_Time": "Average Lead Time (days)",
            "Lead_Time_Variability": "Lead-Time Variability (days)"
        },
        title="State Shipment Volume vs Average Lead Time"
    )

    fig_scatter.update_layout(
        height=560,
        template="plotly_dark",
        paper_bgcolor="#15111d",
        plot_bgcolor="#15111d",
        font=dict(color="#f7f3fa"),
        title_font=dict(color="#ffffff", size=18),
        xaxis=dict(
            title_font=dict(color="#ffffff"),
            tickfont=dict(color="#d8cfdd"),
            gridcolor="#3a3142"
        ),
        yaxis=dict(
            title_font=dict(color="#ffffff"),
            tickfont=dict(color="#d8cfdd"),
            gridcolor="#3a3142"
        )
    )

    st.plotly_chart(fig_scatter, width="stretch")

    # ========================================================
    # US SHIPPING EFFICIENCY MAP
    # ========================================================

    st.subheader("US Shipping Efficiency Map")

    st.caption(
        "Use the controls below to focus the map on a factory, customer "
        "region and performance metric."
    )

    # --------------------------------------------------------
    # MAP FILTERS
    # --------------------------------------------------------

    map_col1, map_col2, map_col3 = st.columns(3)

    with map_col1:
        map_factory_options = [
            "All Factories"
        ] + sorted(
            filtered_df["Factory"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_map_factory = st.selectbox(
            "Factory",
            map_factory_options,
            index=0,
            key="map_factory_filter"
        )

    with map_col2:
        map_region_options = [
            "All Regions"
        ] + sorted(
            filtered_df["Region"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_map_region = st.selectbox(
            "Customer Region",
            map_region_options,
            index=0,
            key="map_region_filter"
        )

    with map_col3:
        selected_map_metric = st.selectbox(
            "Map Metric",
            [
                "Average Lead Time",
                "Lead-Time Variability",
                "Shipment Volume"
            ],
            index=0,
            key="map_metric_filter"
        )

    # --------------------------------------------------------
    # APPLY MAP FILTERS
    # --------------------------------------------------------

    map_df = filtered_df.copy()

    if selected_map_factory != "All Factories":
        map_df = map_df[
            map_df["Factory"] == selected_map_factory
        ]

    if selected_map_region != "All Regions":
        map_df = map_df[
            map_df["Region"] == selected_map_region
        ]

    # --------------------------------------------------------
    # US STATE ABBREVIATIONS
    # --------------------------------------------------------

    us_state_abbreviations = {
        "Alabama": "AL",
        "Alaska": "AK",
        "Arizona": "AZ",
        "Arkansas": "AR",
        "California": "CA",
        "Colorado": "CO",
        "Connecticut": "CT",
        "Delaware": "DE",
        "Florida": "FL",
        "Georgia": "GA",
        "Hawaii": "HI",
        "Idaho": "ID",
        "Illinois": "IL",
        "Indiana": "IN",
        "Iowa": "IA",
        "Kansas": "KS",
        "Kentucky": "KY",
        "Louisiana": "LA",
        "Maine": "ME",
        "Maryland": "MD",
        "Massachusetts": "MA",
        "Michigan": "MI",
        "Minnesota": "MN",
        "Mississippi": "MS",
        "Missouri": "MO",
        "Montana": "MT",
        "Nebraska": "NE",
        "Nevada": "NV",
        "New Hampshire": "NH",
        "New Jersey": "NJ",
        "New Mexico": "NM",
        "New York": "NY",
        "North Carolina": "NC",
        "North Dakota": "ND",
        "Ohio": "OH",
        "Oklahoma": "OK",
        "Oregon": "OR",
        "Pennsylvania": "PA",
        "Rhode Island": "RI",
        "South Carolina": "SC",
        "South Dakota": "SD",
        "Tennessee": "TN",
        "Texas": "TX",
        "Utah": "UT",
        "Vermont": "VT",
        "Virginia": "VA",
        "Washington": "WA",
        "West Virginia": "WV",
        "Wisconsin": "WI",
        "Wyoming": "WY",
        "District of Columbia": "DC"
    }

    # --------------------------------------------------------
    # CREATE MAP SUMMARY
    # --------------------------------------------------------

    if map_df.empty:

        st.warning(
            "No shipment records match the selected map filters."
        )

    else:

        map_state_summary = (
            map_df.groupby("State/Province")
            .agg(
                Total_Shipments=(
                    "Shipping Lead Time (days)",
                    "count"
                ),
                Average_Lead_Time=(
                    "Shipping Lead Time (days)",
                    "mean"
                ),
                Lead_Time_Variability=(
                    "Shipping Lead Time (days)",
                    "std"
                )
            )
            .reset_index()
        )

        map_state_summary["Lead_Time_Variability"] = (
            map_state_summary["Lead_Time_Variability"]
            .fillna(0)
        )

        # Keep US states only
        us_map_data = map_state_summary[
            map_state_summary["State/Province"]
            .isin(us_state_abbreviations.keys())
        ].copy()

        us_map_data["State_Code"] = (
            us_map_data["State/Province"]
            .map(us_state_abbreviations)
        )

        # ----------------------------------------------------
        # SELECT MAP METRIC
        # ----------------------------------------------------

        if selected_map_metric == "Average Lead Time":

            map_color_values = (
                us_map_data["Average_Lead_Time"]
            )

            map_colorbar_title = "Avg Lead Time (days)"

        elif selected_map_metric == "Lead-Time Variability":

            map_color_values = (
                us_map_data["Lead_Time_Variability"]
            )

            map_colorbar_title = "Lead-Time Variability (days)"

        else:

            map_color_values = (
                us_map_data["Total_Shipments"]
            )

            map_colorbar_title = "Shipment Volume"

        # ----------------------------------------------------
        # FACTORY LOCATIONS
        # ----------------------------------------------------

        factory_locations = pd.DataFrame({
            "Factory": [
                "Lot's O' Nuts",
                "Wicked Choccy's",
                "Sugar Shack",
                "Secret Factory",
                "The Other Factory"
            ],
            "Latitude": [
                32.881893,
                32.076176,
                48.11914,
                41.446333,
                35.1175
            ],
            "Longitude": [
                -111.768036,
                -81.088371,
                -96.18115,
                -90.565487,
                -89.971107
            ]
        })

        # If a specific factory is selected, show only
        # that factory marker.
        if selected_map_factory != "All Factories":
            factory_locations = factory_locations[
                factory_locations["Factory"]
                == selected_map_factory
            ]

        # ----------------------------------------------------
        # CREATE MAP
        # ----------------------------------------------------

        fig_map = go.Figure()

        # State choropleth
        fig_map.add_trace(
            go.Choropleth(
                locations=us_map_data["State_Code"],
                z=map_color_values,
                locationmode="USA-states",
                text=us_map_data["State/Province"],
                customdata=us_map_data[
                    [
                        "Total_Shipments",
                        "Average_Lead_Time",
                        "Lead_Time_Variability"
                    ]
                ],
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "Average Lead Time: %{customdata[1]:.1f} days<br>"
                    "Total Shipments: %{customdata[0]:,}<br>"
                    "Lead-Time Variability: %{customdata[2]:.1f} days"
                    "<extra></extra>"
                ),
                colorbar_title=map_colorbar_title,
                colorscale="Plasma"
            )
        )

        # Factory markers
        fig_map.add_trace(
            go.Scattergeo(
                lon=factory_locations["Longitude"],
                lat=factory_locations["Latitude"],
                text=factory_locations["Factory"],
                mode="markers",
                marker=dict(
                    size=11,
                    symbol="star"
                ),
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "Factory Location"
                    "<extra></extra>"
                ),
                name="Factories"
            )
        )

        # ----------------------------------------------------
        # MAP LAYOUT
        # ----------------------------------------------------

        fig_map.update_layout(
            template="plotly_white",
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(color="#24172b"),
            title=(
                f"US Shipping Efficiency by Customer State — "
                f"{selected_map_metric}"
            ),
            geo=dict(
                scope="usa",
                showland=True,
                showlakes=True
            ),
            height=650,
            margin=dict(
                l=0,
                r=0,
                t=60,
                b=0
            )
        )

        st.plotly_chart(
            fig_map,
            width="stretch"
        )

        st.caption(
            "The map focuses on US customer states as required by the "
            "technical documentation. Canadian records remain retained "
            "for other analyses."
        )


# ============================================================
# TAB 3 — SHIP MODES
# ============================================================

with tab3:
    st.markdown('<div class="section-title">Ship Mode Performance</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-note">Compare recorded lead time, volume, variability and descriptive financial context.</div>',
        unsafe_allow_html=True
    )

    ship_mode_summary = (
        filtered_df.groupby("Ship Mode")
        .agg(
            Total_Shipments=("Shipping Lead Time (days)", "count"),
            Average_Lead_Time=("Shipping Lead Time (days)", "mean"),
            Lead_Time_Variability=("Shipping Lead Time (days)", "std"),
            Total_Sales=("Sales", "sum"),
            Gross_Profit=("Gross Profit", "sum")
        )
        .reset_index()
    )

    ship_mode_summary["Lead_Time_Variability"] = (
        ship_mode_summary["Lead_Time_Variability"].fillna(0)
    )

    ship_mode_summary["Ship Mode"] = pd.Categorical(
        ship_mode_summary["Ship Mode"],
        categories=ship_mode_order,
        ordered=True
    )

    ship_mode_summary = (
        ship_mode_summary.sort_values("Ship Mode").reset_index(drop=True)
    )

    c1, c2 = st.columns(2)

    with c1:
        fig_ship_mode = px.bar(
            ship_mode_summary,
            x="Ship Mode",
            y="Average_Lead_Time",
            text="Average_Lead_Time",
            title="Average Recorded Lead Time by Ship Mode",
            labels={
                "Average_Lead_Time": "Average Lead Time (days)",
                "Ship Mode": "Shipping Mode"
            }
        )
        fig_ship_mode.update_traces(
            texttemplate="%{text:.1f}", textposition="outside"
        )
        fig_ship_mode.update_layout(template="plotly_dark", paper_bgcolor="#15111d", plot_bgcolor="#15111d", font=dict(color="#f7f3fa"), title_font=dict(color="#ffffff", size=16), xaxis=dict(title_font=dict(color="#ffffff"), tickfont=dict(color="#d8cfdd")), yaxis=dict(title_font=dict(color="#ffffff"), tickfont=dict(color="#d8cfdd"), gridcolor="#3a3142"))
        st.plotly_chart(fig_ship_mode, width="stretch")

    with c2:
        fig_ship_volume = px.bar(
            ship_mode_summary,
            x="Ship Mode",
            y="Total_Shipments",
            text="Total_Shipments",
            title="Shipment Volume by Ship Mode",
            labels={
                "Total_Shipments": "Total Shipments",
                "Ship Mode": "Shipping Mode"
            }
        )
        fig_ship_volume.update_traces(
            texttemplate="%{text:,}", textposition="outside"
        )
        fig_ship_volume.update_layout(template="plotly_dark", paper_bgcolor="#15111d", plot_bgcolor="#15111d", font=dict(color="#f7f3fa"), title_font=dict(color="#ffffff", size=16), xaxis=dict(title_font=dict(color="#ffffff"), tickfont=dict(color="#d8cfdd")), yaxis=dict(title_font=dict(color="#ffffff"), tickfont=dict(color="#d8cfdd"), gridcolor="#3a3142"))
        st.plotly_chart(fig_ship_volume, width="stretch")

    st.subheader("Standard vs Expedited")

    filtered_df["Service Category"] = filtered_df["Ship Mode"].apply(
        lambda x: "Standard" if x == "Standard Class" else "Expedited"
    )

    service_category_summary = (
        filtered_df.groupby("Service Category")
        .agg(
            Total_Shipments=("Shipping Lead Time (days)", "count"),
            Average_Lead_Time=("Shipping Lead Time (days)", "mean"),
            Lead_Time_Variability=("Shipping Lead Time (days)", "std"),
            Total_Sales=("Sales", "sum"),
            Total_Cost=("Cost", "sum"),
            Gross_Profit=("Gross Profit", "sum")
        )
        .reset_index()
    )

    service_category_summary["Lead_Time_Variability"] = (
        service_category_summary["Lead_Time_Variability"].fillna(0)
    )

    service_category_summary["Gross_Margin_%"] = (
        service_category_summary["Gross_Profit"]
        / service_category_summary["Total_Sales"]
        * 100
    )

    service_category_order = ["Expedited", "Standard"]

    service_category_summary["Service Category"] = pd.Categorical(
        service_category_summary["Service Category"],
        categories=service_category_order,
        ordered=True
    )

    service_category_summary = (
        service_category_summary
        .sort_values("Service Category")
        .reset_index(drop=True)
    )

    st.caption(
        "Expedited includes Same Day, First Class and Second Class. Standard "
        "includes Standard Class. The comparison is descriptive and uses "
        "recorded shipping lead time. Cost is not a dedicated shipping-cost field."
    )

    st.dataframe(
        service_category_summary[
            ["Service Category", "Total_Shipments", "Average_Lead_Time",
             "Lead_Time_Variability", "Total_Sales", "Total_Cost",
             "Gross_Profit", "Gross_Margin_%"]
        ]
        .rename(columns={
            "Total_Shipments": "Total Shipments",
            "Average_Lead_Time": "Average Lead Time (days)",
            "Lead_Time_Variability": "Lead-Time Variability (days)",
            "Total_Sales": "Total Sales",
            "Total_Cost": "Total Cost",
            "Gross_Profit": "Gross Profit",
            "Gross_Margin_%": "Gross Margin (%)"
        })
        .style.format({
            "Total Shipments": "{:,.0f}",
            "Average Lead Time (days)": "{:,.1f}",
            "Lead-Time Variability (days)": "{:,.1f}",
            "Total Sales": "${:,.2f}",
            "Total Cost": "${:,.2f}",
            "Gross Profit": "${:,.2f}",
            "Gross Margin (%)": "{:.2f}%"
        }),
        width="stretch",
        hide_index=True
    )

    st.subheader("Lead-Time Variability by Ship Mode")

    fig_ship_variability = px.bar(
        ship_mode_summary,
        x="Ship Mode",
        y="Lead_Time_Variability",
        text="Lead_Time_Variability",
        title="Lead-Time Variability by Ship Mode",
        labels={
            "Lead_Time_Variability": "Lead-Time Variability (days)",
            "Ship Mode": "Shipping Mode"
        }
    )
    fig_ship_variability.update_traces(
        texttemplate="%{text:.1f}", textposition="outside"
    )
    fig_ship_variability.update_layout(template="plotly_dark", paper_bgcolor="#15111d", plot_bgcolor="#15111d", font=dict(color="#f7f3fa"), title_font=dict(color="#ffffff", size=16), xaxis=dict(title_font=dict(color="#ffffff"), tickfont=dict(color="#d8cfdd")), yaxis=dict(title_font=dict(color="#ffffff"), tickfont=dict(color="#d8cfdd"), gridcolor="#3a3142"))
    st.plotly_chart(fig_ship_variability, width="stretch")

    with st.expander("💰 Financial Context by Ship Mode"):
        ship_mode_financials = (
            filtered_df.groupby("Ship Mode")
            .agg(
                Total_Sales=("Sales", "sum"),
                Total_Cost=("Cost", "sum"),
                Gross_Profit=("Gross Profit", "sum")
            )
            .reset_index()
        )

        ship_mode_financials["Gross_Margin_%"] = (
            ship_mode_financials["Gross_Profit"]
            / ship_mode_financials["Total_Sales"]
            * 100
        )

        ship_mode_financials["Ship Mode"] = pd.Categorical(
            ship_mode_financials["Ship Mode"],
            categories=ship_mode_order,
            ordered=True
        )

        ship_mode_financials = (
            ship_mode_financials.sort_values("Ship Mode")
            .reset_index(drop=True)
        )

        st.caption(
            "Financial values represent product/order economics in the dataset. "
            "They should not be interpreted as shipping charges."
        )

        st.dataframe(
            ship_mode_financials.rename(columns={
                "Total_Sales": "Total Sales",
                "Total_Cost": "Total Cost",
                "Gross_Profit": "Gross Profit",
                "Gross_Margin_%": "Gross Margin (%)"
            }).style.format({
                "Total Sales": "${:,.2f}",
                "Total Cost": "${:,.2f}",
                "Gross Profit": "${:,.2f}",
                "Gross Margin (%)": "{:.2f}%"
            }),
            width="stretch",
            hide_index=True
        )

# ============================================================
# TAB 4 — ROUTE EXPLORER
# ============================================================

with tab4:
    st.markdown('<div class="section-title">Route Explorer</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-note">Drill into one factory-to-customer-state route and inspect shipment timelines.</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        drilldown_factories = sorted(
            filtered_df["Factory"].dropna().unique().tolist()
        )
        selected_factory = st.selectbox(
            "Select Factory",
            drilldown_factories,
            key="drilldown_factory_v3"
        )

    with col2:
        drilldown_states = sorted(
            filtered_df.loc[
                filtered_df["Factory"] == selected_factory,
                "State/Province"
            ].dropna().unique().tolist()
        )
        selected_drilldown_state = st.selectbox(
            "Select Customer State / Province",
            drilldown_states,
            key="drilldown_state_v3"
        )

    selected_route_df = filtered_df[
        (filtered_df["Factory"] == selected_factory)
        & (filtered_df["State/Province"] == selected_drilldown_state)
    ].copy()

    route_shipments = len(selected_route_df)
    route_average_lead_time = selected_route_df[
        "Shipping Lead Time (days)"
    ].mean()

    route_lead_time_variability = selected_route_df[
        "Shipping Lead Time (days)"
    ].std()

    if pd.isna(route_lead_time_variability):
        route_lead_time_variability = 0

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Route Shipments", f"{route_shipments:,}")
    with c2:
        st.metric("Average Lead Time", f"{route_average_lead_time:.1f} days")
    with c3:
        st.metric("Lead-Time Variability", f"{route_lead_time_variability:.1f} days")

    st.subheader(f"📍 {selected_factory} → {selected_drilldown_state}")

    route_order_details = selected_route_df[
        ["Order ID", "Order Date", "Ship Date", "Ship Mode",
         "Customer ID", "Product Name", "Shipping Lead Time (days)"]
    ].sort_values("Order Date").copy()

    with st.expander("📋 View order-level shipment details"):
        st.dataframe(
            route_order_details,
            width="stretch",
            hide_index=True
        )

    timeline_display_options = [25, 50, 100, "All"]

    selected_timeline_count = st.selectbox(
        "Timeline Records to Display",
        timeline_display_options,
        index=0,
        key="timeline_count_v3"
    )

    timeline_data = selected_route_df[
        ["Order ID", "Order Date", "Ship Date", "Ship Mode"]
    ].sort_values("Order Date").copy()

    if selected_timeline_count != "All":
        timeline_data = timeline_data.head(selected_timeline_count)

    timeline_data["Timeline Label"] = (
        timeline_data["Order ID"].astype(str)
        + " | "
        + timeline_data["Ship Mode"].astype(str)
    )

    fig_timeline = px.timeline(
        timeline_data,
        x_start="Order Date",
        x_end="Ship Date",
        y="Timeline Label",
        color="Ship Mode",
        hover_data={
            "Order ID": True,
            "Order Date": True,
            "Ship Date": True,
            "Ship Mode": True
        },
        title="Order Date → Ship Date Timeline"
    )

    fig_timeline.update_yaxes(
        autorange="reversed",
        title="Orders"
    )
    fig_timeline.update_xaxes(title="Date")
    fig_timeline.update_layout(height=620, template="plotly_dark", paper_bgcolor="#15111d", plot_bgcolor="#15111d", font=dict(color="#f7f3fa"), title_font=dict(color="#ffffff", size=16), xaxis=dict(title_font=dict(color="#ffffff"), tickfont=dict(color="#d8cfdd"), gridcolor="#3a3142"), yaxis=dict(title_font=dict(color="#ffffff"), tickfont=dict(color="#d8cfdd")))

    st.plotly_chart(fig_timeline, width="stretch")

# ============================================================
# TAB 5 — DATA & METHODOLOGY
# ============================================================

with tab5:
    st.markdown('<div class="section-title">Data Quality & Methodology</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-note">Transparent view of the dataset preparation and analytical definitions.</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Records Loaded", f"{records_loaded:,}")
    with c2:
        st.metric("Missing Order Dates", f"{missing_order_dates:,}")
    with c3:
        st.metric("Missing Ship Dates", f"{missing_ship_dates:,}")
    with c4:
        st.metric("Invalid / Negative Lead Times", f"{invalid_lead_time_count:,}")

    st.success(
        f"Records remaining after validation: {len(df):,}"
    )

    with st.expander("🧹 Data Cleaning & Validation"):
        st.markdown("""
        - Order Date and Ship Date are parsed using the documented day-first format.
        - Shipping Lead Time is calculated as Ship Date − Order Date.
        - Missing dates and invalid/negative lead times are identified.
        - Invalid/negative lead-time records are removed.
        - Geographic fields are standardized by trimming whitespace.
        - The underlying source values are not manually altered.
        """)

    with st.expander("🏭 Factory & Route Definitions"):
        st.markdown("""
        **Factory assignment** is based on the documented Product → Factory mapping.

        **Region route:** Factory + Customer Region

        **State route:** Factory + Customer State / Province

        Route metrics include total shipments, average recorded lead time,
        and lead-time variability.
        """)

    with st.expander("🏆 Route Efficiency Score"):
        st.markdown("""
        The dashboard uses a normalized 0–100 presentation score based on
        average recorded lead time across the available factory-to-state routes.
        A higher score represents better recorded route performance.

        This score is an analytical presentation metric because the technical
        documentation specifies a normalized efficiency score but does not
        prescribe a particular normalization formula.
        """)

    with st.expander("⚠️ Important Lead-Time Interpretation"):
        st.warning(
            "The recorded shipment dates in the source dataset produce multi-year "
            "lead times. The dashboard retains those values rather than inventing "
            "a plausibility threshold or changing the source dates. Delay analysis "
            "therefore refers specifically to recorded lead time."
        )

    with st.expander("🚚 Ship Mode Definitions"):
        st.markdown("""
        **Standard:** Standard Class

        **Expedited:** Same Day, First Class and Second Class

        The Standard vs Expedited comparison is descriptive. The dataset does
        not contain a dedicated shipping-cost field, so Cost is not treated as
        shipping expense.
        """)

    st.caption(
        "Nassau Candy Distributor • Factory-to-Customer Shipping Route Efficiency Analysis"
    )
