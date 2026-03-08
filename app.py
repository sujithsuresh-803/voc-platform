import streamlit as st
import pandas as pd
from analyser import analyse_feedback, generate_executive_summary
from visualiser import (
    plot_sentiment_breakdown,
    plot_theme_distribution,
    plot_severity_breakdown,
    plot_priority_matrix,
    plot_feature_areas
)

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="VoC Intelligence Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ──
st.markdown("""
<style>
    /* Dark background */
    .stApp { background-color: #0D1117; color: #E6EDF3; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #161B22; border-right: 1px solid #30363D; }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #1C2128;
        border: 1px solid #30363D;
        border-radius: 8px;
        padding: 16px;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #FF9900;
        color: #111111;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        width: 100%;
    }
    .stButton > button:hover { background-color: #E47911; }
    
    /* Dataframe */
    [data-testid="stDataFrame"] { border: 1px solid #30363D; border-radius: 8px; }
    
    /* Headers */
    h1, h2, h3 { color: #E6EDF3; }
    
    /* Success/warning boxes */
    .stSuccess { background-color: rgba(63,185,80,0.1); border-color: #3FB950; }
    .stWarning { background-color: rgba(255,153,0,0.1); border-color: #FF9900; }
</style>
""", unsafe_allow_html=True)


# ── SIDEBAR ──
with st.sidebar:
    st.markdown("## 🎯 VoC Platform")
    st.markdown("*Voice of Customer Intelligence*")
    st.divider()

    st.markdown("### How to use")
    st.markdown("""
    1. **Paste** customer feedback text, or
    2. **Upload** a CSV file
    3. Click **Analyse**
    4. View insights & download report
    """)

    st.divider()
    st.markdown("### Sample feedback")
    st.markdown("*Don't have data? Use this to test:*")

    sample_data = """The app crashes every time I try to play a song offline
Music recommendations are spot on, love the discover weekly
Can't figure out how to create a collaborative playlist
Premium price is too high compared to Spotify
The new UI update made everything harder to find
Audio quality in HD mode is absolutely incredible
App uses too much battery in the background
Customer support took 5 days to respond to my issue
Lyrics feature doesn't sync properly with the music
The family plan is great value for money
Search results are terrible, can't find niche artists
Offline download speed is very slow on mobile
The podcast integration is seamless and well designed
App freezes when switching between songs quickly
Love the artist merch store integration"""

    if st.button("Load Sample Data"):
        st.session_state["sample_loaded"] = sample_data
    
    st.divider()
    st.markdown("### About")
    st.markdown("Built by **Sujith Suresh**")
    st.markdown("Product Operations Manager")
    st.markdown("[LinkedIn](https://linkedin.com/in/sujith-suresh) · [Portfolio](https://sujithsuresh.github.io)")


# ── MAIN HEADER ──
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("# 🎯 Voice of Customer Intelligence Platform")
    st.markdown("*Turn raw customer feedback into actionable product insights — powered by Gemini AI*")
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Powered by**")
    st.markdown("🤖 Google Gemini 1.5 Flash")

st.divider()


# ── INPUT SECTION ──
st.markdown("## 📥 Input Feedback")

tab1, tab2 = st.tabs(["📝 Paste Text", "📁 Upload CSV"])

feedback_list = []

with tab1:
    # Check if sample data was loaded
    default_text = ""
    if "sample_loaded" in st.session_state:
        default_text = st.session_state["sample_loaded"]

    text_input = st.text_area(
        "Paste one feedback item per line",
        value=default_text,
        height=200,
        placeholder="The app crashes on startup...\nLove the new playlist feature...\nPricing is too expensive..."
    )

    if text_input:
        feedback_list = [line.strip() for line in text_input.strip().split("\n") if line.strip()]
        st.caption(f"✅ {len(feedback_list)} feedback items detected")

with tab2:
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file:
        df_upload = pd.read_csv(uploaded_file)
        st.markdown("**Preview:**")
        st.dataframe(df_upload.head(), use_container_width=True)

        # Let user pick which column has the feedback
        col = st.selectbox("Which column contains the feedback?", df_upload.columns)
        feedback_list = df_upload[col].dropna().astype(str).tolist()
        st.caption(f"✅ {len(feedback_list)} feedback items loaded")


