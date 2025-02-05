from Tools.demo.sortvisu import steps
from langchain.prompts import PromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_core.runnables import RunnableSequence

# Initialize the Ollama model
llm = Ollama(model="gemma2:9b")

# Create a prompt template
template = "Translate the following text to French: {text}"
prompt = PromptTemplate(input_variables=["text"], template=template)

# Create a chain
pipeline = prompt | llm

# Run the chain
response = pipeline.invoke({"text": "Hello, how are you?"})
print(response)
response = llm.invoke("Hello, how are you?")
print(response)