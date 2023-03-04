import streamlit as st
import pandas as pd
import os
import time




def app():
    st.error('in construction 🚧', icon="🚨")
    with st.spinner('Wait for it...'):
        path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)).replace('\\', '/') + '/data'

        #df = pd.read_csv(f"{path}//PS_LibreAcces_Personne_activite_202212080954.txt", sep='|')
        #df = pd.read_csv(f"{path}/medecins.csv", sep=";")

        #df = pd.read_feather(f"{path}/medecins_soft.feather")


    #df = pd.read_csv(f"{path}/medecins_soft.csv", sep=",")
    #df.to_feather(f"{path}/medecins_soft.feather")
    #st.write(df.dtypes)
    #st.write(df)

    start = time.time()
    #df = pd.read_csv(f"{path}/PS_LibreAcces_Personne_activite_202212080954.txt", sep="|")
    end = time.time()
    st.write('read csv')
    st.write(end - start)

    start = time.time()
    df = pd.read_feather(f"{path}/PS_LibreAcces_Personne_activite.feather")
    end = time.time()
    st.write('read feather')
    st.write(end - start)

    st.write(df.columns)

    st.write(len(df))
    choose_df = df[df["Libellé profession"] == "Médecin"]
    st.write(len(choose_df))
    st.write(len(choose_df[choose_df["Libellé savoir-faire"] == "Spécialiste en Médecine Générale"]))
    st.write(len(choose_df[choose_df["Libellé savoir-faire"] == "Qualifié en Médecine Générale"]))
    st.write(len(choose_df[choose_df["Libellé savoir-faire"] == "Médecine Générale"]))

    liste = ["Médecine Générale","Qualifié en Médecine Générale","Spécialiste en Médecine Générale"]
    st.write(len(choose_df[choose_df["Libellé savoir-faire"].isin(liste)]))
    #choose_df = choose_df[choose_df["Libellé savoir-faire"] == "Spécialiste en Médecine Générale"]
    st.write(len(choose_df))
    st.write(len(choose_df[choose_df["Code profession"] == '45']))






    choose_df = choose_df[0:50000]
    st.write(choose_df)
    #st.write(df.iloc[113]['Tarif hors secteur 1 / hors adhérent OPTAM/OPTAM-CO'].replace(',','.'))

    def convert_column(x):
        x = str(x)
        z = x.replace(',', '.')
        return float(z)

    start = time.time()
    # df['Tarif hors secteur 1 / hors adhérent OPTAM/OPTAM-CO'] = df['Tarif hors secteur 1 / hors adhérent OPTAM/OPTAM-CO'].apply(convert_column)
    end = time.time()
    st.write('replace')
    st.write(end - start)

    #st.write(df[0:1000])

    #st.write(df[0:1000])

    #st.write(df)
    start = time.time()
    #df.astype({'Tarif hors secteur 1 / hors adhérent OPTAM/OPTAM-CO': 'float64'})
    end = time.time()
    st.write('astype float64')
    st.write(end - start)

    start = time.time()
    #df.to_feather(f"{path}/PS_LibreAcces_Personne_activite.feather")
    end = time.time()
    st.write('to_feather')
    st.write(end - start)

    #st.write(df)