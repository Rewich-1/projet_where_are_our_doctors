import streamlit as st
import pandas as pd
import geopandas as gpd
from streamlit_folium import folium_static
import folium
import os






def app():
    st.error('in construction 🚧', icon="🚨")
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

    st.success('downloaded data !')


    st.markdown('''# Analyze your region''')
    st.caption("Source : https://annuaire.sante.fr/")
    st.caption(
        " ![Alt Text](https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Octicons-mark-github.svg/32px-Octicons-mark-github.svg.png) : https://github.com/jbc2/where_is_our_doctor")
    st.write('---')

    choose_region = st.selectbox('Select your region',data_geo['nom'])
    region_df = data_geo[data_geo["nom"] == choose_region]
    code = list(region_df["code"])


    m = folium.Map(location=[46, 2], zoom_start=5)
    cp = folium.Choropleth(
        geo_data=region_df,
        name="Light Map",
        key_on="feature.properties.code",
        fill_color="Blues",
        fill_opacity=0.8,
        line_opacity=0.2,

        overlay=True)
    m.add_child(cp)
    style_function = lambda x: {'fillColor': '#4C81B7',
                                'color': '#4C81B7',
                                'fillOpacity': 0.1,
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#4C81B7',
                                    'color': '#4C81B7',
                                    'fillOpacity': 0.50,
                                    'weight': 0.1}
    NIL = folium.features.GeoJson(
        region_df,
        style_function=style_function,
        control=False,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(
            fields=["nom"],
            aliases=["nom"],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
        )
    )
    folium.TileLayer('CartoDB positron', name="Light Map", control=False).add_to(m)
    m.add_child(NIL)
    m.keep_in_front(NIL)

    col1, col2 = st.columns(2)
    with col1:
        folium_static(m)
    #st.dataframe(df[0:1000])
    with col2:
        df = df
        df.drop(df[df['Code INSEE Département'] == '0'].index, inplace=True)
        sum_count = df.groupby('Code INSEE Département').sum()
        sum_count.reset_index(inplace=True)
        sum_count['rank'] = sum_count['counts'].rank(ascending=False)
        classement = list(sum_count[sum_count["Code INSEE Département"] == code[0]]['rank'])
        st.header(f"♨️Classement ♨️")
        st.header(f"✅ {classement[0]}/100")
        st.header(f"👨🏼‍⚕️ {list(sum_count[sum_count['Code INSEE Département'] == code[0]]['counts'])[0]}")

    #st.dataframe(sum_count)
    #st.dataframe(df)
    sum_count = pd.merge(df, sum_count, how='inner')

    df['rank_counts_Departement'] = df.groupby('Code INSEE Département')['counts'].rank(ascending=False)
    test = df.drop_duplicates(subset=['Code INSEE Département'])
    #st.dataframe(sum_count)



    #profession
    #df['rank'] = df[["Profession","counts"]].rank(ascending=False)
    df['rank_Profession'] = df.groupby('Profession')['counts'].rank(ascending=False)
    code = list(region_df["code"])
    medecin_region = df[df["Code INSEE Département"] == code[0]]

    #st.dataframe(medecin_region[0:1000])
    #st.dataframe(medecin_region[0:1000])

    st.header("counts")
    st.bar_chart(medecin_region, y=["counts"], x="Profession")
    st.header("rank_Profession")
    st.bar_chart(medecin_region, y=["rank_Profession"], x="Profession")

    with st.expander("missing profession"):
        unique_profession = df.drop_duplicates(subset=['Profession'])['Profession']
        missing_profession = pd.merge(unique_profession,medecin_region, how='outer')
        missing_profession = missing_profession[missing_profession["counts"].isnull()]
        st.dataframe(missing_profession["Profession"],use_container_width=True)

    with st.expander("data"):
        st.dataframe(medecin_region,use_container_width=True)
        st.dataframe(df, use_container_width=True)




























