import streamlit as st
import openai
import pdfplumber

# --- 1. SETTINGS ---
st.set_page_config(page_title="Tayyaba's Job Agent", page_icon="🎯")
st.title("🤖 My Personal Job Hunter")
st.info("Target: Lahore (Gulberg/Walton) & $140k PKR+ Remote Jobs")

# Put your OpenAI Key here (Get it from platform.openai.com)
API_KEY = st.text_input("Enter OpenAI API Key", type="password")

# --- 2. THE LOGIC ---
def find_jobs(cv_text):
    openai.api_key = API_KEY
    prompt = f"""
    You are a professional recruiter in Pakistan. 
    Analyze this CV: {cv_text[:2000]}
    
    TASK: Find 3-5 CURRENT job openings for a MERN/AI student.
    1. LOCATION: Priority 1: Lahore (Gulberg, Walton). Priority 2: Remote.
    2. SALARY: For remote, must be approx $500/month (140,000 PKR).
    3. SPEED: Only list 'Urgent' or 'Easy Apply' roles.
    
    OUTPUT: Provide Title, Company, Location, and a DIRECT SEARCH LINK.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# --- 3. THE INTERFACE ---
uploaded_file = st.file_uploader("Upload your CV (PDF)", type="pdf")

if st.button("Find My Next Job"):
    if not API_KEY:
        st.error("Please enter your API Key first!")
    elif uploaded_file:
        with st.spinner("Searching Gulberg & Walton for matches..."):
            with pdfplumber.open(uploaded_file) as pdf:
                text = "".join([page.extract_text() for page in pdf.pages])
            
            results = find_jobs(text)
            st.success("Jobs Found!")
            st.markdown(results)
