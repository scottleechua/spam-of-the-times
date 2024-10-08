from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import flask
import pandas as pd
import os

meta_tags = [
    {
        "name": "description",
        "content": "a personal history of spam, marketing, and other text messages.",
    },
    {"name": "google", "content": "nositelinkssearchbox"},
    {"property": "og:title", "content": "spam of the times"},
    {
        "property": "og:description",
        "content": "a personal history of spam, marketing, and other text messages.",
    },
    {
        "property": "og:image",
        "content": "https://raw.githubusercontent.com/scottleechua/spam-of-the-times/main/assets/header_spamofthetimes.png",
    },
    {
        "property": "og:image:alt",
        "content": "screenshot of a chart entitled 'spam of the times' showing the count of spam texts received per day betwen September 2022 and February 2024",
    },
    {"property": "twitter:title", "content": "spam of the times"},
    {"property": "twitter:card", "content": "summary_large_image"},
    {
        "property": "twitter:description",
        "content": "a personal history of spam, marketing, and other text messages.",
    },
    {
        "property": "twitter:image",
        "content": "https://raw.githubusercontent.com/scottleechua/spam-of-the-times/main/assets/header_spamofthetimes.png",
    },
    {
        "property": "twitter:image:alt",
        "content": "screenshot of a chart entitled 'spam of the times' showing the count of spam texts received per day betwen September 2022 and February 2024",
    },
    {"name": "robots", "content": "noarchive"},  # prevent Microsoft AI scraping
]


app = Dash(meta_tags=meta_tags)
app.title = "spam of the times"
app.index_string = """
<!DOCTYPE html>
<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='en'>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <script data-goatcounter="https://spamott.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""
server = app.server

df = pd.read_csv("text-messages.csv")
# df = pd.read_csv("https://raw.githubusercontent.com/scottleechua/data/main/spam-and-marketing-sms/text-messages.csv")

df["date-received"] = pd.to_datetime(df["date-received"]).dt.date
num_days = (df["date-received"].max() - df["date-received"].min()).days + 1
latest_month = df["date-received"].max().strftime("%b %Y")
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
fig.add_vline(x="2024-07-22 12:00", line_width=2, line_dash="dash", line_color="red")

fig.add_annotation(
    text="---: SIM card<br>     registration<br>     deadline",
    align="left",
    showarrow=False,
    xref="paper",
    yref="paper",
    x=0.01,
    y=0.995,
    font=dict(color="black"),
    borderwidth=0,
)

fig.add_annotation(
    text="---: POGOs<br>     banned<br>     in the PH",
    align="left",
    showarrow=False,
    xref="paper",
    yref="paper",
    x=0.01,
    y=0.845,
    font=dict(color="red"),
    borderwidth=0,
)

fig.update_layout(
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    legend_title=None,
    xaxis_title=None,
    xaxis_fixedrange=True,
    yaxis_fixedrange=True,
    font_family="Montserrat",
    margin=dict(l=30, r=40, b=10),
)

fig.update_xaxes(tickprefix="<br>")
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
            children=[
                html.P(
                    children=[
                        "dataset: ",
                        html.A(
                            "GitHub",
                            href="https://github.com/scottleechua/data/tree/main/spam-and-marketing-sms",
                            target="_blank",
                        ),
                        " | ",
                        html.A(
                            "Kaggle",
                            href="https://www.kaggle.com/datasets/scottleechua/ph-spam-marketing-sms-w-timestamps",
                            target="_blank",
                        ),
                    ]
                )
            ],
            className="download-menu",
        ),
        html.P(
            children=[
                html.Div(
                    children=[
                        html.Br(),
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
                "Two days later, I stopped deleting spam texts. In fact, I stopped deleting texts at all.",
            ]
        ),
        dcc.Graph(figure=fig, config=config, style={"width": "100%", "padding": "0"}),
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
                "We usually consider spam as digital detritus: something that clogs the servers, something to junk, something to purge. We feel like this should be a solved problem by now, and yet the only texts we ever get are spam."
            ]
        ),
        html.P(
            children=[
                "But in the way one can learn a lot about someone by going through their trash — what they had for lunch, what they bought, what they buy into — perhaps one can also learn about a society by the spam it tries to erase."
            ]
        ),
        html.P(
            children=[
                "Or perhaps not! But we'll never know unless we study it, and we can't study it without preserving it."
            ]
        ),
        html.Div(
            children=[
                html.Br(),
                "***",
            ],
            className="center-divider",
        ),
        html.P(
            children=[
                f"By {latest_month}, I had archived {total_texts:,} texts in total. Instead of the usual ",
                html.A(
                    "'spam vs. ham'",
                    href="https://cwiki.apache.org/confluence/display/spamassassin/Ham",
                    target="_blank",
                ),
                " binary labels commonly seen in ",
                html.A(
                    "spam detection training datasets",
                    href="https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset",
                    target="_blank",
                ),
                ", I ended up sorting texts into five categories:",
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
                "The complete data dictionary and metadata are on ",
                html.A(
                    "GitHub",
                    href="https://github.com/scottleechua/data/tree/main/spam-and-marketing-sms",
                    target="_blank",
                ),
                ", but for your reading pleasure, here's every message from the first three categories:",
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
                    style={"width": "100%"},
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
                    cell_selectable=False,
                ),
            ],
            className="dropdown-and-table",
        ),
        html.P(
            children=[
                html.Br(),
                "This is usually the part where — having sliced and diced the data every which way — I present you with the results of some statistical tests and draw some conclusions. I haven't done that here. And I could say that I haven't had the time, that the day job is busy and the nights are just packed.",
            ]
        ),
        html.P(
            children=[
                "But the truth is that I just don't want to. The charts you see on this page are more than enough for me. As the data collector ",
                html.B("and"),
                " the data subject, it's nice to take a step back and look at the shape of the thing, the outline of a life traced by the spam that sticks to it the way that barnacles accrue beneath a ship. It feels like being at my own funeral, like hearing someone else summarize my life. ",
                html.Em(
                    "He requested so many one-time passwords last May. Isn't that so him?"
                ),
            ]
        ),
        html.P(
            children=[
                "Last year, as the SIM registration deadline approached, I thought this little archival exercise would soon conclude itself. ",
                "But at 09:41 on the final day, the day ",
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
        html.P(children=["—and I let out a breath I didn't know I'd been holding."]),
        html.Div(
            children=[
                "***",
            ],
            className="center-divider",
        ),
        html.P(
            children=[
                "The full dataset of my text messages is freely available on ",
                html.A(
                    "GitHub",
                    href="https://github.com/scottleechua/data/tree/main/spam-and-marketing-sms",
                    target="_blank",
                ),
                " and ",
                html.A(
                    "Kaggle",
                    href="https://www.kaggle.com/datasets/scottleechua/ph-spam-marketing-sms-w-timestamps",
                    target="_blank",
                ),
                " under the ",
                html.A(
                    "CC-BY-4.0 license",
                    href="https://creativecommons.org/licenses/by/4.0/",
                    target="_blank",
                ),
                ".",
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
                        "favicon from ",
                        html.A(
                            "Flaticon",
                            href="https://www.flaticon.com/free-icons/old-phone",
                            target="_blank",
                        ),
                        html.Br(),
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


@app.server.route("/robots.txt")
def serve_robots():
    return flask.send_file("static/robots.txt", mimetype="text/plain")


@app.server.route("/sitemap.xml")
def serve_sitemap():
    return flask.send_file("static/sitemap.xml", mimetype="application/xml")


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))
