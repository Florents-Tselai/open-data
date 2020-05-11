# -*- coding: utf-8 -*-

import requests
import datetime

import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

baseHopkinsURL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"

TICKFONT = dict(family="Roboto", size=12, color="#114B5F")

TEXTFONT = dict(family="Roboto", size=16, color="#114B5F")

XAXIS = dict(
    showline=True,
    zeroline=True,
    showgrid=False,
    showticklabels=True,
    linecolor="#114B5F",
    linewidth=0.1,
    ticks="outside",
    tickcolor="#BBBBBB",
    gridcolor="#F8FAFA",
    tickfont=TICKFONT,
)

YAXIS = dict(
    showgrid=True,
    gridcolor="#F8FAFA",
    zeroline=False,
    showline=True,
    showticklabels=True,
    linecolor="#114B5F",
    linewidth=0.1,
    ticks="outside",
    tickcolor="#BBBBBB",
    tickfont=TICKFONT,
)

TICKFONT_STYLE = dict(family="Roboto", size=8, color="#114B5F")

TEXTFONT = dict(family="Roboto", size=16, color="#114B5F")

XAXIS_STYLE = dict(
    showline=True,
    zeroline=False,
    showgrid=True,
    showticklabels=True,
    linecolor="#114B5F",
    linewidth=0.1,
    ticks="outside",
    tickcolor="#BBBBBB",
    gridcolor="#F8FAFA",
    tickfont=TICKFONT_STYLE,
)

YAXIS_STYLE = dict(
    showgrid=True,
    gridcolor="#F8FAFA",
    zeroline=False,
    showline=True,
    showticklabels=True,
    linecolor="#114B5F",
    linewidth=0.1,
    ticks="outside",
    tickcolor="#BBBBBB",
    tickfont=TICKFONT_STYLE,
)

YAXIS_STYLE2 = dict(
    showgrid=True,
    gridcolor="#F8FAFA",
    zeroline=False,
    showline=False,
    showticklabels=False,
    linecolor="#114B5F",
    linewidth=0.1,
    tickcolor="#BBBBBB",
    tickfont=TICKFONT_STYLE,
)


def parseFloat(x):
    try:
        x = x.replace(",", "")
        return float(x)
    except ValueError:
        return None


def create_scatterplot_casesVStests_logx(name, wom_data, countries_data, show=False):
    wom = wom_data

    countries_names = countries_data
    countries_names = countries_names.rename(columns={"ADMIN": "Country,Other"})
    wom = pd.merge(wom, countries_names, on="Country,Other", how="left")

    wom["Tot Cases/1M pop"] = (wom["Tot Cases/1M pop"]).apply(lambda x: parseFloat(x))
    wom["Deaths/1M pop"] = (wom["Deaths/1M pop"]).apply(lambda x: parseFloat(x))
    wom["Tests/ 1M pop"] = (wom["Tests/ 1M pop"]).apply(lambda x: parseFloat(x))

    wom["testing_median_diff_pct"] = (
        (wom["Tests/ 1M pop"] - wom["Tests/ 1M pop"].median())
        / wom["Tests/ 1M pop"].median()
    ) * 100
    wom["cases_rate_normalized"] = (wom["Tot Cases/1M pop"] * 100) / wom[
        "Tests/ 1M pop"
    ]
    wom["cases_rate_normalized"] = wom["cases_rate_normalized"].round(2)
    wom["cases_rate_median_diff_pct"] = (
        (wom["cases_rate_normalized"] - wom["cases_rate_normalized"].median())
        / wom["cases_rate_normalized"].median()
    ) * 100

    wom = wom[wom["Deaths/1M pop"] > 0]

    def text(row):
        if row["Country,Other"] == "Greece":
            return row["ADMIN_GR"]
        else:
            return ""

    texts = [text(row) for index, row in wom.iterrows()]

    fig = px.scatter(
        wom,
        x=wom["Tests/ 1M pop"],
        y=wom["Tot Cases/1M pop"],
        size=wom["Deaths/1M pop"] + 150,
        hover_name="ADMIN_GR",
        color=(wom["Deaths/1M pop"]),
        color_continuous_scale=[("#3f6678"), ("#BA3A0A")],
        range_color=[wom["Deaths/1M pop"].min(), wom["Deaths/1M pop"].max()],
        opacity=0.9,
        log_y=True,
        log_x=True,
        text=texts,
        labels={
            "Deaths/1M pop": "<b>Θάνατοι</b>/<br>1Μ",
            "Tests/ 1M pop": "Τεστ/ 1M πληθυσμού",
            "Tot Cases/1M pop": "Κρούσματα/ 1M πληθυσμού",
            "size": "",
            "text": "",
        },
    )

    fig.update_traces(textposition="middle right", textfont=TEXTFONT)

    fig.update_layout(
        xaxis=XAXIS,
        yaxis=YAXIS,
        showlegend=True,
        paper_bgcolor="#E6ECEC",
        plot_bgcolor="#E6ECEC",
        title=dict(
            text="<b>Κρούσματα</b>, <b>Τεστ</b> και <b>Θάνατοι</b> ανά χώρα<br>",
            font=TEXTFONT,
        ),
        xaxis_title=dict(text="<b>Τεστ</b>/1 εκατ. πληθυσμού", font=TICKFONT),
        yaxis_title=dict(text="<b>Κρούσματα</b>/1 εκατ. πληθυσμού", font=TICKFONT),
        hoverlabel=dict(font_size=10, font_family="Roboto"),
        hovermode="closest"
        # annotations=[dict(
        #     x=0,
        #     y=-.21,
        #     xref='paper',
        #     yref='paper',
        #     text='<br> Πηγή δεδομένων: <a href="https://www.worldometers.info/coronavirus/">Worldometer</a>',
        #     showarrow=False,
        #     visible=True,
        #     font=dict(
        #         family='Roboto',
        #         color='#114B5F',
        #         size=10
        #     )
        # )]
    )

    fig.update_layout(
        coloraxis_colorbar=dict(
            nticks=3,
            tickmode="array",
            tick0=wom["Deaths/1M pop"].min(),
            tickvals=[
                wom["Deaths/1M pop"].min(),
                wom["Deaths/1M pop"].max() / 2,
                wom["Deaths/1M pop"].max(),
            ],
            ticktext=[
                wom["Deaths/1M pop"].min(),
                wom["Deaths/1M pop"].max() / 2,
                wom["Deaths/1M pop"].max(),
            ],
        )
    )

    fig.update_layout(height=450, margin=dict(l=30, r=10, b=10, t=80, pad=0))

    if show:
        config = dict(
            {
                "displayModeBar": True,
                "scrollZoom": False,
                "displaylogo": False,
                "responsive": True,
                "staticPlot": False,
            }
        )
        fig.show(config=config)
    fig.write_json(name + ".json")


