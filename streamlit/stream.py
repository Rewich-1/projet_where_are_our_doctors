
import streamlit as st
import os



import home
import fod
import ayr
import cwa
import dwtp
import processing


###################################################################################################


st.set_page_config(
    page_title="but where is our medecin",
    page_icon="🏥",
    layout='wide'
    )

st_folder = 'sp_app_solution'
os.makedirs(st_folder, exist_ok=True)



# MENU

PAGES = {
    "summarize" :home,
    #"processing" :processing,
    "find our doctor": fod,
    "distribution with the population": dwtp,
    "changes with age": cwa,
    #"changes with gender": cwg,
    "analyze your region": ayr
    #"distribution of medical students": train

}
st.sidebar.title('🏥 Menu 🏥')
selection = st.sidebar.radio("Select your page", list(PAGES.keys()))



st.sidebar.info('👩🏼‍⚕ have fun 👨🏼‍⚕️')
st.sidebar.success('Made by jb')

page = PAGES[selection]

page.app()