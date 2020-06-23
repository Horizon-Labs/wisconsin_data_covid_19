import matplotlib.pyplot as plt
import plotly.figure_factory as ff

def graphCounties(fips, values, title="", legend_title=""):
    scope = ['Wisconsin']

    fig = ff.create_choropleth(
        fips=fips, values=values, scope=scope,
        #colorscale=colorscale, round_legend_values=True,
        simplify_county=0, simplify_state=0,
        county_outline={'color': 'rgb(15, 15, 55)', 'width': 0.5},
        state_outline={'color': 'rgb(60, 60, 200)', 'width': 1},
        legend_title=legend_title,
        title=title
    )

    fig.layout.template = None
    fig.show()

def compare(values1, values2, title=""):
    plt.scatter(values1, values2, title=title)
    plt.show()