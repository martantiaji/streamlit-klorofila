import streamlit as st
from streamlit_option_menu import option_menu
from apps import (home,geemap_script)
#import your app modules here

st.set_page_config(
    page_title="Chlorophyll-a",
    page_icon=":earth_asia:",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None)

# A dictionary of apps in the format of {"App title": "App icon"}
# More icons can be found here: https://icons.getbootstrap.com

apps = [
    {"func": home.app, "title": "Home", "icon": "house"},
    {"func": geemap_script.app, "title": "Klorofil-a", "icon": "map"},
]

titles = [app["title"] for app in apps]
icons = [app["icon"] for app in apps]

params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles.index(params["page"][0].lower()))
else:
    default_index = 0

with st.sidebar:
    selected = option_menu(
        "Menu Utama",
        options=titles,
        icons=icons,
        menu_icon="cast",
        default_index=default_index,
    )

    st.sidebar.title("Tentang")
    st.sidebar.info(
        """
        Aplikasi web ini dikelola ole Martanti Aji dengan dosen pembimbing Dr. Lalu Muhamad Jaelani S.T., M.Sc., PhD. 
        Url aplikasi web ini yaitu : [Streamlit Klorofil-a](https://share.streamlit.io/martantiaji/streamlit-klorofila)
        
        Anda dapat mengakses referensi kode : [GitHub Aji](https://github.com/martantiaji/streamlit-klorofila.git)

    """
    )

for app in apps:
    if app["title"] == selected:
        app["func"]()
        break
