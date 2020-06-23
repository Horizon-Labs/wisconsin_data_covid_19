import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import numpy as np

codes = [55001,55003,55005,55007,55009,55011,55013,55015,55017,55019,55021,55023,55025,55027,55029,55031,55033,55035,55037,55039,55041,55043,55045,55047,55049,55051,55053,55055,55057,55059,55061,55063,55065,55067,55069,55071,55073,55075,55077,55078,55079,55081,55083,55085,55087,55089,55091,55093,55095,55097,55099,55101,55103,55105,55107,55109,55111,55113,55115,55117,55119,55121,55123,55125,55127,55129,55131,55133,55135,55137,55139,55141]

def graphCounties( values, fips = codes, title="", legend_title=""):
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
    print("Correlation: ", np.corrcoef(values1, values2)[0][1])
    plt.scatter(values1, values2)
    plt.show()