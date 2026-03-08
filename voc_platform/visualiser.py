import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def plot_sentiment_breakdown(df):
    """
    Pie chart showing Positive / Negative / Neutral split
    """
    counts = df["sentiment"].value_counts().reset_index()
    counts.columns = ["sentiment", "count"]

    colours = {
        "Positive": "#3FB950",
        "Negative": "#F85149",
        "Neutral": "#8B949E"
    }

    fig = px.pie(
        counts,
        names="sentiment",
        values="count",
        color="sentiment",
        color_discrete_map=colours,
        title="Sentiment Breakdown",
        hole=0.45  # Makes it a donut chart — looks cleaner
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent background
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E6EDF3"),
        title_font_size=16,
        showlegend=True
    )

    return fig


def plot_theme_distribution(df):
    """
    Horizontal bar chart of feedback themes
    """
    counts = df["theme"].value_counts().reset_index()
    counts.columns = ["theme", "count"]
    counts = counts.sort_values("count", ascending=True)  # ascending for horizontal

    fig = px.bar(
        counts,
        x="count",
        y="theme",
        orientation="h",
        title="Feedback by Theme",
        color="count",
        color_continuous_scale=["#1C2128", "#FF9900"]  # Dark to Amazon orange
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E6EDF3"),
        title_font_size=16,
        showlegend=False,
        coloraxis_showscale=False,
        xaxis=dict(gridcolor="#30363D"),
        yaxis=dict(gridcolor="#30363D")
    )

    return fig


def plot_severity_breakdown(df):
    """
    Bar chart showing Critical / High / Medium / Low counts
    """
    order = ["Critical", "High", "Medium", "Low"]
    counts = df["severity"].value_counts().reindex(order, fill_value=0).reset_index()
    counts.columns = ["severity", "count"]

    colours = {
        "Critical": "#F85149",
        "High": "#FF9900",
        "Medium": "#F0C040",
        "Low": "#3FB950"
    }

    fig = px.bar(
        counts,
        x="severity",
        y="count",
        title="Issues by Severity",
        color="severity",
        color_discrete_map=colours
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E6EDF3"),
        title_font_size=16,
        showlegend=False,
        xaxis=dict(gridcolor="#30363D"),
        yaxis=dict(gridcolor="#30363D")
    )

    return fig


def plot_priority_matrix(df):
    """
    Scatter plot — Frequency (x) vs Severity score (y)
    This is the most powerful chart — shows what to fix first
    """

    # Convert severity to a number so we can plot it
    severity_score = {
        "Critical": 4,
        "High": 3,
        "Medium": 2,
        "Low": 1
    }

    # Count frequency and average severity per theme
    df["severity_score"] = df["severity"].map(severity_score)
    matrix = df.groupby("theme").agg(
        frequency=("theme", "count"),
        avg_severity=("severity_score", "mean")
    ).reset_index()

    # Colour by frequency
    fig = px.scatter(
        matrix,
        x="frequency",
        y="avg_severity",
        text="theme",
        size="frequency",
        title="Priority Matrix — What to Fix First",
        color="avg_severity",
        color_continuous_scale=["#3FB950", "#FF9900", "#F85149"]
    )

    fig.update_traces(
        textposition="top center",
        marker=dict(opacity=0.85)
    )

    # Add quadrant lines
    fig.add_hline(
        y=2.5,
        line_dash="dash",
        line_color="#30363D",
        annotation_text="Severity threshold"
    )
    fig.add_vline(
        x=matrix["frequency"].mean(),
        line_dash="dash",
        line_color="#30363D",
        annotation_text="Avg frequency"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E6EDF3"),
        title_font_size=16,
        coloraxis_showscale=False,
        xaxis=dict(
            title="Frequency (how often mentioned)",
            gridcolor="#30363D"
        ),
        yaxis=dict(
            title="Avg Severity (1=Low, 4=Critical)",
            gridcolor="#30363D",
            range=[0.5, 4.5]
        )
    )

    return fig


def plot_feature_areas(df):
    """
    Top 10 most mentioned feature areas
    """
    counts = df["feature_area"].value_counts().head(10).reset_index()
    counts.columns = ["feature_area", "count"]
    counts = counts.sort_values("count", ascending=True)

    fig = px.bar(
        counts,
        x="count",
        y="feature_area",
        orientation="h",
        title="Top Mentioned Feature Areas",
        color="count",
        color_continuous_scale=["#1C2128", "#58A6FF"]
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E6EDF3"),
        title_font_size=16,
        showlegend=False,
        coloraxis_showscale=False,
        xaxis=dict(gridcolor="#30363D"),
        yaxis=dict(gridcolor="#30363D")
    )

    return fig
# ```

# ---

# **Line by line — the important parts:**

# **`import plotly.express as px`**
# Plotly Express is the simple, high-level way to make charts. One line of code = a full interactive chart.

# **`import plotly.graph_objects as go`**
# Graph Objects is the lower-level, more customisable Plotly. We use it for adding the quadrant lines on the priority matrix.

# ---

# **Each function follows the same pattern:**
# ```
# raw data in → count/aggregate → build chart → style it → return it