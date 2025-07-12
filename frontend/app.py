import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000"  # Update if deployed elsewhere

st.set_page_config(page_title="College Query Assistant", layout="centered")
st.title("🏫 College Query Assistant")

#Select Role
role = st.selectbox("Select Your Role", ["Student", "Professor", "Admin"])

#Select Action
action = st.radio("Action", ["Ask a Question", "Upload a Document"])

# Categories available
categories = ["course", "facilities", "professor", "academic", "announcements"]

#Ask a Question Block #
if action == "Ask a Question":
    st.header(" Ask a Question")
    question = st.text_area("Enter your question")
    category = st.selectbox("Select Category (optional)", ["None"] + categories)

    if st.button("Get Answer"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            params = {"question": question}
            if category != "None":
                params["category"] = category

            with st.spinner("Searching for answer..."):
                try:
                    response = requests.get(f"{API_BASE_URL}/query/", params=params)
                    response.raise_for_status()
                    data = response.json()

                    answer = data.get("answer", "").strip()
                    st.subheader("Answer:")
                    if answer.lower().startswith("i'm sorry") or answer.lower() in ["", "i don't know"]:
                        st.info("I don't know the answer based on the available documents.")
                    else:
                        st.success(answer)

                except Exception as e:
                    st.error(f"Error: {e}")

# Upload PDF Document
elif action == "Upload a Document":
    if role == "Student":
        st.warning("Only Professors and Admins can upload documents.")
    else:
        st.header(" Upload PDF Documents")
        uploaded_files = st.file_uploader("Choose one or more PDF files", type="pdf", accept_multiple_files=True)
        category = st.selectbox("Select Category", categories)

        if st.button("Upload"):
            if not uploaded_files:
                st.warning("Please upload at least one PDF file.")
            else:
                with st.spinner("Uploading and processing..."):
                    files = [("files", (f.name, f, "application/pdf")) for f in uploaded_files]
                    data = {"category": category}

                    try:
                        response = requests.post(f"{API_BASE_URL}/upload/", files=files, data=data)
                        response.raise_for_status()
                        result = response.json()

                        if response.status_code == 207:
                            st.warning(result["message"])
                            for fail in result["failed"]:
                                st.error(f"{fail['file']} failed: {fail['error']}")
                        else:
                            st.success("All files uploaded and processed successfully!")

                    except requests.exceptions.RequestException as e:
                        st.error(f"Upload failed: {e}")
