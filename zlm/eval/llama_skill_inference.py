import requests
import json
from zlm import AutoApplyModel
from zlm.prompts.sections_prompt import SKILLS

# Define the endpoint and model
OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Default Ollama API URL
model_name = "hf.co/WildBurger/group1_finetuned_gemma2_v3:Q8_0"  # Replace with your model's name if different

ds_file_path = "eval_json_skill_ds.json"
ds_file_path2 = "eval_json_skill_ds2.json"
json_data, inf_res = [], []
try:
    with open(ds_file_path, "r", encoding="utf-8") as j_file:  # Specify UTF-8 encoding
        data1 = json.load(j_file)
        json_data += data1
except FileNotFoundError:
    print("File not found.")
except Exception as e:
    print(f"An error occurred: {e}")

try:
    with open(ds_file_path2, "r", encoding="utf-8") as j_file2:  # Specify UTF-8 encoding
        data2 = json.load(j_file2)
        json_data += data2
except FileNotFoundError:
    print("File not found.")
except Exception as e:
    print(f"An error occurred: {e}")

print("Data Size:{}".format(len(json_data)))
inference_llm = AutoApplyModel(api_key="", provider="Ollama", model=model_name,
                               downloads_dir="C:/Users/Wilfried/Downloads/") # replace with your local dir

for item in json_data:
    if item.get("input").get("resume").get("skill_section") is None or len(
            item.get("input").get("resume").get("skill_section")) < 1:
        continue

    prompt = SKILLS.format(section_data=json.dumps(item.get("input").get("resume")),
                               job_description=json.dumps(item.get("input").get("job_description")))
    response = inference_llm.llm.get_response(prompt=prompt, expecting_longer_output=True, need_json_output=True)
    try:
        if response is not None and isinstance(response, dict):
            if response.get("resume") is not None:
                if isinstance(response.get("resume"), str):
                    string_text = response.get("resume").strip()
                    if not string_text or string_text is None:
                        continue
                    # j_tmp = json.loads(string_text)
                    json_response = {"resume": string_text}
                elif isinstance(response.get("resume"), dict):
                    json_response = {"skill_section": response.get("resume").get("skill_section")}
                else:
                    json_response = {"resume": response.get("resume")}
            else:
                json_response = {"skill_section": response.get("skill_section")}
        elif isinstance(response, dict):
            json_response = response
        print(json.dumps(json_response, indent=4))
        inf_res.append({
            "benchmark_output": item.get("output"),
            "inference_output": json_response
        })
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

inference_output_ds = "finetuned_gemma2_skill_ds.json"
try:
    with open(inference_output_ds, "w+", encoding='utf-8') as output_file:
        json.dump(inf_res, output_file, indent=4)
except Exception as e:
    print(f"An error occurred when writing the output file: {e}")