import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import plotly.express as px
import plotly.io as pio

pio.renderers.default = "browser"
if __name__ == '__main__':
    '''
    In this code, I am going to scrape data from santemontreal.qc.ca website for covid case distribution 
    on montreal island. Then I am going to make a dashboard and expand on it for interactivities... Maybe add different
    regions? or add another set of data like rent price.
    '''

    # First let's scrape the data.

    url = 'https://santemontreal.qc.ca/en/public/coronavirus-covid-19/' \
          'situation-of-the-coronavirus-covid-19-in-montreal/#c43674'
    r = requests.get(url).content
    soup = BeautifulSoup(r, 'html.parser')
    table = soup.select_one('#c46934 > div.csc-textpic-text > div:nth-child(7)').table
    columns = [col.text.replace('\xa0', ' ') for col in table.thead.tr.select('th')]
    # The column names are pretty long. Let's just make a new list...
    columns = ['City', 'New cases in 24 Hrs', 'Cases last 14 Days',
               'Cases per 100K last 14 Days', 'Cumulative cases', 'Cumulative cases per 100K']
    body_data = []
    for tr in table.tbody.select('tr'):
        body_data.append([td.text for td in tr.select('td')])
    df = pd.DataFrame(body_data, columns=columns)

    # Now clean the data. First, get rid of all non-numeric values in table body and convert them to appropriate dtype.
    for i in range(1, len(df.columns)):
        # remove commas
        col = df[df.columns[i]]
        col.str.replace(',', '')
        df[df.columns[i]] = pd.to_numeric(col.str.replace('\D+', ''))
    df.drop(df.index[-2:], inplace=True)

    with open('rsc/mtl_geojson.json') as f:
        mtl_geojson = json.load(f)

    # Bunch of different naming schemes. Trying to unify them.

    # For Dataframe.
    df[df.columns[0]] = df[df.columns[0]].str.replace('Le ' , '')
    df[df.columns[0]] = df[df.columns[0]].str.replace('La ' , '')
    df[df.columns[0]] = df[df.columns[0]].str.replace('Les ' , '')
    df[df.columns[0]] = df[df.columns[0]].str.replace('- ', '-')
    df[df.columns[0]] = df[df.columns[0]].str.replace(' ', '-')
    df[df.columns[0]] = df[df.columns[0]].str.replace('–', '-')

    # for json file
    replace_dict = {'Le ' : '', 'La ': '', 'Les ':'', ' ':'-'}
    for dist in mtl_geojson['features']:
        for word, initial in replace_dict.items():
            dist['properties']['NOM'] = dist['properties']['NOM'].replace(word, initial)

    # location looks for the column of the dataframe that matcheds with "id" field of json.
    # If you don't have "id" in json, use featuredidkey to manually select the field that matches with df data.
    fig = px.choropleth(df, geojson=mtl_geojson, locations=df.columns[0], color=df.columns[2],
                        featureidkey="properties.NOM",
                        range_color=(0, df[df.columns[2]].max()),
                        )
    fig.update_geos(fitbounds="locations", visible=True)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()