def create_scatterplot_casesVStests_logy(name, wom_data, countries_data, show=False):
    wom = wom_data

    countries_names = countries_data
    countries_names = countries_names.rename(columns={"ADMIN": "Country,Other"})
    wom = pd.merge(wom, countries_names, on="Country,Other", how="left")

    wom["Tot Cases/1M pop"] = (wom["Tot Cases/1M pop"]).apply(lambda x: parseFloat(x))
    wom["Deaths/1M pop"] = (wom["Deaths/1M pop"]).apply(lambda x: parseFloat(x))
    wom["Tests/ 1M pop"] = (wom["Tests/ 1M pop"]).apply(lambda x: parseFloat(x))

    wom["testing_median_diff_pct"] = (
        (wom["Tests/ 1M pop"] - wom["Tests/ 1M pop"].median())
        / wom["Tests/ 1M pop"].median()
    ) * 100
    wom["cases_rate_normalized"] = (wom["Tot Cases/1M pop"] * 100) / wom[
        "Tests/ 1M pop"
    ]
    wom["cases_rate_median_diff_pct"] = (
        (wom["cases_rate_normalized"] - wom["cases_rate_normalized"].median())
        / wom["cases_rate_normalized"].median()
    ) * 100

    wom = wom[wom["Deaths/1M pop"] > 0]

    def info(row):
        if (row["testing_median_diff_pct"] > 3000) & (
            row["cases_rate_median_diff_pct"] < 0
        ):
            return row["ADMIN_GR"]
        elif row["Country,Other"] == "Greece":
            return row["ADMIN_GR"]
        elif row["Deaths/1M pop"] == wom["Deaths/1M pop"].max():
            return row["ADMIN_GR"]
        else:
            return ""

    texts = [info(row) for index, row in wom.iterrows()]

    fig = px.scatter(
        wom,
        x=wom["Tests/ 1M pop"],
        y=wom["Tot Cases/1M pop"],
        size=wom["Deaths/1M pop"] + 150,
        hover_name="ADMIN_GR",
        color=(wom["Deaths/1M pop"]),
        color_continuous_scale=[("#3f6678"), ("#BA3A0A")],
        range_color=[wom["Deaths/1M pop"].min(), wom["Deaths/1M pop"].max()],
        opacity=0.9,
        log_y=True,
        log_x=False,
        text=texts,
        labels={
            "Deaths/1M pop": "Θάνατοι/1M πληθυσμού",
            "Tests/ 1M pop": "Τεστ/1M πληθυσμού",
            "Tot Cases/1M pop": "Κρούσματα/1M πληθυσμού",
            "size": "",
            "text": "",
        },
    )

    fig.update_traces(textposition="bottom center", textfont=TEXTFONT)

    fig.update_layout(
        xaxis=XAXIS,
        yaxis=YAXIS,
        showlegend=True,
        paper_bgcolor="#E6ECEC",
        plot_bgcolor="#E6ECEC",
        title=dict(
            text="<br><b>Κρούσματα</b> και Τεστ ανά 1 εκατ. πληθυσμού<br>",
            font=TEXTFONT,
        ),
        xaxis_title=dict(text="Τεστ/1 εκατ. πληθυσμού", font=TICKFONT),
        yaxis_title=dict(text="Κρούσματα/1 εκατ. πληθυσμού", font=TICKFONT),
        hoverlabel=dict(font_size=10, font_family="Roboto"),
        hovermode="closest",
        annotations=[
            dict(
                x=0,
                y=-0.2,
                xref="paper",
                yref="paper",
                text='<br> Πηγή δεδομένων: <a href="https://www.worldometers.info/coronavirus/">Worldometer</a>',
                showarrow=False,
                visible=True,
                align="left",
                font=dict(family="Roboto", color="#114B5F", size=10),
            )
        ],
    )

    fig.update_layout(
        coloraxis_colorbar=dict(
            nticks=3,
            tickmode="array",
            tick0=wom["Deaths/1M pop"].min(),
            tickvals=[
                wom["Deaths/1M pop"].min(),
                wom["Deaths/1M pop"].max() / 2,
                wom["Deaths/1M pop"].max(),
            ],
            ticktext=[
                wom["Deaths/1M pop"].min(),
                wom["Deaths/1M pop"].max() / 2,
                wom["Deaths/1M pop"].max(),
            ],
        )
    )

    fig.update_layout(height=450, margin=dict(l=10, r=10, b=10, t=80, pad=0))

    if show:
        config = dict(
            {
                "displayModeBar": True,
                "scrollZoom": False,
                "displaylogo": False,
                "responsive": True,
                "staticPlot": False,
            }
        )
        fig.show(config=config)

    fig.write_json(name + ".json")


