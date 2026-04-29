import os
from dotenv import load_dotenv
import streamlit as st
from openai import AzureOpenAI

load_dotenv()

api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

if not api_key:
    st.error("Missing OPENAI_API_KEY in .env file")
    st.stop()

client = AzureOpenAI(api_key=api_key, azure_endpoint=endpoint, api_version=api_version, azure_deployment=deployment)

st.set_page_config(page_title="IT Help Desk AI Assistant", page_icon="💻")

st.title("💻 IT Help Desk AI Assistant")
st.write("Describe an IT issue and get practical troubleshooting guidance.")
st.caption("This tool provides troubleshooting suggestions and does not replace official IT support procedures.")

category = st.selectbox(
    "Choose issue category:",
    ["VPN", "Email", "Password/Login", "Printer", "Network", "Software", "Other"]
)

sample_issues = {
    "VPN Issue": "My VPN connects, but I cannot access company resources.",
    "Outlook Issue": "Outlook opens but does not send or receive emails.",
    "Password Issue": "My account is locked and password reset is not working.",
    "Printer Issue": "I can see the printer but my documents stay in queue."
}

sample_choice = st.selectbox("Try a sample issue:", ["None"] + list(sample_issues.keys()))

default_text = sample_issues[sample_choice] if sample_choice != "None" else ""

issue = st.text_area(
    "Enter the problem:",
    value=default_text,
    placeholder="Example: My VPN is connected but I cannot access internal company websites.",
    height=150
)

if st.button("Get Help"):
    if not issue.strip():
        st.warning("Please enter an issue first.")
    else:
        with st.spinner("Analyzing the issue..."):
            prompt = f"""
You are a senior IT Help Desk analyst supporting end users in a corporate environment.

Issue category: {category}
User issue: "{issue}"

Rules:
- Be concise but useful
- Focus on realistic help desk troubleshooting
- Include triage logic where appropriate
- Mention when escalation or admin action is needed
- Avoid unnecessary jargon

Respond with these sections:

Issue Summary:
Possible Causes:
Troubleshooting Steps:
Escalation Guidance:
Severity Level:
"""
            try:
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful IT support assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3
                )

                answer = response.choices[0].message.content

                st.subheader("Suggested Troubleshooting")
                st.write(answer)
                st.info("Check whether the issue affects one user or multiple users before escalating.")

            except Exception as e:
                st.error(f"Error: {e}")