import plotly.express as px
import pandas as pd


def issue_bar_chart(data: pd.DataFrame):

    fig = px.bar(
        data,
        x="Issue",
        y="Count",
        color="Issue",
        text="Count",
        color_discrete_sequence=px.colors.qualitative.Safe
    )

    fig.update_layout(
        height=380,
        template="plotly_white",
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    fig.update_traces(textposition="outside")

    return fig


def issue_pie_chart(data: pd.DataFrame):

    fig = px.pie(
        data,
        names="Issue",
        values="Count",
        hole=0.55
    )

    fig.update_layout(
        height=380,
        template="plotly_white",
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig


def missing_values_chart(data: pd.DataFrame):

    fig = px.bar(
        data,
        x="Column",
        y="Missing",
        text="Missing",
        color="Missing",
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        height=400,
        template="plotly_white",
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title="Column",
        yaxis_title="Missing Values"
    )

    return fig


def numeric_distribution(df: pd.DataFrame, column: str):

    fig = px.histogram(
        df,
        x=column,
        nbins=30
    )

    fig.update_layout(
        height=380,
        template="plotly_white",
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig


def correlation_heatmap(df: pd.DataFrame):

    numeric = df.select_dtypes(include="number")

    if numeric.empty:
        return None

    corr = numeric.corr()

    fig = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdBu_r"
    )

    fig.update_layout(
        height=500,
        template="plotly_white"
    )

    return fig


def data_type_chart(df: pd.DataFrame):

    counts = (
        df.dtypes
        .astype(str)
        .value_counts()
        .reset_index()
    )

    counts.columns = ["Type", "Count"]

    fig = px.pie(
        counts,
        names="Type",
        values="Count",
        hole=0.45
    )

    fig.update_layout(
        height=380,
        template="plotly_white"
    )

    return fig