def create_linechart_deaths_intubated_gr(name, greeceTimeline_data, show=False):
    df = greeceTimeline_data
    df = df.drop("Province/State", axis=1)
    df = df.drop("Country/Region", axis=1)
    df = df.set_index("Status")
    df = df.T
    df = df.reset_index()
    df = df.rename(columns={"index": "date"})
    df = df[15:]
    df["date"] = pd.to_datetime(df["date"])
    df["date"] = pd.to_datetime(df["date"], format="%b-%d-%y").dt.strftime("%d-%b")
    df["date_gr"] = df["date"]
    df["date_gr"] = df["date_gr"].astype(str)
    df["date_gr"] = df["date_gr"].str.replace("Feb", "Φεβ")
    df["date_gr"] = df["date_gr"].str.replace("Mar", "Μαρ")
    df["date_gr"] = df["date_gr"].str.replace("Apr", "Απρ")
    df["date_gr"] = df["date_gr"].str.replace("May", "Μάι")

    # Initialize figure
    fig = go.Figure()

    # Add Traces
    fig.add_trace(
        go.Scatter(
            x=df.date_gr,
            y=df.deaths,
            mode="lines+markers",
            connectgaps=True,
            marker_color="#BA3A0A",
            name="θάνατοι",
            line_shape="spline",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.date_gr,
            y=df.intubated,
            mode="lines+markers",
            connectgaps=True,
            marker_color="#3f6678",
            name="διασωληνωμένοι",
            line_shape="spline",
        )
    )

    # Add buttons
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                active=0,
                buttons=list([
                    dict(label="ΟΛΑ",
                         method="update",
                         args=[{"visible": [True, True]},
                               {"title": "Θάνατοι και διασωληνωμένοι ασθενείς ανά ημέρα στην Ελλάδα"}
                                ]),
                    dict(label="Θάνατοι",
                         method="update",
                         args=[{"visible": [True, False]},
                               {"title": "Θάνατοι ανά ημέρα στην Ελλάδα"}]
                                ),
                    dict(label="Διασ/μένοι",
                         method="update",
                         args=[{"visible": [False, True]},
                               {"title": "Διασωληνωμένοι ασθενείς ανά ημέρα στην Ελλάδα"}]
                                ),
                    
                    ]),
                    pad={'t':0, 'l':0, 'b':0, 'r':0},
                    showactive=True,
                    x=0.05,
                    xanchor="left",
                    y=1.05,
                    yanchor="top"
                )
            ]
        )

    fig.update_layout(
        xaxis=dict(
            showline=True,
            zeroline=True,
            showgrid=False,
            showticklabels=True,
            linecolor="#114B5F",
            linewidth=0.1,
            ticks="outside",
            tickcolor="#BBBBBB",
            gridcolor="#F8FAFA",
            tickfont=dict(family="Roboto", size=12, color="#114B5F",),
            dtick=10,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#F8FAFA",
            zeroline=False,
            showline=True,
            showticklabels=True,
            linecolor="#114B5F",
            linewidth=0.1,
            ticks="outside",
            tickcolor="#BBBBBB",
            tickfont=dict(family="Roboto", size=12, color="#114B5F"),
        ),
        showlegend=False,
        legend=dict(font=dict(family="Roboto", size=12, color="#114B5F")),
        paper_bgcolor="#E6ECEC",
        plot_bgcolor="#E6ECEC",
        title=dict(
            text="<b>Θάνατοι</b> και <b>διασωληνωμένοι</b> ασθενείς στην Ελλάδα",
            font=dict(family="Roboto", size=16, color="#114B5F"),
        ),
        hoverlabel=dict(font_size=10, font_family="Roboto"),
        hovermode="closest",
    )

    fig.update_layout(height=450, margin=dict(l=10, r=10, b=10, t=90, pad=0))

    if show:
        config = dict(
            {
                "displayModeBar": True,
                "scrollZoom": False,
                "displaylogo": False,
                "responsive": True,
                "staticPlot": False,
            }
        )
        fig.show(config=config)
    fig.write_json(name + ".json")


"""φορτώνουμε το αρχείο που επιθυμούμε, τον αριθμό σημείο έναρξης της οπτικοποίησης,
το όνομα της νέας στήλης που θα δημιουργηθεί από το melt, 
το όνομα του αρχείου που θέλουμε να σώσουμε"""


