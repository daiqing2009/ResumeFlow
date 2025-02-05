import requests

# Define the endpoint and your prompt
OLLAMA_API_URL  = "http://localhost:11434/api/generate"  # Default Ollama API URL
model_name = "llama3.1:8b"  # Replace with your model's name if different
prompt = "Can you show me a resume template for a Java developer?"

# Payload to send
payload = {
    "model": model_name,
    "prompt": prompt,
    "stream":False,
    "max_tokens": 512,
    "temperature": 0.9
}

try:
    # Send a POST request
    response = requests.post(OLLAMA_API_URL, json=payload)
    response.raise_for_status()  # Raise an error for bad HTTP responses

    # Print the response from the Llama model
    print("Response from Llama:{}".format(response.json()["response"]))

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
