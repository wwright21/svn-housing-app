import streamlit as st

# - - - PAGE SETUP - - -
home_sales = st.Page(
    page='views/home_sales.py',
    title='Home Sales',
    icon=':material/real_estate_agent:'
)

permits = st.Page(
    page='views/permits.py',
    title='Building Permits',
    icon=':material/construction:'
)

demographics = st.Page(
    page='views/demographics.py',
    title='Demographics',
    icon=':material/group:'
)


# - - - NAVIGATION SETUP - - -
pg = st.navigation(
    pages=[
        home_sales,
        permits,
        demographics,
    ])

# - - - SHARED ON ALL PAGES - - -
st.logo('Assets/logo.png')

# - - - RUN NAVIGATION - - -
pg.run()

# the custom CSS lives here:
hide_default_format = """
        <style>
            MainMenu, footer {
                visibility: hidden;
                height: 0%;
            }
            [data-testid="stHeader"] {
                display: none;
            }
            section.main > div:has(~ footer ) {
                padding-bottom: 1px;
                padding-top: 2px;
            }
            [data-testid="stDecoration"] {
                display: none;
                }
            [class="stDeployButton"] {
                display: none;
            }
            .stActionButton {
                visibility: hidden;
            }
            [data-testid="stSidebarNavItems"] {
                font-size: 18px;
            }
        </style>
       """


# inject the CSS
st.markdown(hide_default_format, unsafe_allow_html=True)
