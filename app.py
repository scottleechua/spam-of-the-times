from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import os

app = Dash()
server = app.server

df = pd.read_csv("./data/text-messages.csv")

df["date-received"] = pd.to_datetime(df["date-received"]).dt.date
num_days = (df["date-received"].max() - df["date-received"].min()).days + 1

total_texts = len(df)


def text_pct_generator(category):
    count = len(df[df["category"] == category])
    pct = count * 100 / total_texts
    return pct


fig = px.histogram(
    df,
    x="date-received",
    nbins=int(num_days / 2),
    color="category",
    category_orders={"category": ["spam", "ads", "gov", "notifs", "OTP"]},
)

fig.add_vline(x="2023-07-30 12:00", line_width=2, line_dash="dash", line_color="black")

fig.add_annotation(
    text="---: SIM card<br>registration<br>deadline",
    align="right",
    showarrow=False,
    xref="paper",
    yref="paper",
    x=0.995,
    y=0.995,
    bordercolor="black",
    borderwidth=0,
)

fig.update_layout(
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    legend_title=None,
    xaxis_title=None,
    # xaxis_tickformat="%b '%y",
    xaxis_fixedrange=True,
    yaxis_fixedrange=True,
    font_family="Montserrat",
    margin=dict(b=10),
)

fig.update_xaxes(tickprefix="<br> ")
fig.update_yaxes(ticksuffix="   ")

# on first page load, show only spam and the legend
fig.update_traces(visible="legendonly")
fig.data[0].visible = True

config = {"displayModeBar": False, "showTips": False}
dropdown_choices = ["spam", "ads", "gov"]

app.layout = html.Div(
    children=[
        html.H1(children="spam of the times"),
        html.Div(
            children=[html.P(children=["download data: GitHub | Kaggle"])],
            className="download-menu",
        ),
        html.P(
            children=[
                html.Br(),
                html.Div(
                    children=[
                        "***",
                    ],
                    className="center-divider",
                ),
                html.Br(),
                "On Sep 27 2022, the Philippine Senate passed the ",
                html.A(
                    "SIM Registration Act",
                    href="https://www.philstar.com/headlines/2022/09/28/2212803/senate-approves-sim-registration-bill",
                    target="_blank",
                ),
                " in a move against SMS spam, scams, and fraud.",
            ]
        ),
        html.P(
            children=[
                "Around that time, I was fascinated by Mikko Hypponen's ",
                html.A(
                    "Malware Museum",
                    href="https://archive.org/details/malwaremuseum",
                    target="_blank",
                ),
                ", an online archive that treats computer viruses as cultural artifacts worthy of preservation and study. ",
            ]
        ),
        html.P(
            children=[
                "Two days later, I stopped deleting spam texts. In fact, I stopped deleting texts at all.",
            ]
        ),
        dcc.Graph(figure=fig, config=config),
        html.P(
            children=[
                f"I split all {total_texts:,} texts into 5 categories:",
            ]
        ),
        html.Ol(
            children=[
                html.Li(
                    children=[
                        html.Strong("spam"),
                        f" ({text_pct_generator('spam'):.0f}%): unsolicited messages from unknown numbers;",
                    ]
                ),
                html.Li(
                    children=[
                        html.Strong("ads"),
                        f" ({text_pct_generator('ads'):.0f}%): marketing I can't unsubscribe from;",
                    ]
                ),
                html.Li(
                    children=[
                        html.Strong("gov"),
                        f" ({text_pct_generator('gov'):.0f}%): PSAs and disaster warnings.",
                    ]
                ),
                html.Li(
                    children=[
                        html.Strong("notifs"),
                        f" ({text_pct_generator('notifs'):.0f}%): messages I both expect and welcome; and",
                    ]
                ),
                html.Li(
                    children=[
                        html.Strong("OTP"),
                        f" ({text_pct_generator('OTP'):.0f}%): one-time passwords.",
                    ]
                ),
            ]
        ),
        html.P(
            children=[
                "For your reading pleasure, here's every message from the first 3 categories:"
            ]
        ),
        html.Div(
            children=[
                dcc.Dropdown(
                    id="filter_dropdown",
                    options=dropdown_choices,
                    placeholder="-select-",
                    value="spam",
                    searchable=False,
                    className="custom-dropdown",
                ),
                dash_table.DataTable(
                    data=df.sort_values(by="date-received", ascending=False).to_dict(
                        "records"
                    ),  # for table view, show latest messages first
                    id="table-container",
                    columns=[{"name": "text", "id": "text"}],
                    page_action="none",
                    style_table={"height": "300px", "overflowY": "auto"},
                    style_cell={"textAlign": "left"},
                    style_header={"display": "none"},
                    style_data={
                        "whiteSpace": "normal",
                        "height": "auto",
                        "padding": "10px",
                    },
                    style_data_conditional=[
                        {
                            "if": {"row_index": "odd"},
                            "backgroundColor": "rgb(230,236,245)",
                        }
                    ],
                ),
            ],
            className="dropdown-and-table",
        ),
        html.P(
            children=[
                "As the SIM registration deadline approached, I thought this little archival exercise would soon come to an end. ",
            ]
        ),
        html.P(
            children=[
                "But at 9:41am on Jul 30 2023, the day ",
                html.A(
                    "54 million",
                    href="https://www.sunstar.com.ph/cebu/local-news/54-million-unregistered-sim-cards-deactivated",
                    target="_blank",
                ),
                " unregistered phone numbers were permanently deactivated, I got a text saying:",
            ]
        ),
        html.Div(
            children="B D O-Advisory:Your registered mobile number needs to be updated today. Please update here: https:// shorten.tv /loginnow to continue receiving One-Time Pin (OTP)",
            className="sms-div",
        ),
        html.P(children=["—and so we continue."]),
        html.Div(
            children=[
                "***",
            ],
            className="center-divider",
        ),
        html.P(
            children=[
                "The full dataset of my text messages is available under the ",
                html.A(
                    "CC-BY-4.0 license",
                    href="https://creativecommons.org/licenses/by/4.0/",
                    target="_blank",
                ),
                " on GitHub and Kaggle. I aim to update it twice a year.",
            ]
        ),
        html.P(
            children=[
                "For questions, feedback, or to get ⚠️ FREE signup instant cash!! 💰 — email scottleechua [at] gmail [dot] com."
            ]
        ),
        html.Br(),
        html.Footer(
            children=[
                html.P(
                    children=[
                        "© 2024 ",
                        html.A(
                            "Scott Lee Chua",
                            href="https://scottleechua.com",
                            target="_blank",
                        ),
                        " 🇵🇭",
                    ]
                ),
            ]
        ),
    ]
)


@app.callback(Output("table-container", "data"), Input("filter_dropdown", "value"))
def update_table(selection):
    dff = df[df["category"] == selection]
    return dff.to_dict("records")


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))
