from openai import OpenAI
import streamlit as st
import pandas as pd
import os
from docx import Document
import fitz
import time

client = OpenAI(api_key=st.secrets["openai_api_key"])

SKILLSET_DIR = "inputs/skillsets"
RESUME_DIR = "inputs/resumes"
BESPOKE_RESUME_DIR = "b3spoke_resumes"
if not os.path.exists(BESPOKE_RESUME_DIR):
    os.makedirs(BESPOKE_RESUME_DIR)

TEMPLATES_DIR = "templates"
if not os.path.exists(TEMPLATES_DIR):
    os.makedirs(TEMPLATES_DIR)

logo_url = (
    "https://raw.githubusercontent.com/MadJobs/B3SPOKE/main/assets/MJ_sidebar.png"
)
st.set_page_config(page_title="MadJ(ツ)bs | B3SPOKE", layout="wide", page_icon=logo_url)

st.sidebar.image(logo_url, use_column_width=True)

skillset_content = None
resume_content = None
template_content = None


def get_csv_files(directory):
    return [f for f in os.listdir(directory) if f.endswith(".csv")]


def get_doc_files(directory):
    doc_extensions = [".pdf", ".doc", ".docx", ".txt"]
    return [
        f
        for f in os.listdir(directory)
        if any(f.endswith(ext) for ext in doc_extensions)
    ]


def load_multiple_csv(file_paths):
    df_list = [pd.read_csv(path) for path in file_paths]
    return pd.concat(df_list, ignore_index=True)


