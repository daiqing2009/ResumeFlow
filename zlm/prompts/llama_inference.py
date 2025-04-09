import requests
import json

from zlm import AutoApplyModel
from zlm.prompts.convert_prompt import JD_CONVERT
from zlm.prompts.job_fit_evaluate_prompt import JOB_FIT_PROMPT
from zlm.prompts.sections_prompt import SKILLS, EXPERIENCE, PROJECTS
from zlm.utils.data_extraction import extract_text

# Define the endpoint and your prompt
OLLAMA_API_URL  = "http://localhost:11434/api/generate"  # Default Ollama API URL
# model_name = "hf.co/WildBurger/group1_finetuned_gemma2_v3:Q8_0"  # Replace with your model's name if different
model_name = "gemma2:9b"
# pdf_file_path = "S:/ResumeFlow/zlm/demo_data/user_resume.pdf"
# job_description = ""
# try:
#     with open("S:/ResumeFlow/zlm/demo_data/test_jd3.txt", "r", encoding="utf-8") as file:  # Specify UTF-8 encoding
#         file_content = file.read()
#     job_description = job_description + file_content
# except FileNotFoundError:
#     print("File not found.")
# except Exception as e:
#     print(f"An error occurred: {e}")

# resume = extract_text(pdf_file_path)
# prompt = JD_CONVERT+"\nJob Description Data: "+job_description
# prompt = JOB_FIT_PROMPT.format(job_description = job_description, resume = resume)

ds_file_path = "C:/Users/Wilfried/Downloads/eval_json_exp_ds3.json"
json_data, inf_res = [],[]
try:
    with open(ds_file_path, "r", encoding="utf-8") as j_file:  # Specify UTF-8 encoding
        json_data = json.load(j_file)
    print("Data Size:{}".format(len(json_data)))
except FileNotFoundError:
    print("File not found.")
except Exception as e:
    print(f"An error occurred: {e}")

inference_llm = AutoApplyModel(api_key="", provider="Ollama", model = model_name, downloads_dir="C:/Users/Wilfried/Downloads/")

count = 0
for item in json_data:
    count+=1
    if count <1:
        continue
    if len(inf_res)>41:
        break
    if item.get("input").get("resume").get("work_experience") is None or len(item.get("input").get("resume").get("work_experience")) < 1:
        continue

    prompt = EXPERIENCE.format(section_data=json.dumps(item.get("input").get("resume")), job_description=json.dumps(item.get("input").get("job_description")))
    response = inference_llm.llm.get_response(prompt=prompt, expecting_longer_output=True, need_json_output=True)
    # Payload to send
    # payload = {
    #     "model": model_name,
    #     "prompt": prompt,
    #     "stream":False,
    #     "max_tokens": 4096,
    #     "temperature": 0.8
    # }

    try:
        # Send a POST request
        # response = requests.post(OLLAMA_API_URL, json=payload)
        # response.raise_for_status()  # Raise an error for bad HTTP responses

        # Print the response from the Llama model
        if response is not None and isinstance(response, dict):
            if response.get("resume") is not None:
                if isinstance(response.get("resume"), str):
                    string_text = response.get("resume").strip()
                    if not string_text or string_text is None:
                        continue
                    # j_tmp = json.loads(string_text)
                    json_response = {"resume": string_text}
                elif isinstance(response.get("resume"), dict):
                    json_response = {"work_experience" : response.get("resume").get("work_experience")}
                else:
                    json_response = {"resume" : response.get("resume")}
            else:
                json_response = {"work_experience": response.get("work_experience")}
        elif isinstance(response, dict):
            json_response = response
        print(json.dumps(json_response, indent=4))
        inf_res.append({
            "benchmark_output":item.get("output"),
            "inference_output": json_response
        })
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


inference_output_ds = "C:/Users/Wilfried/Downloads/base_gemma2_exp_ds2.json"
try:
    with open(inference_output_ds, "w+", encoding='utf-8') as output_file:
        json.dump(inf_res, output_file, indent=4)
except Exception as e:
    print(f"An error occurred when writing the output file: {e}")