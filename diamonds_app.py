import streamlit as st
from frontend import main

if __name__ == '__main__':
    st.set_page_config(page_title='diamond_price_recommender_app', layout='wide', initial_sidebar_state='auto',
    menu_items={'About': "This is an mvp of a diamond price recommender app! 💎"})
    main()
