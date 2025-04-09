import json

from zlm.utils.metrics import compute_rouge, cosine_similarity

# ds_file_path = "C:/Users/Wilfried/Downloads/inference_gemma2_skill_ds2.json"
ds_file_path = "C:/Users/Wilfried/Downloads/base_gemma2_exp_ds2.json"
output_data = []

try:
    with open(ds_file_path, "r", encoding="utf-8") as j_file2:  # Specify UTF-8 encoding
        data = json.load(j_file2)
except FileNotFoundError:
    print("File not found.")
except Exception as e:
    print(f"An error occurred: {e}")

output_data = data
total = len(output_data)
print(f"Data Size: {total}")
num_outlier = 0

references = []
predictions = []

valid_num_output = 0
cos_sim_scores = []
for sec in output_data[0].get("benchmark_output"):
    print(f"Section: {sec}")

for output in output_data:
    bench_output, inference_output = None, None
    for sec in output.get("benchmark_output"):
        bench_output = output.get("benchmark_output").get(sec)
        if bench_output is None or (isinstance(bench_output, list) and len(bench_output) < 1):
            continue

    for sec in output.get("inference_output"):
        inference_output = output.get("inference_output").get(sec)
        if inference_output is None or (isinstance(inference_output, list) and len(inference_output) < 1):
            num_outlier += 1
            continue
        else:
            reference = json.dumps({sec:bench_output})
            prediction = json.dumps({sec:inference_output})
            valid_num_output += 1
            cos_sim_score = cosine_similarity(reference, prediction)
            cos_sim_scores.append(cos_sim_score)
            references.append(reference)
            predictions.append(prediction)

outlier_rate = num_outlier / total
print(f"Outlier Rate: {outlier_rate:.2f}")
# rouge_score = compute_rouge(predictions, references)
# for r_s in rouge_score:
#     print(f"{r_s}: {rouge_score[r_s]:.3f}")
avg_cos_sim_score = sum(cos_sim_scores) / valid_num_output
print(f"Average COS similarity score: {avg_cos_sim_score:.3f}")