def after100Cases(
    data,
    countries_data,
    population,
    numberCompare,
    columnName,
    outputName,
    titleGraphic,
    keyWordHover,
    xAxis,
    yAxis,
    show=False,
):
    """ φορτώνουμε το πρώτο αρχείο από το Hopkins"""
    df = (
        data.drop(["Lat", "Long"], axis=1)
        .melt(
            id_vars=["Province/State", "Country/Region"],
            var_name="Date",
            value_name=columnName,
        )
        .astype({"Date": "datetime64[ns]", columnName: "Int64"}, errors="ignore")
    )

    """ φορτώνουμε το αρχείο με την αντιστοίχιση ελληνικών - αγγλικών ονομάτων χωρών"""
    gr = countries_data
    """ το συνδέουμε με το dataframe από το Hopkins ώστε να προστεθεί το ADMIN_GR"""
    df = pd.merge(df, gr, how="left", left_on="Country/Region", right_on="ADMIN")

    """ φορτώνουμε το αρχείο με τους πληθυσμούς"""
    pop = population
    """συνδέουμε το dataframe με τα ελληνικά ονόματα """
    gr = pd.merge(gr, pop, how="right", left_on="ADMIN", right_on="Country,Other")

    """Ενώνουμε το dataframe του Hopkins και εκείνο του population με βάση την στήλη με τα ελληνικά ονόματα"""
    df = pd.merge(df, gr, how="left", on="ADMIN_GR")

    """ υπολογίζουμε συγκεντρωτικά για κάθε χώρα τα κρούσματα και τους θανάτους ανά ημέρα"""
    df = (
        df.groupby(["Country/Region", "Date", "ADMIN_GR", "Population (2020)"])[
            columnName
        ]
        .sum()
        .reset_index()
    )

    """ ------------------- ΞΕΚΙΝΑ Η ΟΠΤΙΚΟΠΟΙΗΣΗ ------------------"""

    """ Φτιάχνουμε ένα variable που ΔΕΝ ΘΑ ΠΕΡΙΕΧΕΙ τις χώρες αναφοράς - που θα χρωματίσουμε με άλλο χρώμα"""
    cnt = df[
        (df["Country/Region"] != "Greece")
        & (df["Country/Region"] != "Germany")
        & (df["Country/Region"] != "Italy")
        & (df["Country/Region"] != "United Kingdom")
        & (df["Country/Region"] != "US")
        & (df["Country/Region"] != "Spain")
        & (df["Country/Region"] != "China")
    ]

    fig = px.line(
        cnt[
            (cnt["Country/Region"] != "Diamond Princess")
            & (cnt[columnName] >= numberCompare)
        ],
        y=columnName,
        color="ADMIN_GR",
        hover_data=["ADMIN_GR"],
        labels={"Date": "Ημερομηνία", columnName: keyWordHover, "ADMIN_GR": "Χώρα"},
        title=titleGraphic,
        line_shape="spline",
        render_mode="svg",
        color_discrete_sequence=["rgb(189,189,189)"],
    )

    fig.update_layout(
        paper_bgcolor="#E6ECEC",
        plot_bgcolor="#E6ECEC",
        font=dict(family="Roboto", size=11, color="#114B5F"),
    )

    fig.update_layout(
        hovermode="closest",
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Roboto"),
        hoverlabel_align="left",
    )

    fig.update_layout(showlegend=True)
    fig.update_layout(
        legend_title="Διπλό κλικ σε κάθε<br>χώρα για να την <br>απομονώσετε<br>",
        legend=dict(
            traceorder="reversed",
            font=dict(family="roboto", size=10, color="black"),
            bgcolor="#E6ECEC",
            bordercolor="#dadada",
            borderwidth=0.3,
        ),
    )

    fig.update_yaxes(
        nticks=4,
        showticklabels=True,
        showline=True,
        linewidth=2,
        linecolor="#114B5F",
        showgrid=True,
        gridwidth=0.1,
        gridcolor="#F8FAFA",
        title_text=yAxis,
        title_font={"size": 11, "color": "#114B5F"},
    )

    fig.update_xaxes(
        ticks=None,
        showticklabels=True,
        showline=False,
        linewidth=0.1,
        linecolor="#F8FAFA",
        showgrid=True,
        gridwidth=0.1,
        gridcolor="#F8FAFA",
        title_text=xAxis,
        title_font={"size": 11, "color": "#114B5F"},
    )

    fig.update_layout(xaxis_showgrid=True, yaxis_showgrid=True)

    fig.update_layout(yaxis_type="log")

    fig.update_layout(height=380)

    # Γερμανία
    fig.add_trace(
        go.Scatter(
            y=df[
                (df["Country/Region"] == "Germany") & (df[columnName] > numberCompare)
            ][columnName],
            name="Γερμανία",
            line=dict(color="black", width=2),
            hovertemplate="<b>{}</b> στην Γερμανία<extra></extra>".format(
                "%{y:.f} " + keyWordHover
            ),
        )
    )

    # Ιταλία
    fig.add_trace(
        go.Scatter(
            y=df[(df["Country/Region"] == "Italy") & (df[columnName] > numberCompare)][
                columnName
            ],
            name="Ιταλία",
            line=dict(color="#3E82B3", width=2),
            hovertemplate="<b>{}</b> στην Ιταλία<extra></extra>".format(
                "%{y:.f} " + keyWordHover
            ),
        )
    )

    # UK
    fig.add_trace(
        go.Scatter(
            y=df[
                (df["Country/Region"] == "United Kingdom")
                & (df[columnName] > numberCompare)
            ][columnName],
            name="Ηνωμένο Βασίλειο",
            line=dict(color="#FFD400", width=2),
            hovertemplate="<b>{}</b> στο Ηνωμένο Βασίλειο<extra></extra>".format(
                "%{y:.f} " + keyWordHover
            ),
        )
    )

    # USA
    fig.add_trace(
        go.Scatter(
            y=df[(df["Country/Region"] == "US") & (df[columnName] > numberCompare)][
                columnName
            ],
            name="ΗΠΑ",
            line=dict(color="lightgreen", width=2),
            hovertemplate="<b>{}</b> στις ΗΠΑ<extra></extra>".format(
                "%{y:.f} " + keyWordHover
            ),
        )
    )
    # Spain
    fig.add_trace(
        go.Scatter(
            y=df[(df["Country/Region"] == "Spain") & (df[columnName] > numberCompare)][
                columnName
            ],
            name="Ισπανία",
            line=dict(color="purple", width=2),
            hovertemplate="<b>{}</b> στην Ισπανία<extra></extra>".format(
                "%{y:.f} " + keyWordHover
            ),
        )
    )
    # Greece
    fig.add_trace(
        go.Scatter(
            y=df[(df["Country/Region"] == "Greece") & (df[columnName] > numberCompare)][
                columnName
            ],
            name="Ελλάδα",
            line=dict(color="#BA3A0A", width=3),
            hovertemplate="<b>{}</b> στην Ελλάδα<extra></extra>".format(
                "%{y:.f} " + keyWordHover
            ),
        )
    )

    # μέγεθος γραμμής σε κάθε χώρα στο legend, trace/constant
    fig.update_layout(
        legend={"itemsizing": "constant"},
        annotations=[
            dict(
                x=0,
                y=1,
                xref="paper",
                yref="paper",
                text="Δεν περιλαμβάνεται η Κίνα.<br><i>Λογαριθμική κλίμακα</i>",
                showarrow=False,
                align="left",
            )
        ],
    )
    fig.update_layout(height=380, margin=dict(l=10, r=10, b=10, t=65, pad=10))

    if show:
        config = dict(
            {
                "displayModeBar": True,
                "scrollZoom": False,
                "displaylogo": False,
                "responsive": True,
                "staticPlot": False,
            }
        )
        fig.show(config=config)
    fig.write_json(outputName)


