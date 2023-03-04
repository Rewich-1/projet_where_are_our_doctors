import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_folium import folium_static
import folium


import datetime
import numpy as np
from sklearn.linear_model import LinearRegression
import time
import plotly.graph_objects as go
import plotly.express as px
import time
import datetime as dt
from datetime import date, timedelta ,datetime
import os
import gc
import sys


# ======================================= PAGE =======================================
def app():
    with st.spinner('Wait for it...'):

        path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)).replace('\\','/')+'/data'

        data_geo = gpd.read_file(f"{path}//departements.geojson")
        #df = pd.read_csv(f"{path}/medecins_soft.csv", sep=",")
        #df = pd.read_csv(f"{path}/medecins.csv", sep=";")
        #df = pd.read_feather(f"{path}/medecins_soft.feather")
        #df = pd.read_feather(f"{path}/processing/medecins_Profession_dép.feather")
        df = pd.read_feather(f"{path}/processing/PS_LibreAcces_Personne_activite.feather")
        #df = pd.read_feather(f"{path}/medecins.feather")

        #pop_dep = pd.read_csv(f"{path}/population_departement.csv", sep=';')
        #dp_france = pd.read_csv(f"{path}/departements-france1.csv")
        #df2 = gpd.read_file(f"{path}//departements.geojson")

        #pop_dep["Total"] = pop_dep["Total"].str.replace(" ", "")
        #pop_dep["Total"] = pd.to_numeric(pop_dep["Total"])

    st.success('downloaded data !')



    st.markdown('''# Find our Doctor''')
    st.caption("Source : https://annuaire.sante.fr/")
    st.caption(
        "![Alt Text](https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Octicons-mark-github.svg/32px-Octicons-mark-github.svg.png) : https://github.com/jbc2/where_is_our_doctor")
    st.write('---')



    choose_profession = st.selectbox('Select your medical specialty',df.drop_duplicates(subset=['Profession'])['Profession'])


    #choose_profession = "Médecin généraliste"
    choose_df = df[df["Profession"] == choose_profession]




    #choose_df = choose_df.drop_duplicates(subset=['Nom du professionnel'])
    #result_choose = choose_df.groupby('Code INSEE Département')['Code INSEE Département'].count().reset_index(name="count")
    df2 = data_geo.merge(choose_df, left_on='code', right_on='Code INSEE Département', how='left')



    m = folium.Map(location=[46, 2], zoom_start=5)

    cp = folium.Choropleth(
        geo_data=df2,
        name="Light Map",
        data=df2,
        columns=["Code INSEE Département", "counts"],
        key_on="feature.properties.code",
        # key_on="feature.id",
        fill_color="Blues",
        fill_opacity=0.8,
        line_opacity=0.2,
        legend_name=f"répartition des {df2['counts'].sum()} {choose_profession} en france",
        overlay=True)

    m.add_child(cp)
    style_function = lambda x: {'fillColor': '#ffffff',
                                'color': '#000000',
                                'fillOpacity': 0.1,
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000',
                                    'color': '#000000',
                                    'fillOpacity': 0.50,
                                    'weight': 0.1}
    NIL = folium.features.GeoJson(
        df2,
        style_function=style_function,
        control=False,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(
            fields=['code', 'counts'],
            aliases=['code: ', 'counts: '],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
        )
    )

    folium.TileLayer('CartoDB positron', name="Light Map", control=False).add_to(m)

    m.add_child(NIL)
    m.keep_in_front(NIL)



    folium_static(m)

    st.header('Some data')
    col1, col2 = st.columns(2)

    with col1:
        st.write(f'mean of {choose_profession} by region')
        st.header(f'{choose_df["counts"].mean()}')

    with col2:
        st.write(f'number of {choose_profession}')
        st.header(f'{df2["counts"].sum()}')

    col1, col2 = st.columns(2)
    with col1:
        st.header('classement')
        st.dataframe(df2[['nom', 'counts']], 400, 200)
    with col2:
        df2["counts"].mean()

        df2 = df2.loc[df2["counts"] >  df2["counts"].quantile(.80)]
        rest = df2.loc[df2["counts"] <  df2["counts"].quantile(.80)]



        rest = pd.DataFrame(data={  'nom': "reste",
                                    'counts': rest["counts"].sum()
                                    }, index=[0]
                            )

        df2 = pd.concat([df2, rest])


        pie_chart = px.pie(df2[['nom', 'counts']],
                           title=f'distribution of {choose_profession}',
                           values="counts",
                           names="nom"
                           )
        st.plotly_chart(pie_chart)





































