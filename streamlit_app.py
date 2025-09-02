import streamlit as st
import squadbase.streamlit as sq
import os
import tempfile
from pathlib import Path

from temp import _get_host_from_headers, _extract_subdomain, _get_cookies_from_headers

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

# Get Squadbase user information
user_info = sq.auth.get_user()

# Store in session state for reuse
st.session_state['user_info'] = user_info

# Access user data
st.write(f"Welcome, {user_info.get('firstName', '')} {user_info.get('lastName', '')}")

st.write("---")

st.write(user_info)

st.write("---")

st.write("# DEBUGGING")

headers = getattr(st.context, "headers", None)
st.write("Headers:", headers)

host = _get_host_from_headers(headers)
st.write("Host:", host)

subdomain = _extract_subdomain(host)
st.write("Subdomain:", subdomain)

cookies = _get_cookies_from_headers(headers)
st.write("Cookies:", cookies)

st.write("---")

st.header("📁 File Upload & Download")

uploaded_file = st.file_uploader("Choose a file", type=None)

if uploaded_file is not None:
    temp_dir = Path("/tmp")
    if not temp_dir.exists():
        temp_dir = Path(tempfile.gettempdir())
    
    file_path = temp_dir / uploaded_file.name
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")
    st.write(f"File saved to: {file_path}")
    st.write(f"File size: {uploaded_file.size} bytes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with open(file_path, "rb") as f:
            st.download_button(
                label="📥 Download file",
                data=f.read(),
                file_name=uploaded_file.name,
                mime=uploaded_file.type or "application/octet-stream"
            )
    
    with col2:
        if st.button("🗑️ Delete file"):
            try:
                os.remove(file_path)
                st.success(f"File '{uploaded_file.name}' deleted from temporary storage")
            except Exception as e:
                st.error(f"Error deleting file: {e}")

st.write("---")

st.subheader("📂 List files in /tmp")
if st.button("List temporary files"):
    temp_dir = Path("/tmp")
    if not temp_dir.exists():
        temp_dir = Path(tempfile.gettempdir())
    
    try:
        files = list(temp_dir.glob("*"))[:20]
        if files:
            st.write(f"Files in {temp_dir} (showing max 20):")
            for file in files:
                if file.is_file():
                    st.write(f"- {file.name} ({file.stat().st_size} bytes)")
        else:
            st.write(f"No files found in {temp_dir}")
    except Exception as e:
        st.error(f"Error listing files: {e}")
