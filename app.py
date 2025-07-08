"""Simple Dash-Pylint App"""

import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import Input
from dash import Output
import pandas as pd
from plotly import express as pex

# Read data
df = pd.read_csv("assets/healthcare_dataset.csv")
df["Billing Amount"] = pd.to_numeric(df["Billing Amount"])
df["Date of Admission"] = pd.to_datetime(df["Date of Admission"], format="%Y-%m-%d")
df["Year Month"] = df["Date of Admission"].dt.to_period("M")

num_records = df.shape[0]
avg_billing = round(df["Billing Amount"].mean(), 3)
num_doctors = df["Doctor"].nunique()
num_hospitals = df["Hospital"].nunique()
num_ins_provider = df["Insurance Provider"].unique().shape[0]
num_medical_conditions = df["Medical Condition"].unique().shape[0]

genders = df["Gender"].unique()

# Creating Web-App Dashboard
app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME]
)

stats1 = dbc.Card(
    [
        html.Div(
            html.H4(f"Total Patient Records: {num_records}", style={"fontSize": 20})
        ),
        html.Div(html.H4(f"Average Billing: {avg_billing}", style={"fontSize": 20})),
    ],
    body=True,
)
stats2 = dbc.Card(
    [
        html.Div(
            html.H4(
                f"Total Number of Hospitals: {num_hospitals}", style={"fontSize": 20}
            )
        ),
        html.Div(
            html.H4(
                f"Total Number of num_doctors: {num_doctors}", style={"fontSize": 20}
            )
        ),
    ],
    body=True,
)
stats3 = dbc.Card(
    [
        html.Div(
            html.H4(
                f"Total Number of Insurance Provider: {num_ins_provider}",
                style={"fontSize": 20},
            )
        ),
        html.Div(
            html.H4(
                f"Total Number of Medical Conditions: {num_medical_conditions}",
                style={"fontSize": 20},
            )
        ),
    ],
    body=True,
)

patient_demographics_filter = dbc.Card(
    [
        html.Div(
            [
                html.Div(html.H6("Patient Demographics")),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(dbc.Label("Gender")),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id="patient-gender",
                                        options=[
                                            {"label": gender, "value": gender}
                                            for gender in genders
                                        ],
                                        placeholder="Gender",
                                        value=None,
                                    )
                                ),
                            ],
                            align="center",
                            className="text-center",
                        ),
                    ]
                ),
            ]
        )
    ],
    body=True,
)

age_distribution = dbc.Card(
    [
        html.Div(html.H5("Patient Age Distribution")),
        html.Div(
            dcc.Graph(
                id="age-distribution",
                responsive=True,
                style={"width": "100%", "height": "100%"},
            )
        ),
    ],
    body=True,
)

medical_condition_distribution = dbc.Card(
    [
        html.Div(html.H5("Patient Medical Condition Distribution")),
        html.Div(
            dcc.Graph(
                id="condition-distribution",
                responsive=True,
                style={"width": "100%", "height": "100%"},
            )
        ),
    ],
    body=True,
)

insurance_provider_distribution = dbc.Card(
    [
        html.Div(html.H5("Insurance Provider Comparison")),
        html.Div(
            dcc.Graph(
                id="insurance-comparison",
                responsive=True,
                style={"width": "100%", "height": "100%"},
            )
        ),
    ],
    body=True,
)

billing_amount_distribution = dbc.Card(
    [
        html.Div(html.H5("Billing Amount Distribution")),
        html.Div(
            dcc.Slider(
                id="billing-slider",
                min=df["Billing Amount"].min(),
                max=df["Billing Amount"].max(),
                value=df["Billing Amount"].median(),
                marks={
                    int(value): f"{int(value):,}"
                    for value in df["Billing Amount"]
                    .quantile([0, 0.25, 0.50, 0.75, 1.0])
                    .values
                },
                step=100,
            )
        ),
        html.Div(
            dcc.Graph(
                id="billing-distribution",
                responsive=True,
                style={"width": "100%", "height": "100%"},
            )
        ),
    ],
    body=True,
)

trends_in_admission_filter = dbc.Card(
    [
        html.Div(
            [
                html.Div(html.H6("Controls")),
                html.Div(
                    dbc.Row(
                        [
                            dbc.Col(dbc.Label("Chart Type:")),
                            dbc.Col(
                                dcc.RadioItems(
                                    id="chart-type",
                                    options=[
                                        {"label": "Line Chart", "value": "line"},
                                        {"label": "Bar Chart", "value": "bar"},
                                    ],
                                    value="line",
                                    inline=True,
                                )
                            ),
                        ],
                        align="center",
                        className="text-center",
                    )
                ),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(dbc.Label("Condition:")),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id="condition",
                                        options=[
                                            {"label": condition, "value": condition}
                                            for condition in df[
                                                "Medical Condition"
                                            ].unique()
                                        ],
                                        placeholder="Condition",
                                        value=None,
                                    )
                                ),
                            ],
                            align="center",
                            className="text-center",
                        )
                    ]
                ),
            ]
        )
    ],
    body=True,
)

