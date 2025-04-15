# ResumeFlow: An LLM-facilitated Pipeline for Personalized Resume Generation and Refinement 
[![License: MIT](https://img.shields.io/badge/License-MIT-success.svg?logo)](https://github.com/daiqing2009/ResumeFlow/blob/main/LICENSE)

## Framework
<img width="950" alt="image" src="https://github.com/daiqing2009/ResumeFlow/blob/main/resources/exp-job-recomm-arch.png" />

This repository was forked from https://github.com/Ztrimus/ResumeFlow 

# Setup, Installation and Usage
## Prerequisites
 - OS : Linux, Mac
 - Python : 3.11.6 and above
 - Ollama with local LLMs downloaded, we recommend using our fine-tuned model.
 - LLM API key(Optional): [OpenAI](https://platform.openai.com/account/api-keys) OR [Gemini Pro](https://ai.google.dev/)


## Setup & Run Code - Use as Project

```sh
git clone https://github.com/Ztrimus/job-llm.git
cd job-llm
```
 1. Create and activate python environment (use `python -m venv .env` or conda or etc.) to avoid any package dependency conflict.
 2. Install [Poetry package](https://python-poetry.org/docs/basic-usage/) (dependency management and packaging tool)
    ```bash
    pip install poetry
    ```
 3. Install all required packages.
     - Refer [pyproject.toml](pyproject.toml) or [poetry.lock](poetry.lock) for list of packages.
        ```bash
        poetry install
        ```
        OR
     - If above command not working, we also provided [requirements.txt](resources/requirements.txt) file. But, we recommend using poetry.
        ```bash
        pip install -r resources/requirements.txt
        ```
4. We also need to install following packages to conversion of latex to pdf
    - For linux
        ```bash
        sudo apt-get install texlive-latex-base texlive-fonts-recommended texlive-fonts-extra
        ```
        NOTE: try `sudo apt-get update` if terminal unable to locate package.
    - For Mac
        ```bash
        brew install basictex
        sudo tlmgr install enumitem fontawesome
        ```
5. If you want to run ollama models
    ```sh
    ollama pull llama3.1
    ```
6. Run following script to get result
```bash
>>> python main.py /
    --url "JOB_POSTING_URL" /
    --master_data="JSON_USER_MASTER_DATA" /
    --api_key="YOUR_LLM_PROVIDER_API_KEY" / # put api_key considering provider
    --downloads_dir="DOWNLOAD_LOCATION_FOR_RESUME_CV" /
    --provider="openai" # openai, gemini
```

## References
 - [Prompt engineering Guidelines](https://platform.openai.com/docs/guides/prompt-engineering)
 - [Overleaf LaTex Resume Template](https://www.overleaf.com/latex/templates/jakes-resume-anonymous/cstpnrbkhndn)
 - [Combining LaTeX with Python](https://tug.org/tug2019/slides/slides-ziegenhagen-python.pdf)
 - [OpenAI Documentation](https://platform.openai.com/docs/api-reference/chat/create)
