from streamlit_extras.switch_page_button import switch_page

exec(open("pages/page_setting/setting.py").read())

switch_page('home')
