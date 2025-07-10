import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000"  # URL where your FastAPI backend is running

st.set_page_config(page_title="College Query Assistant", layout="centered")
st.title("🏫 College Query Assistant")

# --- Select Role ---
role = st.selectbox("Select Your Role", ["Student", "Professor", "Admin"])

# --- Select Action ---
action = st.radio("Action", ["Ask a Question", "Upload a Document"])

# --- Categories available ---
categories = ["course", "facilities", "professor", "academic", "announcements"]

# ------------------------
# 📥 Ask a Question Block
# ------------------------
if action == "Ask a Question":
    st.header("❓ Ask a Question")
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
                    if not answer or answer.lower() in ["", "i don't know", "no relevant information found"]:
                        st.subheader("📌 Answer:")
                        st.info("I don't know the answer based on the available documents.")
                    else:
                        st.subheader("📌 Answer:")
                        st.success(answer)

                    st.subheader("📄 Sources:")
                    # Show only unique file names from the sources
                    unique_files = {src["source"] for src in data.get("sources", [])}
                    if unique_files:
                        for file in unique_files:
                            st.markdown(f"- **{file}**")
                    else:
                        st.info("No source files found.")

                except Exception as e:
                    st.error(f"Error: {e}")

# -------------------------------
# 📤 Upload PDF Document Block
# -------------------------------
elif action == "Upload a Document":
    if role == "Student":
        st.warning("Only Professors and Admins can upload documents.")
    else:
        st.header("📤 Upload PDF Documents")
        uploaded_files = st.file_uploader("Choose one or more PDF files", type="pdf", accept_multiple_files=True)
        category = st.selectbox("Select Category", categories)

        if st.button("Upload"):
            if not uploaded_files:
                st.warning("Please upload at least one PDF file.")
            else:
                with st.spinner("Uploading and processing..."):
                    for uploaded_file in uploaded_files:
                        files = [("files", (uploaded_file.name, uploaded_file, "application/pdf"))]
                        data = {"category": category}

                        try:
                            response = requests.post(f"{API_BASE_URL}/upload/", files=files, data=data)
                            response.raise_for_status()
                            st.success(f"{uploaded_file.name} uploaded successfully!")
                        except requests.exceptions.RequestException as e:
                            st.error(f"Upload failed for {uploaded_file.name}: {e}")