def heatmap(
    data,
    countries_df,
    population,
    columnName,
    outputName,
    titleGraphic,
    keyWord,
    show=False,
):
    """ φορτώνουμε το πρώτο αρχείο από το Hopkins"""
    df = data.drop(["Lat", "Long"], axis=1)
    """ υπολογίζουμε το difference από ημέρα σε ημέρα, ώστε να βγάλουμε τα ΝΕΑ κρούσματα/θάνατοι ανά ημέρα"""
    cols = df.columns.to_list()
    df_dif = df[cols[4:]].diff(axis=1)
    df = df_dif.join(df["Country/Region"])
    """ αλλάζουμε τα data από wide σε long + μετρέπουμε τη στήλη Date σε datetime"""
    df = pd.melt(
        df, id_vars=["Country/Region"], var_name="Date", value_name=columnName
    ).astype({"Date": "datetime64[ns]", columnName: "Int64"}, errors="ignore")

    """ φορτώνουμε το αρχείο με την αντιστοίχιση ελληνικών - αγγλικών ονομάτων χωρών"""
    gr = countries_df
    """ το συνδέουμε με το dataframe από το Hopkins ώστε να προστεθεί το ADMIN_GR"""
    df = pd.merge(df, gr, how="left", left_on="Country/Region", right_on="ADMIN")

    """ φορτώνουμε το αρχείο με τους πληθυσμούς"""
    pop = population
    """συνδέουμε το dataframe με τα ελληνικά ονόματα """
    gr = pd.merge(gr, pop, how="right", left_on="ADMIN", right_on="Country,Other")

    """Ενώνουμε το dataframe του Hopkins και εκείνο του population με βάση την στήλη με τα ελληνικά ονόματα"""
    df = pd.merge(df, gr, how="left", on="ADMIN_GR")

    """ υπολογίζουμε συγκεντρωτικά για κάθε χώρα τα κρούσματα και τους θανάτους ανά ημέρα"""
    df = (
        df.groupby(["Country/Region", "Date", "ADMIN_GR", "Population (2020)"])[
            columnName
        ]
        .sum()
        .reset_index()
    )

    """ ------------------- ΠΡΟΕΤΟΙΜΑΖΟΥΜΕ ΤΗ ΣΤΗΛΗ ΠΟΥ ΘΑ ΟΠΤΙΚΟΠΟΙΗΣΟΥΜΕ -----------------"""
    df[columnName + "_per_hundr"] = (df[columnName] / df["Population (2020)"]) * 100000

    """ ------------------- ΕΠΙΛΕΓΟΥΜΕ ΤΙΣ ΧΩΡΕΣ ΜΕ ΠΑΡΟΜΟΙΟ ΠΛΗΘΥΣΜΟ ΜΕ ΤΗΝ ΕΛΛΑΔΑ -----------"""

    df = df[
        (df["Population (2020)"] > 9000000)
        & (df["Population (2020)"] < 12000000)
        & (df["Date"] > "2020-03-06")
        & (df["Country/Region"] != "Portugal")
    ]

    """ ------------------- ΞΕΚΙΝΑ Η ΟΠΤΙΚΟΠΟΙΗΣΗ ------------------"""

    countries = df["ADMIN_GR"]
    item = df[columnName + "_per_hundr"]
    base = datetime.datetime.today()
    dates = df["Date"]

    fig = go.Figure(
        data=go.Heatmap(
            z=item,
            x=dates,
            y=countries,
            customdata=df[columnName],
            showscale=True,
            hovertemplate="<b>%{y}</b><br>"
            + "<i>%{x}</i><br><br>"
            + "%{customdata} "
            + keyWord
            + "<extra></extra>",
            colorscale=[
                [0, "#E6ECEC"],  # 0
                [1.0 / 10000, "#dadada"],  # 10
                [1.0 / 1000, "#d7dfe3"],  # 100
                [1.0 / 100, "#b0bfc7"],  # 1000
                [1.0 / 10, "#3f6678"],  # 10000
                [1.0, "#BA3A0A"],
            ],
            colorbar=dict(
                title=keyWord + "/<br>100 χιλ ",
                tick0=0,
                tickmode="auto",  # όταν το tickmode είναι array, τότε παίρνει τα values του tickvals
                tickvals=[0, 1000, 1800],
            ),
        )
    )

    fig.update_layout(title=titleGraphic)

    fig.update_layout(
        hovermode="closest",
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Roboto"),
        hoverlabel_align="left",
    )

    fig.update_layout(
        paper_bgcolor="#E6ECEC",
        plot_bgcolor="#E6ECEC",
        font=dict(family="Roboto", size=11, color="#114B5F"),
    )

    fig.update_layout(height=400, margin=dict(l=10, r=10, b=20, t=75, pad=10))


    if show:
        config = dict(
            {
                "displayModeBar": True,
                "scrollZoom": False,
                "displaylogo": False,
                "responsive": True,
                "staticPlot": False,
            }
        )

    fig.write_json(outputName)


