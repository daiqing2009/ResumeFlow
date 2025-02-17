import requests
import json
from zlm.prompts.job_fit_evaluate_prompt import JOB_FIT_PROMPT
from zlm.utils.data_extraction import extract_text

# Define the endpoint and your prompt
OLLAMA_API_URL  = "http://localhost:11434/api/generate"  # Default Ollama API URL
model_name = "gemma2:9b"  # Replace with your model's name if different
pdf_file_path = "S:/ResumeFlow/zlm/demo_data/user_resume.pdf"
job_description = ""
try:
    with open("S:/ResumeFlow/zlm/demo_data/test_jd.txt", "r", encoding="utf-8") as file:  # Specify UTF-8 encoding
        file_content = file.read()
    job_description = job_description + file_content
except FileNotFoundError:
    print("File not found.")
except Exception as e:
    print(f"An error occurred: {e}")


resume = extract_text(pdf_file_path)
prompt = JOB_FIT_PROMPT.format(job_description = job_description, resume = resume)
print(prompt)
# Payload to send
payload = {
    "model": model_name,
    "prompt": prompt,
    "stream":False,
    "max_tokens": 512,
    "temperature": 0.6
}

try:
    # Send a POST request
    response = requests.post(OLLAMA_API_URL, json=payload)
    response.raise_for_status()  # Raise an error for bad HTTP responses

    # Print the response from the Llama model
    json_response_string = response.json().get("response")
    print("Response from Gemma2:{}".format(json_response_string))
    # parsed_json = json.loads(json_response_string)
    # print(json.dumps(parsed_json, indent=4))
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
