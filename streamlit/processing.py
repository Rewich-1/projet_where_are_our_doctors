import streamlit as st
import pandas as pd
import os




def app():
    st.error('in construction 🚧', icon="🚨")


    with st.spinner('Wait for download the data'):
        path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)).replace('\\', '/') + '/data'

        #data_geo = gpd.read_file(f"{path}//departements.geojson")
        #df = pd.read_csv(f"{path}/medecins_soft.csv", sep=",")
        #if os.path.isfile(f"{path}/processing/medecins_Profession_dép.feather"):
            #df = pd.read_feather(f"{path}/processing/medecins_Profession_dép.feather")
        #else:
        #df = pd.read_csv(f"{path}/medecins.csv", sep=";")

        df = pd.read_csv(f"{path}/PS_LibreAcces_Personne_activite_202212080954.txt", sep="|")
        #df = pd.read_feather(f"{path}/medecins_soft.feather")
        #df = pd.read_feather(f"{path}/medecins.feather")

        #pop_dep = pd.read_csv(f"{path}/population_departement.csv", sep=';')
        #dp_france = pd.read_csv(f"{path}/departements-france1.csv")
        #df2 = gpd.read_file(f"{path}//departements.geojson")
        #age = pd.read_csv(f"{path}/medecin_tranche_age.csv", encoding='unicode_escape')
        #Personne_activite = pd.read_feather(f"{path}/PS_LibreAcces_Personne_activite.feather")

        #pop_dep["Total"] = pop_dep["Total"].str.replace(" ", "")
        #pop_dep["Total"] = pd.to_numeric(pop_dep["Total"])

    st.success('downloaded data !')

    with st.expander("departements"):
        st.write('ok')
        #st.write(data_geo[0:1000])
    with st.expander("medecins_soft"):
        st.write('ok')
        st.write(df[0:100000])
    with st.expander("population_departement"):
        st.write('ok')
        #st.write(pop_dep[0:1000])
    with st.expander("medecin_tranche_age"):
        st.write('ok')
        #.write(age[0:1000])
    with st.expander("PS_LibreAcces_Personne_activite"):
        st.write('ok')
        #st.write(Personne_activite[0:1000])




    ############################################################ procession
    with st.spinner('data processing..'):
        #df.drop_duplicates(subset=['Nom du professionnel'])
        #df = df[["Profession","Code INSEE Département"]]
        #df = df.groupby(["Profession","Code INSEE Département"]).size().reset_index(name='counts')
        df = df[df["Libellé profession"] == "Médecin"]

        st.write('end')

    st.success('data processing')

    with st.expander("departements"):
        st.write('ok')
        #st.write(data_geo[0:1000])
    with st.expander("medecins_soft"):
        st.write('ok')
        st.write(df[0:100000])
        df = df[["Libellé savoir-faire", "Code commune (coord. structure)"]]
        df["Code commune (coord. structure)"] = df['Code commune (coord. structure)'].astype(str).str[0:2]
        df["Code commune (coord. structure)"] = df['Code commune (coord. structure)'].astype(str).replace('na', 0)

        df["Libellé savoir-faire"] = df['Libellé savoir-faire'].replace('Qualifié en Médecine Générale', "Médecine Générale")
        df["Libellé savoir-faire"] = df['Libellé savoir-faire'].replace('Spécialiste en Médecine Générale',"Médecine Générale")


        df = df.groupby(["Libellé savoir-faire", "Code commune (coord. structure)"]).size().reset_index(name='counts')
        df = df.rename(
            columns={"Libellé savoir-faire": "Profession", "Code commune (coord. structure)": "Code INSEE Département"})
        st.write(df)
    with st.expander("population_departement"):
        st.write('ok')
        #st.write(pop_dep[0:1000])
    with st.expander("medecin_tranche_age"):
        st.write('ok')
        #st.write(age[0:1000])
    with st.expander("PS_LibreAcces_Personne_activite"):
        st.write('ok')
        #st.write(Personne_activite[0:1000])

    ############################################################ change format feather

    with st.spinner('change format..'):
        st.write('end')
        #df.to_feather(f"{path}/processing/medecins_Profession_dép.feather")

        df.to_feather(f"{path}/processing/PS_LibreAcces_Personne_activite.feather")

    st.success('format changed')