trends_in_admission_distribution = dbc.Card(
    [
        html.Div(html.H5("Trends in Admission")),
        html.Div(
            dcc.Graph(
                id="admission-trend-distribution",
                responsive=True,
                style={"width": "100%", "height": "100%"},
            )
        ),
    ],
    body=True,
)

# define the layout
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.H1("Healthcare Dashboard", className="text-center")),
            ],
            align="center",
        ),
        html.Hr(),
        # Hospital Statistics
        dbc.Row(
            [
                dbc.Col(stats1),
                dbc.Col(stats2),
                dbc.Col(stats3),
            ],
            align="center",
            className="text-center",
        ),
        # Patient Data
        dbc.Row(
            [
                dbc.Col(patient_demographics_filter, md=2),
                dbc.Col(age_distribution),
                dbc.Col(medical_condition_distribution),
            ],
            align="center",
            className="text-center mt-2",
        ),
        # Insurance Provider Data
        dbc.Row(
            [
                dbc.Col(insurance_provider_distribution),
            ],
            align="center",
            className="text-center mt-2",
        ),
        # Billing Distribution
        dbc.Row(
            [
                dbc.Col(billing_amount_distribution),
            ],
            align="center",
            className="text-center mt-2",
        ),
        # Trends In Admission
        dbc.Row(
            [
                dbc.Col(trends_in_admission_filter, md=2),
                dbc.Col(trends_in_admission_distribution),
            ],
            align="center",
            className="mb-2 text-center mt-2",
        ),
    ],
    fluid=True,
)

# Callbacks


# Age Distribution
@app.callback(Output("age-distribution", "figure"), Input("patient-gender", "value"))
def age_gender_distribution(gender):
    """Age Distribution"""

    if gender:
        filtered_df = df[df["Gender"] == gender]
    else:
        filtered_df = df

    if filtered_df.empty:
        return {}
    fig = pex.histogram(
        data_frame=filtered_df,
        x="Age",
        nbins=10,
        color="Gender",
        color_discrete_sequence=["#636EFA", "#EF553B"],
        # title="Age vs Gender Distribution"
    )
    return fig


# Medical Condition Distribution
@app.callback(
    Output("condition-distribution", "figure"), Input("patient-gender", "value")
)
def medical_condition_distribution_func(gender):
    """Medical Condition Distribution"""

    if gender:
        filtered_df = df[df["Gender"] == gender]
    else:
        filtered_df = df

    if filtered_df.empty:
        return {}
    fig = pex.pie(
        data_frame=filtered_df,
        names="Medical Condition",
        # title="Age vs Gender Distribution",
    )
    return fig


# Insurance Provider Distribution
@app.callback(
    Output("insurance-comparison", "figure"), Input("patient-gender", "value")
)
def insurance_provider_distribution_func(gender):
    """Insurance Provider Distribution"""

    if gender:
        filtered_df = df[df["Gender"] == gender]
    else:
        filtered_df = df

    if filtered_df.empty:
        return {}
    fig = pex.bar(
        data_frame=filtered_df,
        x="Insurance Provider",
        y="Billing Amount",
        color="Medical Condition",
        barmode="group",
        # title="Insurance Provider Price Distribution",
        color_discrete_sequence=pex.colors.qualitative.Dark2,
    )
    return fig


# Billing Amount Distribution
@app.callback(
    Output("billing-distribution", "figure"),
    [Input("patient-gender", "value"), Input("billing-slider", "value")],
)
def billing_amount_distribution_func(gender, amount):
    """Billing Amount Distribution"""

    if gender:
        filtered_df = df[df["Gender"] == gender]
    else:
        filtered_df = df
    if amount:
        filtered_df = filtered_df[filtered_df["Billing Amount"] <= amount]

    if filtered_df.empty:
        return {}
    fig = pex.histogram(
        data_frame=filtered_df,
        x="Billing Amount",
        nbins=10,
    )
    return fig


# Trends in Admission Distribution
@app.callback(
    Output("admission-trend-distribution", "figure"),
    [
        Input("patient-gender", "value"),
        Input("condition", "value"),
        Input("chart-type", "value"),
    ],
)
def trends_in_admission_distribution_func(gender, condition, chart_type):
    """Trends in Admission Distribution"""

    if gender:
        filtered_df = df[df["Gender"] == gender]
    else:
        filtered_df = df
    if condition:
        filtered_df = filtered_df[filtered_df["Medical Condition"] == condition]

    filtered_df = filtered_df.groupby("Year Month").size().reset_index(name="Count")
    filtered_df["Year Month"] = filtered_df["Year Month"].astype(str)
    fig = None
    if filtered_df.empty:
        fig = {}
    elif chart_type == "line":
        fig = pex.line(data_frame=filtered_df, x="Year Month", y="Count")
    elif chart_type == "bar":
        fig = pex.bar(data_frame=filtered_df, x="Year Month", y="Count")
    return fig


if __name__ == "__main__":
    app.run(debug=True)