def create_chrolopleth_casesrate(name, wom_data, countries_data, token, show=False):
    wom = wom_data

    countries_names = countries_data
    countries_names = countries_names.rename(columns={"ADMIN": "Country,Other"})
    wom = pd.merge(wom, countries_names, on="Country,Other", how="left")

    wom["Tot Cases/1M pop"] = (wom["Tot Cases/1M pop"]).apply(lambda x: parseFloat(x))
    wom["Deaths/1M pop"] = (wom["Deaths/1M pop"]).apply(lambda x: parseFloat(x))
    wom["Tests/ 1M pop"] = (wom["Tests/ 1M pop"]).apply(lambda x: parseFloat(x))

    wom["testing_median_diff_pct"] = (
        (wom["Tests/ 1M pop"] - wom["Tests/ 1M pop"].median())
        / wom["Tests/ 1M pop"].median()
    ) * 100
    wom["cases_rate_normalized"] = (wom["Tot Cases/1M pop"] * 100) / wom[
        "Tests/ 1M pop"
    ]
    wom["cases_rate_normalized"] = wom["cases_rate_normalized"].round(2)
    wom["cases_rate_median_diff_pct"] = (
        (wom["cases_rate_normalized"] - wom["cases_rate_normalized"].median())
        / wom["cases_rate_normalized"].median()
    ) * 100

    res = requests.get(
        "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"
    )
    countries = res.json()

    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=countries,
            locations=wom.iso_alpha_3,
            z=wom.cases_rate_normalized.astype(float),
            colorscale=[("#3f6678"), ("#BA3A0A")],
            zmin=wom.cases_rate_normalized.min(),
            zmax=wom.cases_rate_normalized.max(),
            text=wom["ADMIN_GR"],
            marker_line_width=0.5,
            #                                     marker_line_color='grey',
            colorbar_title="%",
            colorbar=dict(tick0=0, dtick=20),
        )
    )

    fig.update_layout(
        mapbox_style="mapbox://styles/trilikis/ck916mr2y0wox1iozbu71xkw6",
        mapbox_accesstoken=token,
        mapbox_zoom=-1,
        mapbox_center={"lat": 41.902782, "lon": 12.496366},
    )

    fig.update_layout(
        paper_bgcolor="#E6ECEC",
        plot_bgcolor="#E6ECEC",
        margin=dict(l=20, r=0, t=50, b=50),
        title=dict(
            text="<br><b>Κρούσματα</b> αναλογικά με τα τεστ ανά χώρα<br>",
            y=0.98,
            x=0.02,
            xanchor="left",
            yanchor="top",
            font=dict(family="Roboto", size=16, color="#114B5F"),
        ),
        annotations=[
            dict(
                x=0,
                y=-0.1,
                xref="paper",
                yref="paper",
                text="Οι διαφορετικές πολιτικές των χωρών ως προς τα τεστ <br>μπορεί να οδηγούν σε υποεκτιμήσεις ή υπερεκτιμήσεις.",
                showarrow=False,
                visible=True,
                align="left",
                font=dict(family="Roboto", color="#114B5F", size=10),
            )
        ],
    )

    if show:
        config = dict(
            {
                "displayModeBar": True,
                "scrollZoom": False,
                "displaylogo": False,
                "responsive": True,
                "staticPlot": False,
            }
        )
        fig.show(config=config)
    fig.write_json(name + ".json")


def create_chrolopleth_recoveredrate(name, wom_data, countries_data, token, show=False):
    wom = wom_data

    countries_names = countries_data
    countries_names = countries_names.rename(columns={"ADMIN": "Country,Other"})
    wom = pd.merge(wom, countries_names, on="Country,Other", how="left")

    wom["Tot Cases/1M pop"] = (wom["Tot Cases/1M pop"]).apply(lambda x: parseFloat(x))
    wom["Deaths/1M pop"] = (wom["Deaths/1M pop"]).apply(lambda x: parseFloat(x))
    wom["Tests/ 1M pop"] = (wom["Tests/ 1M pop"]).apply(lambda x: parseFloat(x))

    wom["TotalCases"] = (wom["TotalCases"]).apply(lambda x: parseFloat(x))
    wom["TotalRecovered"] = (wom["TotalRecovered"]).apply(lambda x: parseFloat(x))

    wom["testing_median_diff_pct"] = (
        (wom["Tests/ 1M pop"] - wom["Tests/ 1M pop"].median())
        / wom["Tests/ 1M pop"].median()
    ) * 100
    wom["cases_rate_normalized"] = (wom["Tot Cases/1M pop"] * 100) / wom[
        "Tests/ 1M pop"
    ]
    wom["cases_rate_normalized"] = wom["cases_rate_normalized"].round(2)
    wom["cases_rate_median_diff_pct"] = (
        (wom["cases_rate_normalized"] - wom["cases_rate_normalized"].median())
        / wom["cases_rate_normalized"].median()
    ) * 100
    wom["recovered_rate"] = (wom["TotalRecovered"] * 100) / wom["TotalCases"]
    wom["recovered_rate"] = wom["recovered_rate"].round(2)

    res = requests.get(
        "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"
    )
    countries = res.json()

    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=countries,
            locations=wom.iso_alpha_3,
            z=wom.recovered_rate.astype(float),
            colorscale=["#3f6678", "#FFC100"],
            zmin=wom.recovered_rate.min(),
            zmax=wom.recovered_rate.max(),
            text=wom["ADMIN_GR"],
            marker_line_width=0.5,
            #                                     marker_line_color='grey',
            colorbar_title="%",
            colorbar=dict(tick0=0, dtick=20),
        )
    )

    fig.update_layout(
        mapbox_style="mapbox://styles/trilikis/ck916mr2y0wox1iozbu71xkw6",
        mapbox_accesstoken=token,
        mapbox_zoom=-1,
        mapbox_center={"lat": 41.902782, "lon": 12.496366},
    )

    fig.update_layout(
        paper_bgcolor="#E6ECEC",
        plot_bgcolor="#E6ECEC",
        margin=dict(l=20, r=0, t=50, b=50),
        title=dict(
            text="<br>Όσοι <b>ανάρρωσαν</b> ανά χώρα<br>",
            y=0.98,
            x=0.02,
            xanchor="left",
            yanchor="top",
            font=dict(family="Roboto", size=16, color="#114B5F"),
        ),
        annotations=[
            dict(
                x=0,
                y=-0.1,
                xref="paper",
                yref="paper",
                text="ανάρρωσαν/κρούσματα (%)<br>Οι διαφορετικές πολιτικές των χωρών ως προς την<br>καταγραφή των στοιχείων μπορεί να επηρεάζουν τα αποτελέσματα.",
                showarrow=False,
                visible=True,
                align="left",
                font=dict(family="Roboto", color="#114B5F", size=10),
            )
        ],
    )

    if show:
        config = dict(
            {
                "displayModeBar": True,
                "scrollZoom": False,
                "displaylogo": False,
                "responsive": True,
                "staticPlot": False,
            }
        )
        fig.show(config=config)
    fig.write_json(name + ".json")


