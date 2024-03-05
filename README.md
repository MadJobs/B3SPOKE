
![MJ_ASNI](https://github.com/MadJobs/B3SPOKE/assets/3261849/fad5d78e-9a79-46dc-a8e8-b248934c57c5)
```
 ██▄ ▀██ ▄▀▀ █▀▄ ▄▀▄ █▄▀ ██▀
 █▄█ ▄▄█ ▄██ █▀  ▀▄▀ █ █ █▄▄
```

![AI](https://img.shields.io/badge/AI-Enabled-brightgreen)
![Generative AI](https://img.shields.io/badge/Generative%20AI-Enabled-blueviolet)
![OpenLLM](https://img.shields.io/badge/OpenLLM-Integrated-blue)

B3SPOKE generates bespoke resumes tailored to specific job descriptions using natural language processing (NLP) techniques. It utilizes the OpenAI GPT-3.5 model to generate personalized resumes based on uploaded skillsets, resumes, and job descriptions.

## Features

- Upload skillset data in CSV format.
- Upload existing resumes in various formats (PDF, DOC, DOCX, TXT).
- Generate bespoke resumes customized for specific job descriptions.
- Preview and download generated resumes.
- Filter skillset data for more precise resume generation.
- Real-time updates and notifications.
- Easy-to-use interface with a streamlined workflow.

## Installation

To run the application locally, follow these steps:

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Create a virtual environment using `virtualenv`:

### Clone this repository
```bash
git clone https://github.com/MadJobs/B3SPOKE.git
cd B3SPOKE
```

```bash
virtualenv venv
Activate the virtual environment:
```
### For Windows:
```bash
venv\Scripts\activate
```
### For macOS/Linux:
```bash
source venv/bin/activate
```
### Install the required dependencies:
```bash
pip3 install -r requirements.txt
```

### Set up the necessary API keys and secrets.
```bash
mv .streamlit/sample_secrets.toml .streamlit/secrets.toml
```
### Run the application:
```bash
streamlit run b3spoke.py
```
### Access the application in your web browser at http://localhost:8501.
