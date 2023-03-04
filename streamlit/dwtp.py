import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_folium import folium_static
import folium
import numpy as np
import os




# ======================================= PAGE =======================================
def app():





    with st.spinner('Wait for it...'):
        path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)).replace('\\','/')+'/data'
        #data_geo = json.load(open(f"{path}/departements.geojson"))
       # df = pd.read_csv(f"{path}/medecins_soft.csv", sep=",")
       # df = pd.read_csv(f"{path}/medecins.csv", sep=";")
       # df = pd.read_feather(f"{path}/medecins_soft.feather")
        #df = pd.read_feather(f"{path}/medecins.feather")
        #df = pd.read_feather(f"{path}/processing/medecins_Profession_dép.feather")
        df = pd.read_feather(f"{path}/processing/PS_LibreAcces_Personne_activite.feather")
        pop_dep = pd.read_csv(f"{path}/population_departement.csv", sep=';')
        #dp_france = pd.read_csv(f"{path}/departements-france1.csv")
        df2 = gpd.read_file(f"{path}//departements.geojson")

        pop_dep["Total"] = pop_dep["Total"].str.replace(" ", "")
        pop_dep["Total"] = pd.to_numeric(pop_dep["Total"])

    st.success('downloaded data !')



    st.markdown('''# Distribution with the population''')
    st.caption("Source : https://annuaire.sante.fr/")
    st.caption(" ![Alt Text](https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Octicons-mark-github.svg/32px-Octicons-mark-github.svg.png) : https://github.com/jbc2/where_is_our_doctor")
    st.write('---')




    df2 = df2.merge(pop_dep, left_on='code', right_on='code_departements')



    st.header('Data 2022')
    choose_profession = st.selectbox('Select your medical specialty',df.drop_duplicates(subset=['Profession'])['Profession'])  # Select ticker symbol
    #choose_profession = "Médecin généraliste"
    choose_df = df[df["Profession"] == choose_profession]




    #choose_df = choose_df.drop_duplicates(subset=['Nom du professionnel'])


    df2 = df2.merge(choose_df, left_on='code', right_on='Code INSEE Département', how='left')

    df2['med sur hab'] = np.around(df2['Total'] / df2['counts'])

    m = folium.Map(location=[46, 2], zoom_start=5)

    cp = folium.Choropleth(
        geo_data=df2,
        name="Light Map",
        data=df2,
        columns=["code_departements", "med sur hab"],
        key_on="feature.properties.code",
        # key_on="feature.id",
        fill_color="Blues",
        fill_opacity=0.8,
        line_opacity=0.2,
        legend_name=f"people by doctor in {choose_profession} ",
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
            fields=['code_departements', 'Total',"counts","med sur hab"],
            aliases=['code_departements: ', 'people: ', f'number of {choose_profession}',"people by doctor"],
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
        st.write('french population')
        st.header(f'{df2.Total.sum()}')

    with col2:
        st.write(f'number of {choose_profession}')
        st.header(f'{df2["counts"].sum()}')



    mean = df2['med sur hab'].mean()

    st.write(f"mean : {mean}")
    st.header('bad region')
    cols = st.columns(3)
    for i , c in enumerate(cols):
        with c:
            x = df2.sort_values(by=['med sur hab'], ascending=False)[["Départements","med sur hab"]].iat[i, 1]
            st.metric(df2.sort_values(by=['med sur hab'], ascending=False)[["Départements","med sur hab"]].iat[i, 0],
                      x,
                      np.round((x*100)/mean),
                      delta_color="inverse"
                      )




    st.header('best region')
    cols = st.columns(3)
    for i, c in enumerate(cols):
        with c:
            x = df2.sort_values(by=['med sur hab'], ascending=True)[["Départements", "med sur hab"]].iat[i, 1]
            st.metric(df2.sort_values(by=['med sur hab'], ascending=True)[["Départements", "med sur hab"]].iat[i, 0],
                      x,
                      np.round((x * 100) / mean)
                      )

    st.header('data')
    st.bar_chart(df2, y ="med sur hab", x="Départements" )

    st.header('data annalyse')
    st.dataframe(df2[["Départements","Total","counts","med sur hab"]], 800, 200)





