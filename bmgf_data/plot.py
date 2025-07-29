import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np # Added for numerical operations
import math      # Added for math functions

# Load data
df = pd.read_csv('global_sectors_year.csv')

# Create subplot with 2 rows
fig = make_subplots(
    rows=2, cols=1,
    subplot_titles=("Percentage Share of Funding by Sector Per Year", 
                   "Funding by Sector Over the Years"),
    vertical_spacing=0.15,
    row_heights=[0.5, 0.5]
)

# Get unique sectors and assign specific colors based on sector type
sectors = df['sector'].unique()

# Create color mapping based on sector names
color_mapping = {}
for sector in sectors:
    sector_lower = sector.lower()
    if 'health' in sector_lower:
        color_mapping[sector] = '#2ca02c'  # Green
    elif 'education' in sector_lower:
        color_mapping[sector] = '#1f77b4'  # Blue
    elif 'growth' in sector_lower or 'economic' in sector_lower or 'development' in sector_lower:
        color_mapping[sector] = '#ff7f0e'  # Orange
    elif 'equality' in sector_lower or 'gender' in sector_lower or 'equal' in sector_lower:
        color_mapping[sector] = '#e377c2'  # Magenta
    else:
        color_mapping[sector] = '#7f7f7f'  # Gray for others

# Create colors list in the same order as sectors
colors = [color_mapping[sector] for sector in sectors]

# First chart: Percentage Share (top)
for i, sector in enumerate(sectors):
    sector_data = df[df['sector'] == sector]
    fig.add_trace(
        go.Scatter(
            x=sector_data['DATE COMMITTED'],
            y=sector_data['percentage'],
            mode='lines+markers',
            name=sector,
            line=dict(color=colors[i], width=4),
            marker=dict(size=8, color=colors[i], line=dict(width=1, color='white')),
            hovertemplate='<b>%{fullData.name}</b><br>' +
                         'Year: %{x}<br>' +
                         'Percentage: %{y:.1f}%<br>' +
                         '<extra></extra>'
        ),
        row=1, col=1
    )

# Second chart: Amount Committed (bottom)
for i, sector in enumerate(sectors):
    sector_data = df[df['sector'] == sector]
    fig.add_trace(
        go.Scatter(
            x=sector_data['DATE COMMITTED'],
            y=sector_data['AMOUNT COMMITTED'],
            mode='lines+markers',
            name=sector,
            line=dict(color=colors[i], width=4),
            marker=dict(size=8, color=colors[i], line=dict(width=1, color='white')),
            showlegend=False,  # Hide legend for second chart to avoid duplication
            hovertemplate='<b>%{fullData.name}</b><br>' +
                         'Year: %{x}<br>' +
                         'Amount: %{y:$,.0s}<br>' +
                         '<extra></extra>'
        ),
        row=2, col=1
    )

# Update layout for professional appearance
fig.update_layout(
    title=dict(
        text="<b>Global Sector Trends Analysis</b>",
        x=0.5,
        font=dict(size=24, color='#2c3e50')
    ),
    height=800,
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="top",
        y=0.98,
        xanchor="center",
        x=0.5,
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="rgba(0,0,0,0.2)",
        borderwidth=1,
        font=dict(size=11)
    ),
    template="plotly_white",
    font=dict(family="Arial, sans-serif", size=12),
    plot_bgcolor="rgba(248,249,250,0.8)",
    paper_bgcolor="white"
)

# Update x-axes
fig.update_xaxes(
    title_text="Year",
    title_font=dict(size=14, color='#34495e'),
    tickfont=dict(size=12),
    gridcolor='rgba(0,0,0,0.1)',
    row=1, col=1
)
fig.update_xaxes(
    title_text="Year",
    title_font=dict(size=14, color='#34495e'),
    tickfont=dict(size=12),
    gridcolor='rgba(0,0,0,0.1)',
    row=2, col=1
)

# Update y-axes
fig.update_yaxes(
    title_text="Percentage (%)",
    title_font=dict(size=14, color='#34495e'),
    tickfont=dict(size=12),
    gridcolor='rgba(0,0,0,0.1)',
    row=1, col=1
)

# ---- START: FIX FOR Y-AXIS BILLION FORMATTING ----

# Manually calculate tick values and labels for the second chart's y-axis
# This allows us to use 'B' for billions instead of the default 'G' for giga.
max_amount = df['AMOUNT COMMITTED'].max()
tickvals, ticktext = None, None

if pd.notna(max_amount) and max_amount > 0:
    # Determine a "nice" step size for the ticks based on the data's maximum value
    if max_amount >= 4e9: step = 1e9      # Step by 1B
    elif max_amount >= 2e9: step = 5e8    # Step by 500M (0.5B)
    elif max_amount >= 1e9: step = 2.5e8  # Step by 250M (0.25B)
    elif max_amount >= 4e8: step = 1e8    # Step by 100M
    else: step = 5e7                      # Step by 50M

    # Generate an array of tick values from 0 to just above the max value
    tickvals = np.arange(0, max_amount + step, step)

    # Create a function to format the labels
    def format_currency_with_b(value):
        if value == 0: return '$0'
        # The 'g' format specifier removes insignificant trailing zeros (e.g., 1.50 -> 1.5)
        if abs(value) >= 1e9: return f'${value / 1e9:g}B'
        if abs(value) >= 1e6: return f'${value / 1e6:g}M'
        if abs(value) >= 1e3: return f'${value / 1e3:g}K'
        return f'${value:g}'

    # Apply the formatting function to our tick values
    ticktext = [format_currency_with_b(v) for v in tickvals]

# Apply the custom ticks to the second chart's y-axis
fig.update_yaxes(
    title_text="Amount Committed ($)",
    title_font=dict(size=14, color='#34495e'),
    tickfont=dict(size=12),
    gridcolor='rgba(0,0,0,0.1)',
    # tickformat='$,.0s', # This is replaced by the manual tickvals and ticktext below
    tickvals=tickvals,   # Set the calculated tick positions
    ticktext=ticktext,   # Set the custom-formatted tick labels
    row=2, col=1
)

# ---- END: FIX FOR Y-AXIS BILLION FORMATTING ----

# Add subtle styling to subplot titles
fig.update_annotations(
    font=dict(size=16, color='#2c3e50')
)

# Save as standalone HTML file
fig.write_html(
    "global_sectors_analysis.html",
    config={
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
        'toImageButtonOptions': {
            'format': 'png',
            'filename': 'global_sectors_analysis',
            'height': 800,
            'width': 1200,
            'scale': 1
        }
    },
    include_plotlyjs=True
)

print("Professional chart saved as 'global_sectors_analysis.html'")
print("You can now open this file in any web browser without needing to run a server!")

# Optional: Also display the chart if running in Jupyter/interactive environment
# fig.show()