import streamlit as st 
from openai import OpenAI
from PyPDF2 import PdfReader

client=OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

st.title("AI Resume Analyzer")
# st.info("check ats score and improve resume ats score")

st.sidebar.header("Settings")

analysis_type=st.sidebar.selectbox("choose one",[ "Basic Review","ATS Score",  "Improvement Suggestions",
        "Full Analysis"])


def extract_text(pdf_file):
    text=""
    reader=PdfReader(pdf_file)
    for i in reader.pages:
        # st.write(i)
        text += i.extract_text()

    return text

resume_file=st.file_uploader(
    "upload resume (PDF) ",
    type=["pdf"]
)    

job_desc=st.text_area(
    "add job description here ",
    height=300
)

if st.button("Analyze Resume"):
    # pass 
    if not resume_file:
        st.warning("Please upload resume PDF")
        st.stop()

    if not job_desc.strip():
        st.warning("Please enter job description")
        st.stop()

    resume_text=extract_text(resume_file)    

    # st.write(resume_text)

    # SYSTEM ROLE
    system_prompt = f"""
    Your name is Resume Buddy.

    You are an expert recruiter and ATS analyzer.

    Analysis Type: {analysis_type}

    Rules:
    1. Compare resume with job description.
    2. Give clear score if possible.
    3. Mention missing skills.
    4. Suggest improvements.
    5. Use simple English.
    6. Use bullet points.
    """

    # USER ROLE
    user_prompt = f"""
    Resume Content:

    {resume_text}

    Job Description:

    {job_desc}

    Please analyze this resume.
    """

    with st.spinner("Resume Buddy is analyzing..."):

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        result = response.choices[0].message.content

    st.subheader("📌 Analysis Result")
    st.write(result)