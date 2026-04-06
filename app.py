import streamlit as st
import google.generativeai as genai
import pdfplumber

# --- 1. SETTINGS ---
st.set_page_config(page_title="Tayyaba's Gemini Job Agent", page_icon="🚀")
st.title("🤖 My Free AI Job Hunter")
st.info("Powered by Google Gemini - Free for Students!")

# Input for Google API Key
api_key = st.text_input("Enter Google Gemini API Key", type="password")

# --- 2. THE LOGIC ---
def find_jobs_with_gemini(cv_text):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    prompt = f"""
    You are a professional Career Coach in Lahore. 
    Analyze this CV text: {cv_text[:3000]}
    
    TASK: Find 3-5 real, urgent job roles that fit this person's skills.
    1. LOCATION: Priority is Lahore (Gulberg, Walton) or Remote.
    2. SALARY: For remote, target $500/month (140,000 PKR).
    3. LINKS: Provide a direct link or a Google Search link for each job.
    
    Format:
    ### [Job Title]
    - **Company:** [Name]
    - **Location:** [Area]
    - **Why it fits:** [Reason]
    - **Action:** [Link]
    """
    
    response = model.generate_content(prompt)
    return response.text

# --- 3. THE INTERFACE ---
uploaded_file = st.file_uploader("Upload your CV (PDF)", type="pdf")

if st.button("Find My Next Job"):
    if not api_key:
        st.error("Please enter your Google API Key!")
    elif uploaded_file:
        with st.spinner("Gemini is searching for jobs in Lahore..."):
            with pdfplumber.open(uploaded_file) as pdf:
                text = "".join([page.extract_text() for page in pdf.pages])
            
            results = find_jobs_with_gemini(text)
            st.success("Matching Jobs Found!")
            st.markdown(results)
