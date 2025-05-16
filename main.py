import streamlit as st
import google.generativeai as genai

# ----------------- API Key Configuration -----------------
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY not found. Please set it in your Streamlit secrets.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)

# ----------------- User Credentials -----------------
USER_CREDENTIALS = {
    "admin": "password123",
    "user": "codeai2024"
}

# ----------------- Gemini Code Review Function -----------------
def code_review(code, language):
    prompt = f"""
    Review the following {language} code and provide feedback on:

    - Code correctness and potential bugs
    - Code style and readability
    - Potential performance issues
    - Security vulnerabilities (if applicable)
    - Best practices and suggestions for improvement

    ```{language.lower()}
    {code}
    ```
    """
    try:
        model = genai.GenerativeModel(model_name="gemini-2.5-pro")  # Correct model name
        response = model.generate_content(
            [prompt],
            generation_config={
                "temperature": 0.7,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 2048,
            }
        )
        return response.text
    except Exception as e:
        return f"❌ Error during code review: {e}"

# ----------------- Login UI -----------------
def login_ui():
    st.set_page_config(page_title="Login - Gemini Code Reviewer", layout="centered")
    st.title("🔐 Login to Gemini Code Reviewer")
    st.write("Enter your credentials below:")

    input_username = st.text_input("Username", key="login_username")
    input_password = st.text_input("Password", type="password", key="login_password")
    login_button = st.button("Login")

    if login_button:
        if input_username in USER_CREDENTIALS and USER_CREDENTIALS[input_username] == input_password:
            st.session_state["authenticated"] = True
            st.session_state["username"] = input_username
            st.success("✅ Login successful!")
            st.rerun()
        else:
            if input_username not in USER_CREDENTIALS:
                st.error("❌ Invalid username.")
            else:
                st.error("❌ Incorrect password.")

# ----------------- Main App UI -----------------
def app_ui():
    st.set_page_config(page_title="AI Code Reviewer", layout="wide")
    st.markdown(f"## 🤖 Welcome, `{st.session_state['username']}`")
    st.markdown("Review your code with **Gemini AI**!")

    col1, col2 = st.columns([1, 2], gap="medium")

    with col1:
        language = st.selectbox("🔤 Select Language", [
            "Python", "JavaScript", "Java", "C++", "C#", "Go", "Ruby", "PHP", "Swift", "Kotlin"
        ])
        uploaded_file = st.file_uploader("📁 Or upload a file", type=[
            "py", "js", "java", "cpp", "cs", "go", "rb", "php", "swift", "kt"
        ])
        file_code = uploaded_file.read().decode("utf-8") if uploaded_file else ""

    with col2:
        code_input = st.text_area("💻 Enter your code here", height=300, value=file_code)

    if st.button("🚀 Review Code"):
        if not code_input.strip():
            st.warning("⚠️ Please enter some code.")
        else:
            with st.spinner("🔍 Reviewing..."):
                result = code_review(code_input, language)
                st.subheader("📝 Code Review")
                with st.expander("Click to view feedback"):
                    st.write(result)

    if st.button("🔓 Logout"):
        st.session_state.clear()
        st.success("🔄 Logged out. Please refresh to login again.")

# ----------------- Router -----------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
    app_ui()
else:
    login_ui()
