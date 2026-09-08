import streamlit as st

st.title("Skin Sensitizer AI - Diagnostic Mode")
st.success("Streamlit server is successfully rendering components.")

try:
    import app
    st.info("Successfully imported app.py module!")
except Exception as e:
    st.error(f"Error importing app.py during execution: {e}")
    import traceback
    st.code(traceback.format_exc())