def save_uploaded_file(directory, uploaded_file):
    file_path = os.path.join(directory, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")


def read_file_content(file_path):
    """Reads and converts content of various file types to text."""
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    elif file_path.endswith(".pdf"):
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    return ""


def read_file_content(file_path):
    """Reads and converts content of various file types to text."""
    try:
        if file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        elif file_path.endswith(".docx"):
            doc = Document(file_path)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        elif file_path.endswith(".pdf"):
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        else:

            return ""
    except Exception as e:
        st.error(f"Failed to read file {file_path}: {str(e)}")
        return ""


def generate_bespoke_resume(skillset_content, resume_content, job_description):
    df = load_multiple_csv(selected_csv_paths)
    column_names = df.columns.tolist()
    filters = {}
    filtered_df = df
    for column, selected_values in filters.items():
        filtered_df = filtered_df[filtered_df[column].isin(selected_values)]
    csv = convert_df_to_csv(filtered_df)

    # prompt = f"I will now generate a new resume tailored to the job description \"{job_description}\" using the skills from the content \"{skillset_content}\" and your existing resume content \"{resume_content}\". Let's begin."
    #prompt = f"Given the job description: {job_description}, my skills: {csv}, and my resume: {resume_content}, create a new version of {resume_content} bespoke to the job description using the output format in {template_content} which tailored specifically to the job. Include a an analaysis percentage match with the my existing skills{csv} and {resume_content} to the {job_description} then a percentage improvement with the newly created resume."
    prompt = f"""You are to take on the persona of a confident, outgoing, intelligent and motivated professional looking for a career change. As you are looking for a new job you will be creating a cover letter and a new resume for each position you apply to. To achive this, you are going to read the job {job_description} and determine the industry and any nuances to that industry.  When you determine that, you will continue under the impression that is the lens in which to see your work history and skillset to find direct, or inferred corellatons with skillset: {csv} and resume content:{resume_content}. Your objective is to create a new resume bespoke to the the industry and job description. For example, when you create the new resume Objective, you will use the industy and job description to include how any of the resume and skillset experience is realevant to the position. You will do that for each section of the resume, Which needs to include these sections in order (Each section should be all caps): 
    Name
    Contact
    Objective
    QUALIFICATIONS SUMMARY
    SKILL SET SUMMARY
    EXPERIENCE (include a 3 sentence summary of the position and 5 bullet points containing 2 sentences each which show value or measurement use a KPI style.)
    EDUCATION
    Certifications
    ORGANIZATION MEMBERSHIPS
    Professional ACCOMPLISHMENTSIn   
    Publications or speaking engagements. Ensure you use markdown for your output. Include a an analaysis percentage match with the my existing skills and exisiting resume to the job description then a percentage improvement with the newly created resume."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        bespoke_resume = response.choices[0].message.content
        return bespoke_resume
    except Exception as e:
        st.error(f"Error generating bespoke resume: {str(e)}")
        return None


with st.sidebar.expander("Skillsets"):
    uploaded_csv = st.file_uploader(
        "Choose a CSV file", type=["csv"], key="csv_uploader_skillset"
    )
    if uploaded_csv is not None:
        save_uploaded_file(SKILLSET_DIR, uploaded_csv)
        st.success("File uploaded successfully!")
    csv_files = get_csv_files(SKILLSET_DIR)
    selected_csv_files = st.multiselect(
        "Select CSV files", csv_files, key="csv_selector_skillset"
    )
    selected_csv_paths = [
        os.path.join(SKILLSET_DIR, file_name) for file_name in selected_csv_files
    ]
    if selected_csv_paths:
        df = load_multiple_csv(selected_csv_paths)


with st.sidebar.expander("Resumes"):
    uploaded_resume = st.file_uploader(
        "Upload Resume", type=["pdf", "doc", "docx", "txt"], key="resume_uploader"
    )
    if uploaded_resume is not None:
        save_uploaded_file(RESUME_DIR, uploaded_resume)
        st.success("Resume uploaded successfully!")
    resume_files = get_doc_files(RESUME_DIR)
    selected_resume_files = st.multiselect(
        "Select resume files", resume_files, key="resume_files_selector"
    )
    preview_resumes = st.checkbox(
        "Preview Selected Resumes", key="preview_resumes_checkbox"
    )

with st.sidebar.expander("Templates"):
    template_files = get_doc_files(TEMPLATES_DIR)
    selected_template_file = st.selectbox(
        "Select a resume template", template_files, key="template_selector"
    )
    template_path = (
        os.path.join(TEMPLATES_DIR, selected_template_file)
        if selected_template_file
        else None
    )
    template_content = (
        read_file_content(template_path) if template_path else "No template provided."
    )


if selected_resume_files:
    print("")
else:
    st.sidebar.error("𝗣𝗟𝗘𝗔𝗦𝗘 𝗦𝗘𝗟𝗘𝗖𝗧 𝗢𝗥 𝗨𝗣𝗟𝗢𝗔𝗗 𝗔 𝗥𝗘𝗦𝗨𝗠𝗘")
if selected_csv_paths:
    print("")
else:
    st.sidebar.warning("𝗣𝗟𝗘𝗔𝗦𝗘 𝗦𝗘𝗟𝗘𝗖𝗧 𝗢𝗥 𝗨𝗣𝗟𝗢𝗔𝗗 𝗔 𝗦𝗞𝗜𝗟𝗟𝗦𝗘𝗧 𝗖𝗦𝗩")

st.info("𝖢𝖱𝖤𝖠𝖳𝖤 𝖬𝖠𝖣𝖩ツ𝖡𝖲 | 𝖡𝟥𝖲𝖯𝖮𝖪𝖤 𝖱𝖤𝖲𝖴𝖬𝖤")

col1, col2 = st.columns(2)
with col1:
    job_title = col1.text_input("Job Title", value="HaKCer").strip()
    job_url = col2.text_input("URL", value="http://madjobs.org")

job_description = st.text_area(
    "Paste job description below", height=300, key="job_desc"
)

st.markdown("----")

if st.button("Create B3SPOKE resume"):
    with st.spinner("𝙱𝙴𝙴𝙿 𝙱𝙾𝙾𝙿 𝙱𝙴𝙴𝙿 𝙷𝙰𝙲𝙺𝙸𝙽𝙶 𝙸𝙽 𝙿𝚁𝙾𝙶𝚁𝙴𝚂𝚂"):
            time.sleep(5)

    skillset_path = (
        os.path.join(SKILLSET_DIR, selected_csv_files[0])
        if selected_csv_files
        else None
    )
    resume_path = (
        os.path.join(RESUME_DIR, selected_resume_files[0])
        if selected_resume_files
        else None
    )
    skillset_content = (
        read_file_content(skillset_path) if skillset_path else "No skillset provided."
    )
    resume_content = (
        read_file_content(resume_path) if resume_path else "No resume provided."
    )

    bespoke_resume_text = generate_bespoke_resume(
        skillset_content, resume_content, job_description
    )

    for csv_file in selected_csv_files:
        skillset_path = os.path.join(SKILLSET_DIR, csv_file)
    for resume_file in selected_resume_files:
        resume_path = os.path.join(RESUME_DIR, resume_file)
    bespoke_resume_text = generate_bespoke_resume(
        skillset_content, resume_content, job_description
    )
    if bespoke_resume_text:
        html_path = os.path.join(BESPOKE_RESUME_DIR, f"{job_title}.html")
        txt_path = os.path.join(BESPOKE_RESUME_DIR, f"{job_title}.txt")
        with open(html_path, "w") as html_file, open(txt_path, "w") as txt_file:
            html_file.write(bespoke_resume_text)
            txt_file.write(bespoke_resume_text)
        
            st.success("Bespoke resume created successfully.")

st.sidebar.markdown("----")
st.sidebar.success("𝗕𝟯𝗦𝗣𝗢𝗞𝗘 𝗥𝗘𝗦𝗨𝗠𝗘𝗦")
with st.sidebar.expander("B3SPOKE Resumes"):

    if st.checkbox("Preview B3SPOKE Resume"):
        generated_files = os.listdir(BESPOKE_RESUME_DIR)
        
        selected_bespoke_file = st.selectbox('Select a B3SPOKE resume', generated_files, key="bespoked_file_selector", index=0)

        
try:
    generated_files = os.listdir(BESPOKE_RESUME_DIR)
    bespoke_file_path = os.path.join(BESPOKE_RESUME_DIR, selected_bespoke_file)
    with open(bespoke_file_path, "r", encoding="utf-8") as file:

        bespoke_content = file.read()
        st.markdown(bespoke_content, unsafe_allow_html=True)
        st.download_button(
            label=f"Download {selected_bespoke_file}",
            data=bespoke_content,
            file_name=selected_bespoke_file,
        )
    if st.button(f"Delete {selected_bespoke_file}"):
        os.remove(bespoke_file_path)
        st.success(f"{selected_bespoke_file} deleted successfully")
        st.rerun()  
except Exception as e:
    pass

created_resumes_count = len(os.listdir(BESPOKE_RESUME_DIR))

st.sidebar.metric(label="Created Resumes", value=created_resumes_count)

if preview_resumes:
    with st.expander("Resumes Preview"):
        for file_name in selected_resume_files:
            st.text(file_name)
            with open(os.path.join(RESUME_DIR, file_name), "rb") as file:
                st.download_button(
                    label=f"Download {file_name}",
                    data=file,
                    file_name=file_name,
                    key=f"download_{file_name}",
                )

st.sidebar.warning("Development")
with st.sidebar.expander("Development", expanded=False):
    if selected_csv_paths:
        df = load_multiple_csv(selected_csv_paths)

        st.write("### Filters")
        column_names = df.columns.tolist()
        filters = {}
        for column in column_names:
            unique_values = df[column].dropna().unique()
            selected_values = st.multiselect(
                f"Filter by {column}", options=unique_values, key=f"filter_{column}"
            )
            if selected_values:
                filters[column] = selected_values
        filtered_df = df
        for column, selected_values in filters.items():
            filtered_df = filtered_df[filtered_df[column].isin(selected_values)]
        st.write("### Filtered DataFrame")
        st.dataframe(filtered_df)
        csv = convert_df_to_csv(filtered_df)
        st.download_button(
            label="Download filtered data as CSV",
            data=csv,
            file_name="filtered_data.csv",
            mime="text/csv",
        )

    if st.checkbox("Show structured data"):
        unique_categories = df["Category"].unique()
        for category in unique_categories:
            st.subheader(category)
            category_data = df[df["Category"] == category]
            for _, row in category_data.iterrows():
                st.text(f"Item: {row['Item']}")
                if pd.notna(row["Ability Level"]):
                    st.text(f"Ability Level: {row['Ability Level']}")
                if pd.notna(row["Reference"]):
                    st.markdown(f"Reference: [{row['Reference']}]({row['Reference']})")
                if pd.notna(row["Notes"]):
                    st.text(f"Notes: {row['Notes']}")

    created_resumes_count = len(os.listdir(BESPOKE_RESUME_DIR))
    st.metric(label="Created Resumes", value=created_resumes_count)