# ── ANALYSE BUTTON ──
st.markdown("<br>", unsafe_allow_html=True)

if feedback_list:
    if st.button(f"🚀 Analyse {len(feedback_list)} Feedback Items"):

        # ── ANALYSIS ──
        with st.spinner("🤖 Gemini is analysing your feedback..."):
            try:
                df = analyse_feedback(feedback_list)
                st.session_state["results"] = df
                st.success(f"✅ Analysis complete — {len(df)} items processed!")
            except Exception as e:
                st.error(f"❌ Something went wrong: {str(e)}")
                st.stop()

        # ── EXECUTIVE SUMMARY ──
        with st.spinner("📝 Generating executive summary..."):
            summary = generate_executive_summary(st.session_state["results"])
            st.session_state["summary"] = summary


# ── RESULTS ──
if "results" in st.session_state:
    df = st.session_state["results"]
    summary = st.session_state.get("summary", "")

    st.divider()
    st.markdown("## 📊 Results")

    # ── METRIC CARDS ──
    m1, m2, m3, m4, m5 = st.columns(5)

    with m1:
        st.metric("Total Analysed", len(df))
    with m2:
        critical = len(df[df["severity"] == "Critical"])
        st.metric("Critical Issues", critical, delta=f"{round(critical/len(df)*100)}% of total", delta_color="inverse")
    with m3:
        negative = len(df[df["sentiment"] == "Negative"])
        st.metric("Negative Sentiment", negative, delta=f"{round(negative/len(df)*100)}%", delta_color="inverse")
    with m4:
        positive = len(df[df["sentiment"] == "Positive"])
        st.metric("Positive Sentiment", positive, delta=f"{round(positive/len(df)*100)}%")
    with m5:
        top_theme = df["theme"].value_counts().index[0]
        st.metric("Top Theme", top_theme)

    st.divider()

    # ── CHARTS ROW 1 ──
    st.markdown("### 📈 Insight Charts")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.plotly_chart(plot_sentiment_breakdown(df), use_container_width=True)
    with c2:
        st.plotly_chart(plot_theme_distribution(df), use_container_width=True)
    with c3:
        st.plotly_chart(plot_severity_breakdown(df), use_container_width=True)

    # ── CHARTS ROW 2 ──
    c4, c5 = st.columns([1.3, 1])

    with c4:
        st.plotly_chart(plot_priority_matrix(df), use_container_width=True)
    with c5:
        st.plotly_chart(plot_feature_areas(df), use_container_width=True)

    st.divider()

    # ── EXECUTIVE SUMMARY ──
    st.markdown("### 📋 Executive Summary")
    st.markdown(summary)

    st.divider()

    # ── RAW DATA TABLE ──
    st.markdown("### 🗃️ Tagged Feedback Table")

    # Filter controls
    f1, f2, f3 = st.columns(3)
    with f1:
        sentiment_filter = st.multiselect(
            "Filter by Sentiment",
            options=df["sentiment"].unique(),
            default=df["sentiment"].unique()
        )
    with f2:
        severity_filter = st.multiselect(
            "Filter by Severity",
            options=df["severity"].unique(),
            default=df["severity"].unique()
        )
    with f3:
        theme_filter = st.multiselect(
            "Filter by Theme",
            options=df["theme"].unique(),
            default=df["theme"].unique()
        )

    # Apply filters
    filtered_df = df[
        (df["sentiment"].isin(sentiment_filter)) &
        (df["severity"].isin(severity_filter)) &
        (df["theme"].isin(theme_filter))
    ]

    st.dataframe(filtered_df, use_container_width=True, height=300)
    st.caption(f"Showing {len(filtered_df)} of {len(df)} items")

    st.divider()

    # ── DOWNLOAD ──
    st.markdown("### 💾 Download")
    d1, d2 = st.columns(2)

    with d1:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="⬇️ Download Tagged Data (CSV)",
            data=csv,
            file_name="voc_analysis.csv",
            mime="text/csv"
        )
    with d2:
        st.download_button(
            label="⬇️ Download Executive Summary (TXT)",
            data=summary,
            file_name="executive_summary.txt",
            mime="text/plain"
        )