def create_regions_facets(name, regions_greece_deaths_data, show=False):
    deaths = regions_greece_deaths_data
    deaths = deaths.drop(["pop_11"], axis=1)
    deaths["district"] = deaths.district.str.replace("Περιφέρεια", "")
    deaths["district"] = deaths.district.str.replace(
        "Μακεδονίας Θράκης", "Μακεδονίας & Θράκης"
    )
    deaths = deaths[
        (deaths.district != "Χωρίς Μόνιμη Κατοικία στην Ελλάδα")
        & (deaths.district != "Χωρίς Γεωγραφικό Προσδιορισμό")
    ]
    deaths = deaths.melt(
        id_vars=["district"], var_name="Date", value_name="deaths"
    ).astype({"Date": "datetime64[ns]", "deaths": "Int64"})
    deaths = pd.DataFrame(
        deaths.groupby(["district", "Date"]).deaths.sum().reset_index()
    )
    deaths = deaths[deaths.deaths > 0]

    fig = px.area(
        deaths,
        y="deaths",
        x="Date",
        facet_col="district",
        facet_col_wrap=2,
        labels={
            "district": "Περιφέρεια",
            "Date": "Ημ/νία",
            "deaths": "Θάνατοι συνολικά",
        },
    )

    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.for_each_annotation(lambda a: a.update(text=a.text.replace("Περιφέρεια", "")))

    fig["layout"]["yaxis"]["title"]["text"] = ""
    fig["layout"]["yaxis3"]["title"]["text"] = ""
    fig["layout"]["yaxis5"]["title"]["text"] = ""
    fig["layout"]["yaxis7"]["title"]["text"] = ""
    fig["layout"]["xaxis2"]["title"]["text"] = ""
    fig["layout"]["xaxis1"]["title"]["text"] = ""

    fig.update_layout(
        height=450,
        xaxis=XAXIS_STYLE,
        xaxis2=XAXIS_STYLE,
        yaxis=YAXIS_STYLE,
        yaxis3=YAXIS_STYLE,
        yaxis5=YAXIS_STYLE,
        yaxis7=YAXIS_STYLE,
        yaxis2=YAXIS_STYLE2,
        yaxis4=YAXIS_STYLE2,
        yaxis6=YAXIS_STYLE2,
        yaxis8=YAXIS_STYLE2,
        showlegend=False,
        paper_bgcolor="#E6ECEC",
        plot_bgcolor="#E6ECEC",
        title=dict(text="Εξέλιξη <b>θανάτων</b> ανά <b>Περιφέρεια</b>", font=TEXTFONT),
        # margin=dict(l=10, r=10, b=10, t=90, pad=0),
        hoverlabel=dict(font_size=8, font_family="Roboto"),
        yaxis3_title=dict(
            text="",
            font=dict(family="Roboto", size=8, color="#114B5F"),
        ),
        xaxis_title=dict(
            text="<i>Δεν περιλαμβάνονται θάνατοι με άγνωστο γεωγραφικό προσδιορισμό.</i>",
            font=dict(family="Roboto", size=8, color="#114B5F"),
        ),
        hovermode="closest",
    )


    for annot in fig.layout.annotations:
        annot.update(font=dict(family="Roboto", size=8, color="#114B5F"))

    fig.update_traces(line=dict(color="#BA3A0A"))

    fig.update_layout(height=450, margin=dict(l=10, r=10, b=10, t=90, pad=0))

    if show:
        config = dict(
            {
                "displayModeBar": True,
                "scrollZoom": False,
                "displaylogo": False,
                "responsive": True,
                "staticPlot": False,
            }
        )

        fig.show(config=config)
    fig.write_json(name + ".json")


