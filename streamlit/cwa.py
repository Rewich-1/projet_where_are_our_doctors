import streamlit as st
import pandas as pd
import geopandas as gpd
from streamlit_folium import folium_static
import folium
import numpy as np
import os
from collections import Counter
from sklearn.linear_model import LinearRegression


# ======================================= PAGE =======================================

def app():

    st.error('in construction 🚧', icon="🚨")
    with st.spinner('Wait for it...'):

        path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)).replace('\\','/')+'/data'

        data_geo = gpd.read_file(f"{path}//departements.geojson")
        df = pd.read_csv(f"{path}/medecins_soft.csv", sep=",")
        # df = pd.read_csv(f"{path}/medecins.csv", sep=";")
        #pop_dep = pd.read_csv(f"{path}/population_departement.csv", sep=';')
        #dp_france = pd.read_csv(f"{path}/departements-france1.csv")
        #df2 = gpd.read_file(f"{path}//departements.geojson")
        age = pd.read_csv(f"{path}/medecin_tranche_age.csv", encoding='unicode_escape')

        #pop_dep["Total"] = pop_dep["Total"].str.replace(" ", "")
        #pop_dep["Total"] = pd.to_numeric(pop_dep["Total"])
    st.success('downloaded data !')


    st.markdown('''# Find our Doctor''')
    st.caption("Source : https://annuaire.sante.fr/")
    st.caption(
        " ![Alt Text](https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Octicons-mark-github.svg/32px-Octicons-mark-github.svg.png) : https://github.com/jbc2/where_is_our_doctor")
    st.write('---')

    col1, col2 = st.columns(2)
    with col1:
        choose_profession = st.selectbox('Select your age group',age.columns[2:])  # Select ticker symbol

    with col2:
        age['code_dep'] = None
        for ind in age.index:
            if age['dep_insc'][ind][0] == '0':
                age['code_dep'][ind] = age['dep_insc'][ind][1:3]

        df2 = data_geo.merge(age, left_on='code', right_on='code_dep', how='left')
        # df2 = df2.merge(result_choose, left_on='code', right_on='Code INSEE Département')

        df2.replace(np.nan, 0)

        df2[choose_profession] = df2[choose_profession].str.replace(' ', '')
        df2[choose_profession] = pd.to_numeric(df2[choose_profession])


        #df2['9 - 65 ans et plus'] = df2['9 - 65 ans et plus'].str.replace(' ', '')
        #df2["9 - 65 ans et plus"] = pd.to_numeric(df2["9 - 65 ans et plus"])


        m = folium.Map(location=[46, 2], zoom_start=5)

        cp = folium.Choropleth(
            geo_data=df2,
            name="Light Map",
            data=df2,
            columns=["code",choose_profession],
            key_on="feature.properties.code",
            # key_on="feature.id",
            fill_color="Blues",
            fill_opacity=0.8,
            line_opacity=0.2,
            legend_name=f"numbre de medecin of {choose_profession[3:]}  en france",
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
                fields=['code', f'{choose_profession}'],
                aliases=['code', f'{choose_profession[3:]}'],
                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
            )
        )

        folium.TileLayer('CartoDB positron', name="Light Map", control=False).add_to(m)

        m.add_child(NIL)
        m.keep_in_front(NIL)
        folium_static(m)


    data_graph = age.iloc[[0]].T
    data_graph = data_graph.drop(["dep_insc"])
    data_graph = data_graph.drop(["code_dep"])
    data_graph = data_graph.drop([" Ensemble"])
    data_graph[0] = data_graph[0].str.replace(' ', '')
    data_graph[0] = pd.to_numeric(data_graph[0])

    st.bar_chart(data_graph)
    with st.expander("data"):
        st.dataframe(data_graph)






        liste1 = np.random.randint(low=28, high=29, size=(4341,))
        liste2 = np.random.randint(low=30, high=34, size=(31373,))
        liste3 = np.random.randint(low=35, high=39, size=(27529,))
        liste4 = np.random.randint(low=40, high=44, size=(22297,))
        liste5 = np.random.randint(low=35, high=39, size=(27529,))
        liste6 = np.random.randint(low=45, high=49, size=(20290,))
        liste7 = np.random.randint(low=50, high=54, size=(23089,))
        liste8 = np.random.randint(low=55, high=59, size=(28656,))
        liste9 = np.random.randint(low=60, high=64, size=(34895,))
        liste10 = np.random.randint(low=65, high=80, size=(36388,))

        my_dict = {}
        my_dict.update(dict(Counter(liste1.tolist())))
        my_dict.update(dict(Counter(liste2.tolist())))
        my_dict.update(dict(Counter(liste3.tolist())))
        my_dict.update(dict(Counter(liste4.tolist())))
        my_dict.update(dict(Counter(liste5.tolist())))
        my_dict.update(dict(Counter(liste6.tolist())))
        my_dict.update(dict(Counter(liste7.tolist())))
        my_dict.update(dict(Counter(liste8.tolist())))
        my_dict.update(dict(Counter(liste9.tolist())))
        my_dict.update(dict(Counter(liste10.tolist())))



        #st.line_chart(liste[0:100])
        #st.write(my_dict)
        df4 = pd.DataFrame([{"age": key , "Count": value} for key, value in my_dict.items()])
        df4["annee"] = 2022-df4["age"]
        df4["mean"] =  df4["Count"].expanding().mean()
        st.write(df4)
    #st.line_chart(df4, x = "age", y="Count" )
    #st.line_chart(df4, x="annee", y="mean")

    model = LinearRegression()
    model.fit(df4[["annee"]], df4["mean"])
    for i in range(1994,2030):


        df4 = df4.append({'annee': i}, ignore_index=True)
        df4.loc[df4["annee"] == i, "predict"] = model.predict([[i]])+np.random.normal(0, model.predict([[i]])/10)
    #st.write(df4)

    st.line_chart(df4, x="annee", y=["mean","predict"])


    #st.write(model.predict([[1995]]))

    #st.dataframe(liste)


    col1, col2 = st.columns(2)
    with col1:
        st.caption(" ![Alt Text](http://www.carmf.fr/chiffrescles/stats/2021/images/pyramide-cotisants-01-2021.gif)")
        st.caption("[source](http://www.carmf.fr/page.php?page=chiffrescles%2Fstats%2F2021%2Fdemographie.htm)")

    with col2:
        st.caption(" ![Alt Text](http://www.carmf.fr/chiffrescles/stats/2021/images/pyramide-retraites-01-2021.gif)")
        st.caption("[source](http://www.carmf.fr/page.php?page=chiffrescles%2Fstats%2F2021%2Fdemographie.htm)")

    with st.expander("data"):
        st.dataframe(df2[["code",choose_profession]], 400, 200)
        st.dataframe(df)
