from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = Dash()
df = pd.read_csv("./data/sms.csv")

df["date-received"] = pd.to_datetime(df["date-received"]).dt.date
num_days = (df["date-received"].max() - df["date-received"].min()).days + 1

fig = px.histogram(df, x="date-received", nbins=int(num_days / 2), color="type")

fig.add_vline(x="2023-07-25 12:00", line_width=2, line_dash="dash", line_color="black")

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
    xaxis_fixedrange=True,
    yaxis_fixedrange=True,
    font_family="Montserrat",
)

# on first page load, show only spam and the legend
fig.update_traces(visible="legendonly")
fig.data[0].visible = True

config = {"displayModeBar": False}
dropdown_choices = ["spam", "ads", "gov"]

app.layout = html.Div(
    children=[
        html.H1(children="spam of the times"),
        html.P(children="Click on the legend to toggle."),
        dcc.Graph(figure=fig, config=config),
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
            ),  # reverse chronological
            id="table-container",
            columns=[{"name": "text", "id": "text"}],
            page_action="none",
            style_table={"height": "300px", "overflowY": "auto"},
            style_cell={"textAlign": "left"},
            style_header={"display": "none"},
            style_data={"whiteSpace": "normal", "height": "auto", "padding": "10px"},
            style_data_conditional=[
                {"if": {"row_index": "odd"}, "backgroundColor": "rgb(230,236,245)"}
            ],
        ),
    ]
)


@app.callback(Output("table-container", "data"), Input("filter_dropdown", "value"))
def update_table(selection):
    dff = df[df["type"] == selection]
    return dff.to_dict("records")


if __name__ == "__main__":
    app.run(debug=False)