def growth_rate(
    data,
    countries_data,
    population,
    numberCompare,
    columnName,
    outputName,
    titleGraphic,
    keyWordHover,
    xAxis,
    yAxis,
    show=False,
):
    """ φορτώνουμε το πρώτο αρχείο από το Hopkins"""
    df = (
        data.drop(["Lat", "Long"], axis=1)
        .melt(
            id_vars=["Province/State", "Country/Region"],
            var_name="Date",
            value_name=columnName,
        )
        .astype({"Date": "datetime64[ns]", columnName: "Int64"}, errors="ignore")
    )

    """ φορτώνουμε το αρχείο με την αντιστοίχιση ελληνικών - αγγλικών ονομάτων χωρών"""
    gr = countries_data
    """ το συνδέουμε με το dataframe από το Hopkins ώστε να προστεθεί το ADMIN_GR"""
    df = pd.merge(df, gr, how="left", left_on="Country/Region", right_on="ADMIN")

    """ φορτώνουμε το αρχείο με τους πληθυσμούς"""
    pop = population
    """συνδέουμε το dataframe με τα ελληνικά ονόματα """
    gr = pd.merge(gr, pop, how="right", left_on="ADMIN", right_on="Country,Other")

    """Ενώνουμε το dataframe του Hopkins και εκείνο του population με βάση την στήλη με τα ελληνικά ονόματα"""
    df = pd.merge(df, gr, how="left", on="ADMIN_GR")

    """ υπολογίζουμε συγκεντρωτικά για κάθε χώρα τα κρούσματα και τους θανάτους ανά ημέρα"""
    df = (
        df.groupby(["Country/Region", "Date", "ADMIN_GR", "Population (2020)"])[
            columnName
        ]
        .sum()
        .reset_index()
    )

    df["7_day_avg_growth"] = (
        df.groupby(["Country/Region"])[columnName].pct_change().rolling(window=7).mean()
        * 100
    ).round(1)

    """ ------------------- ΞΕΚΙΝΑ Η ΟΠΤΙΚΟΠΟΙΗΣΗ ------------------"""

    """ Φτιάχνουμε ένα variable που ΔΕΝ ΘΑ ΠΕΡΙΕΧΕΙ τις χώρες αναφοράς - που θα χρωματίσουμε με άλλο χρώμα"""
    cnt = df[
        (df["Country/Region"] != "Greece")
        & (df["Country/Region"] != "Germany")
        & (df["Country/Region"] != "Italy")
        & (df["Country/Region"] != "United Kingdom")
        & (df["Country/Region"] != "US")
        & (df["Country/Region"] != "Spain")
        & (df["Country/Region"] != "China")
    ]

    fig = go.Figure()
    fig.update_layout(
        paper_bgcolor="#E6ECEC",
        title=titleGraphic,
        plot_bgcolor="#E6ECEC",
        font=dict(family="Roboto", size=11, color="#114B5F"),
    )

    fig.update_layout(
        hovermode="closest",
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Roboto"),
        hoverlabel_align="left",
    )

    fig.update_layout(showlegend=True)
    fig.update_layout(
        legend_title="Διπλό κλικ σε κάθε<br>χώρα για να την <br>απομονώσετε<br>",
        legend=dict(
            traceorder="reversed",
            font=dict(family="roboto", size=10, color="black"),
            bgcolor="#E6ECEC",
            bordercolor="#dadada",
            borderwidth=0.3,
        ),
    )

    fig.update_yaxes(
        nticks=8,
        rangemode="tozero",
        showticklabels=True,
        showline=True,
        linewidth=2,
        linecolor="#114B5F",
        showgrid=True,
        gridwidth=0.1,
        gridcolor="#F8FAFA",
        title_text=yAxis,
        title_font={"size": 11, "color": "#114B5F"},
    )

    fig.update_xaxes(
        ticks=None,
        rangemode="tozero",
        showticklabels=True,
        showline=False,
        linewidth=0.1,
        linecolor="#F8FAFA",
        showgrid=True,
        gridwidth=0.1,
        gridcolor="#F8FAFA",
        title_text=xAxis,
        title_font={"size": 11, "color": "#114B5F"},
    )

    fig.update_layout(yaxis_type="log")

    fig.update_layout(height=380)

    # world - Dataframe για μετά την 1η Μαρτίου
    world = df[(df["Date"] > "2020-03-01")]
    last_day = world["Date"].max()
    countries_with_increased = world[
        (world.Date == last_day) & (world["7_day_avg_growth"] > numberCompare)
    ]["Country/Region"].tolist()

    # DataFrame με τις χώρες που έχουν ρυθμό αύξησης άνω του numberCompare
    world_df = world[world["Country/Region"].isin(countries_with_increased)]

    fig.add_trace(
        go.Scatter(
            y=world_df["7_day_avg_growth"],
            x=world_df["Date"],
            name="<i>Χώρες με<br>>{}% αύξηση<br> {}<br>τις τελευταίες<br>7 ημέρες</i>".format(
                numberCompare, keyWordHover
            ),
            line=dict(color="gray", width=0.2),
            text=[i for i in world_df["ADMIN_GR"]],
            hovertemplate="<b>{}</b><br><i>{}</i><br>{} αύξηση {} <extra></extra>".format(
                "%{text}", "%{x}", "%{y:.f}% ", keyWordHover
            ),
            showlegend=True,
        )
    )
    # Γερμανία
    fig.add_trace(
        go.Scatter(
            y=world[(world["Country/Region"] == "Germany")]["7_day_avg_growth"],
            x=world["Date"],
            name="Γερμανία",
            line=dict(color="black", width=2),
            hovertemplate="<b>{}</b><br>{}αύξηση {} στη Γερμανία<extra></extra>".format(
                "%{x}", "%{y:.f}% ", keyWordHover
            ),
        )
    )
    # Ιταλία
    fig.add_trace(
        go.Scatter(
            y=world[(world["Country/Region"] == "Italy")]["7_day_avg_growth"],
            x=world["Date"],
            name="Ιταλία",
            line=dict(color="#3E82B3", width=2),
            hovertemplate="<b>{}</b><br>{}αύξηση {} στην Ιταλία<extra></extra>".format(
                "%{x}", "%{y:.f}% ", keyWordHover
            ),
        )
    )
    # UK
    fig.add_trace(
        go.Scatter(
            y=world[(world["Country/Region"] == "United Kingdom")]["7_day_avg_growth"],
            x=world["Date"],
            name="Ηνωμένο Βασίλειο",
            line=dict(color="#FFD400", width=2),
            hovertemplate="<b>{}</b><br>{}αύξηση {} στο Ηνωμένο Βασίλειο<extra></extra>".format(
                "%{x}", "%{y:.f}% ", keyWordHover
            ),
        )
    )

    # USA
    fig.add_trace(
        go.Scatter(
            y=world[(world["Country/Region"] == "US")]["7_day_avg_growth"],
            x=world["Date"],
            name="ΗΠΑ",
            line=dict(color="lightgreen", width=2),
            hovertemplate="<b>{}</b><br>{}αύξηση {} στις ΗΠΑ<extra></extra>".format(
                "%{x}", "%{y:.f}% ", keyWordHover
            ),
        )
    )

    # Spain
    fig.add_trace(
        go.Scatter(
            y=world[(world["Country/Region"] == "Spain")]["7_day_avg_growth"],
            x=world["Date"],
            name="Ισπανία",
            line=dict(color="purple", width=2),
            hovertemplate="<b>{}</b><br>{} αύξηση {} στην Ισπανία<extra></extra>".format(
                "%{x}", "%{y:.f}% ", keyWordHover
            ),
        )
    )
    # Greece
    fig.add_trace(
        go.Scatter(
            y=world[(world["Country/Region"] == "Greece")]["7_day_avg_growth"],
            x=world["Date"],
            name="Ελλάδα",
            line=dict(color="#BA3A0A", width=3),
            hovertemplate="<b>{}</b><br>{} αύξηση {} στην Ελλάδα<extra></extra>".format(
                "%{x}", "%{y:.f}% ", keyWordHover
            ),
        )
    )

    # μέγεθος γραμμής σε κάθε χώρα στο legend, trace/constant
    fig.update_layout(
        legend={"itemsizing": "constant"},
        annotations=[
            dict(
                x=0,
                y=1.1,
                xref="paper",
                yref="paper",
                text="<i>Η τιμή κάθε ημέρας είναι ο μέσος όρος <br>των ρυθμών μεταβολής των τελευταίων επτά ημερών</i>",
                showarrow=False,
                align="left",
            )
        ],
    )
    fig.update_layout(height=450, margin=dict(l=10, r=10, b=10, t=80, pad=0))

    if show:
        config = dict(
            {
                "displayModeBar": True,
                "scrollZoom": False,
                "displaylogo": False,
                "responsive": True,
                "staticPlot": False,
            }
        )

    fig.write_json(outputName)
