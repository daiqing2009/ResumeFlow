'''
-----------------------------------------------------------------------
File: __init__.py
Creation Time: Feb 8th 2024, 2:59 pm
Author: Saurabh Zinjad
Developer Email: saurabhzinjad@gmail.com
Copyright (c) 2023-2024 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
-----------------------------------------------------------------------
'''
import os
import json
import re
import validators
import numpy as np
import streamlit as st

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from zlm.prompts.convert_prompt import RESUME_CONVERT, JD_CONVERT
from zlm.prompts.job_fit_evaluate_prompt import JOB_FIT_PROMPT
from zlm.schemas.sections_schemas import ResumeSchema
from zlm.utils import utils
from zlm.utils.latex_ops import latex_to_pdf
from zlm.utils.llm_models import ChatGPT, Gemini, OllamaModel
from zlm.utils.data_extraction import read_data_from_url, extract_text
from zlm.utils.metrics import jaccard_similarity, overlap_coefficient, cosine_similarity, vector_embedding_similarity
from zlm.prompts.resume_prompt import CV_GENERATOR, RESUME_WRITER_PERSONA, JOB_DETAILS_EXTRACTOR, RESUME_DETAILS_EXTRACTOR
from zlm.schemas.job_details_schema import JobDetails
from zlm.variables import DEFAULT_LLM_MODEL, DEFAULT_LLM_PROVIDER, LLM_MAPPING, section_mapping

module_dir = os.path.dirname(__file__)
demo_data_path = os.path.join(module_dir, "demo_data", "user_profile.json")
prompt_path = os.path.join(module_dir, "prompts")


class AutoApplyModel:
    """
    A class that represents an Auto Apply Model for job applications.

    Args:
        api_key (str): The OpenAI API key.
        downloads_dir (str, optional): The directory to save downloaded files. Defaults to the default download folder.
        provider (str, optional): The LLM provider to use. Defaults to "Gemini".
        model (str, optional): The LLM model to use. Defaults to "gemini-1.5-flash-latest".

    Methods:
        get_prompt(system_prompt_path: str) -> str: Returns the system prompt from the specified path.
        resume_to_json(pdf_path: str) -> dict: Extracts resume details from the specified PDF path.
        user_data_extraction(user_data_path: str) -> dict: Extracts user data from the specified path.
        job_details_extraction(url: str) -> dict: Extracts job details from the specified job URL.
        resume_builder(job_details: dict, user_data: dict) -> dict: Generates a resume based on job details and user data.
        cover_letter_generator(job_details: dict, user_data: dict) -> str: Generates a cover letter based on job details and user data.
        resume_cv_pipeline(job_url: str, user_data_path: str) -> None: Runs the Auto Apply Pipeline.
    """

    def __init__(
        self, api_key: str = None, provider: str = None, model: str = None, downloads_dir: str = utils.get_default_download_folder(), system_prompt: str = RESUME_WRITER_PERSONA
    ):
        self.system_prompt = system_prompt
        self.provider = DEFAULT_LLM_PROVIDER if provider is None or provider.strip() == "" else provider
        self.model = DEFAULT_LLM_MODEL if model is None or model.strip() == "" else model
        self.downloads_dir = utils.get_default_download_folder() if downloads_dir is None or downloads_dir.strip() == "" else downloads_dir

        if api_key is None or api_key.strip() == "os":
                api_env = LLM_MAPPING[self.provider]["api_env"]
                if api_env != None and api_env.strip() != "":
                    self.api_key = os.environ.get(LLM_MAPPING[self.provider]["api_env"]) 
                else:
                    self.api_key = None
        else:
            self.api_key = api_key

        self.llm = self.get_llm_instance()
    
    def get_llm_instance(self):
        if self.provider == "GPT":
            return ChatGPT(api_key=self.api_key, model=self.model, system_prompt=self.system_prompt)
        elif self.provider == "Gemini":
            return Gemini(api_key=self.api_key, model=self.model, system_prompt=self.system_prompt)
        elif self.provider == "Ollama":
            return OllamaModel(model=self.model, system_prompt=self.system_prompt)
        else:
            raise Exception("Invalid LLM Provider")


    def resume_plain_text(self, pdf_path):
        """
        Converts a resume in PDF format to JSON format.

        Args:
            pdf_path (str): The path to the PDF file.

        Returns:
            dict: The resume data in plain text.
        """
        resume_text = extract_text(pdf_path)
        # print("resume_json Text:{}".format(resume_text))
        return resume_text

    def resume_to_json(self, pdf_path):
        """
        Converts a resume in PDF format to JSON format.

        Args:
            pdf_path (str): The path to the PDF file.

        Returns:
            dict: The resume data in JSON format.
        """
        resume_text = extract_text(pdf_path)
        json_parser = JsonOutputParser(pydantic_object=ResumeSchema)

        prompt = PromptTemplate(
            template=RESUME_DETAILS_EXTRACTOR,
            input_variables=["resume_text"],
            partial_variables={"format_instructions": json_parser.get_format_instructions()}
            ).format(resume_text=resume_text)
        print("PDF prompt:{}".format(prompt))
        resume_json = self.llm.get_response(prompt=prompt, need_json_output=True)
        # print("resume_json Text:{}".format(resume_json))
        return resume_json

    @utils.measure_execution_time
    def user_data_extraction(self, user_data_path: str = demo_data_path, is_st=False):
        """
        Extracts user data from the given file path.

        Args:
            user_data_path (str): The path to the user data file.

        Returns:
            dict: The extracted user data in JSON format.
        """
        print("\nFetching user data...")

        if user_data_path is None or (type(user_data_path) is str and user_data_path.strip() == ""):
            user_data_path = demo_data_path

        extension = os.path.splitext(user_data_path)[1]

        if extension == ".pdf":
            user_data = self.resume_plain_text(user_data_path)
            # user_data = self.resume_to_json(user_data_path)
            # print("User data:{}".format(user_data))
        elif extension == ".json":
            user_data = utils.read_json(user_data_path)
        elif validators.url(user_data_path):
            user_data = read_data_from_url([user_data_path])
            pass
        else:
            raise Exception("Invalid file format. Please provide a PDF, JSON file or url.")
        
        return user_data

    @utils.measure_execution_time
    def job_fit_score_evaluation_extraction(self, eval_prompt: str = ""):
        """
        Extract job fit score.

        Args:
            eval_prompt (str): The prompt of job fit score evaluation.

        Returns:
            dict: A dictionary containing the extracted job details.
        """

        print("\nExtracting job fit score...")
        try:
            if eval_prompt is not None and eval_prompt.strip() != "":
                job_fit_score_details = self.llm.get_response(prompt=eval_prompt, need_json_output=True)
                return job_fit_score_details
            else:
                raise Exception("Prompt empty. Unable to evaluate using job fit score")

        except Exception as e:
            print(e)
            st.write("Please provide a valid prompt for job fit score.")
            st.error(f"Error in job fit score evaluation, {e}")
            return None


    @utils.measure_execution_time
    def job_details_extraction(self, url: str=None, job_site_content: str=None, is_st=False):
        """
        Extracts job details from the specified job URL.

        Args:
            url (str): The URL of the job posting.
            job_site_content (str): The content of the job posting.

        Returns:
            dict: A dictionary containing the extracted job details.
        """
        
        print("\nExtracting job details...")

        try:
            # TODO: Handle case where it returns None. sometime, website take time to load, but scraper complete before that.
            if url is not None and url.strip() != "":
                job_site_content = read_data_from_url(url)
            if job_site_content is not None and job_site_content.strip() != "":
                # json_parser = JsonOutputParser(pydantic_object=JobDetails)
                
                # prompt = PromptTemplate(
                #     template=JOB_DETAILS_EXTRACTOR,
                #     input_variables=["job_description"],
                #     partial_variables={"format_instructions": json_parser.get_format_instructions()}
                #     ).format(job_description=job_site_content)

                job_details = self.llm.get_response(prompt=JD_CONVERT+"\n Job Description Data: {}".format(job_site_content), expecting_longer_output=True, need_json_output=True)

                if url is not None and url.strip() != "":
                    job_details["url"] = url
                jd_path = utils.job_doc_name(job_details, self.downloads_dir, "jd")

                utils.write_json(jd_path, job_details)
                print(f"Job Details JSON generated at: {jd_path}")

                if url is not None and url.strip() != "":
                    del job_details['url']
                
                return job_details, jd_path
            else:
                raise Exception("Unable to web scrape the job description.")

        except Exception as e:
            print(e)
            st.write("Please try pasting the job description text instead of the URL.")
            st.error(f"Error in Job Details Parsing, {e}")
            return None, None
 
    @utils.measure_execution_time
    def cover_letter_generator(self, job_details: dict, user_data: dict, need_pdf: bool = True, is_st=False):
        """
        Generates a cover letter based on the provided job details and user data.

        Args:
            job_details (dict): A dictionary containing the job description.
            user_data (dict): A dictionary containing the user's resume or work information.

        Returns:
            str: The generated cover letter.

        Raises:
            None
        """
        print("\nGenerating Cover Letter...")

        try:
            prompt = PromptTemplate(
                template=CV_GENERATOR,
                input_variables=["my_work_information", "job_description"],
                ).format(job_description=job_details, my_work_information=user_data)

            cover_letter = self.llm.get_response(prompt=prompt, expecting_longer_output=True)

            cv_path = utils.job_doc_name(job_details, self.downloads_dir, "cv")
            utils.write_file(cv_path, cover_letter)
            print("Cover Letter generated at: ", cv_path)
            if need_pdf:
                utils.text_to_pdf(cover_letter, cv_path.replace(".txt", ".pdf"))
                print("Cover Letter PDF generated at: ", cv_path.replace(".txt", ".pdf"))
            
            return cover_letter, cv_path.replace(".txt", ".pdf")
        except Exception as e:
            print(e)
            st.write("Error: \n\n",e)
            return None, None

    @utils.measure_execution_time
    def resume_builder(self, job_details: dict, user_data: dict, is_st=False, bckup_llm=None):
        """
        Builds a resume based on the provided job details and user data.

        Args:
            job_details (dict): A dictionary containing the job description.
            user_data (dict): A dictionary containing the user's resume or work information.

        Returns:
            dict: The generated resume details.

        Raises:
            FileNotFoundError: If the system prompt files are not found.
        """
        try:
            print("\nGenerating Resume Details...")
            if is_st: st.toast("Generating Resume Details...")

            resume_details = dict()
            # Personal Information Section
            if is_st: st.toast("Processing Resume's Personal Info Section...")
            if bckup_llm is not None:
                json_formatted_resume = bckup_llm.llm.get_response(
                    prompt=RESUME_CONVERT + "\n Resume Data: {}".format(user_data), expecting_longer_output=True, need_json_output=True)
            else:
                json_formatted_resume = self.llm.get_response(
                prompt=RESUME_CONVERT+"\n Resume Data: {}".format(user_data), expecting_longer_output=True, need_json_output=True)

            print("Response User Data Text: {}".format(json.dumps(json_formatted_resume)))
            if json_formatted_resume is not None and isinstance(json_formatted_resume, dict):
                resume_details["personal"] = {
                    "name": json_formatted_resume.get("name") if json_formatted_resume.get("name") is not None else "",
                    "phone": json_formatted_resume.get("phone") if json_formatted_resume.get("phone") is not None else "",
                    "email": json_formatted_resume.get("email") if json_formatted_resume.get("email") is not None else "",
                    "github": json_formatted_resume.get("github") or "",
                    "linkedin": json_formatted_resume.get("linkedin") or ""
                }
                st.markdown("**Personal Info Section**")
                # resume_details["education"] = json_formatted_resume.get("education") if json_formatted_resume.get("education") is not None else []
                # st.markdown("**Education Info Section**")
                # resume_details["certifications"] = json_formatted_resume.get("certifications") if json_formatted_resume.get("certifications") is not None else []
                # st.markdown("**Certification Info Section**")
                # resume_details["achievements"] = json_formatted_resume.get("achievements") if json_formatted_resume.get("achievements") is not None else []
                # st.markdown("**Achievement Info Section**")
                st.write(resume_details)
            # Other Sections
            for section in ['education', 'summary', 'skill_section', 'work_experience', 'projects', 'certifications','achievements']:
                section_log = f"Processing Resume's {section.upper()} Section..."
                if is_st: st.toast(section_log)
                # if json_formatted_resume[section] == []:
                #     resume_details[section] = []
                #     continue
                print("Processing section: "+section)
                json_parser = JsonOutputParser(pydantic_object=section_mapping[section]["schema"])
                prompt = PromptTemplate(
                    input_variables=[str(section)],
                    template=section_mapping[section]["prompt"],
                    partial_variables={"format_instructions": json_parser.get_format_instructions()}
                ).format(section_data=json.dumps(json_formatted_resume), job_description=json.dumps(job_details))
                # if section == "projects" or section == "work_experience":
                #     response = self.llm.get_response(prompt=prompt, expecting_longer_output=True, need_json_output=True)
                # else:
                if section not in ["skill_section", "work_experience"] and bckup_llm is not None:
                    response = bckup_llm.llm.get_response(prompt=prompt, expecting_longer_output=True, need_json_output=True)
                else:
                    response = self.llm.get_response(prompt=prompt, expecting_longer_output=True, need_json_output=True)

                # Check for empty sections
                if response is not None and isinstance(response, dict):
                    if section in response:
                        if response[section]:
                            if section == "skill_section":
                                resume_details[section] = [i for i in response['skill_section']]
                            else:
                                resume_details[section] = response[section]

                if is_st:
                    st.markdown(f"**{section.upper()} Section**")
                    st.write(response)

            resume_path = utils.job_doc_name(job_details, self.downloads_dir, "resume")
            utils.write_json(resume_path, resume_details)
            resume_path = resume_path.replace(".json", ".pdf")
            st.write(f"resume_path: {resume_path}")

            resume_latex = latex_to_pdf(resume_details, resume_path)
            # st.write(f"resume_pdf_path: {resume_pdf_path}")

            return resume_path, resume_details, json_formatted_resume
        except Exception as e:
            print(e)
            st.write("Error: \n\n", e)
            return resume_path, resume_details, json_formatted_resume


    @utils.measure_execution_time
    def resume_builder_bk(self, job_details: dict, user_data: dict, is_st=False):
        """
        Builds a resume based on the provided job details and user data.

        Args:
            job_details (dict): A dictionary containing the job description.
            user_data (dict): A dictionary containing the user's resume or work information.

        Returns:
            dict: The generated resume details.

        Raises:
            FileNotFoundError: If the system prompt files are not found.
        """
        try:
            print("\nGenerating Resume Details...")
            if is_st: st.toast("Generating Resume Details...")

            resume_details = dict()
            print("User Data Text: {}".format(user_data))
            # Personal Information Section
            if is_st: st.toast("Processing Resume's Personal Info Section...")
            resume_details["personal"] = { 
                "name":  user_data.get("name") if  user_data.get("name") is not None else "",
                "phone": user_data.get("phone") if  user_data.get("phone") is not None else "",
                "email": user_data.get("email") if user_data.get("email") is not None else "",
                "github": user_data.get("media", {}).get("github") or "",
                "linkedin": user_data.get("media", {}).get("linkedin") or ""
                }
            st.markdown("**Personal Info Section**")
            st.write(resume_details)

            # Other Sections
            for section in ['summary', 'work_experience', 'projects', 'skill_section', 'education', 'certifications', 'achievements']:
                section_log = f"Processing Resume's {section.upper()} Section..."
                if is_st: st.toast(section_log)
                if user_data.get(section) is None:
                    continue
                json_parser = JsonOutputParser(pydantic_object=section_mapping[section]["schema"])
                prompt = PromptTemplate(
                    input_variables=[str(section)],
                    template=section_mapping[section]["prompt"],
                    partial_variables={"format_instructions": json_parser.get_format_instructions()}
                    ).format(section_data = json.dumps(user_data.get(section)), job_description = json.dumps(job_details))

                if section == "projects" or section == "work_experience":
                    response = self.llm.get_response(prompt=prompt, expecting_longer_output=True, need_json_output=True)
                else:
                    response = self.llm.get_response(prompt=prompt, need_json_output=True)
                # Check for empty sections
                if response is not None and isinstance(response, dict):
                    if section in response:
                        if response[section]:
                            if section == "skill_section":
                                resume_details[section] = [i for i in response['skill_section'] if len(i['skills'])]
                            else:
                                resume_details[section] = response[section]
                
                if is_st:
                    st.markdown(f"**{section.upper()} Section**")
                    st.write(response)

            if job_details.get("keyskills") is not None:
                resume_details['keyskills'] = ', '.join(job_details['keyskills'])
            
            resume_path = utils.job_doc_name(job_details, self.downloads_dir, "resume")
            utils.write_json(resume_path, resume_details)
            resume_path = resume_path.replace(".json", ".pdf")
            st.write(f"resume_path: {resume_path}")

            resume_latex = latex_to_pdf(resume_details, resume_path)
            # st.write(f"resume_pdf_path: {resume_pdf_path}")

            return resume_path, resume_details
        except Exception as e:
            print(e)
            st.write("Error: \n\n",e)
            return resume_path, resume_details

    def resume_cv_pipeline(self, job_url: str, user_data_path: str = demo_data_path):
        """Run the Auto Apply Pipeline.

        Args:
            job_url (str): The URL of the job to apply for.
            user_data_path (str, optional): The path to the user profile data file.
                Defaults to os.path.join(module_dir, "master_data','user_profile.json").

        Returns:
            None: The function prints the progress and results to the console.
        """
        try:
            if user_data_path is None or user_data_path.strip() == "":
                user_data_path = demo_data_path

            print("Starting Auto Resume and CV Pipeline")
            if job_url is None and len(job_url.strip()) == "":
                print("Job URL is required.")
                return
            
            # Extract user data
            user_data = self.user_data_extraction(user_data_path)

            # Extract job details
            job_details, jd_path = self.job_details_extraction(url=job_url)
            # job_details = read_json("/Users/saurabh/Downloads/JobLLM_Resume_CV/Netflix/Netflix_MachineLearning_JD.json")

            # Build resume
            resume_path, resume_details, json_formatted_resume = self.resume_builder(job_details, user_data)
            # resume_details = read_json("/Users/saurabh/Downloads/JobLLM_Resume_CV/Netflix/Netflix_MachineLearning_resume.json")

            # Generate cover letter
            cv_details, cv_path = self.cover_letter_generator(job_details, user_data)

            # Calculate metrics
            # for metric in ['job_fit_score', 'jaccard_similarity', 'overlap_coefficient', 'cosine_similarity']:
            for metric in ['job_fit_score']:
                print(f"\nCalculating {metric}...")

                if metric == 'vector_embedding_similarity':
                    llm = self.get_llm_instance('Ollama')
                    user_personlization = globals()[metric](llm, json.dumps(resume_details), json.dumps(user_data))
                    job_alignment = globals()[metric](llm, json.dumps(resume_details), json.dumps(job_details))
                    job_match = globals()[metric](llm, json.dumps(user_data), json.dumps(job_details))
                    print("User Personlization Score(resume,master_data): ", user_personlization)
                    print("Job Alignment Score(resume,JD): ", job_alignment)
                    print("Job Match Score(master_data,JD): ", job_match)
                elif metric == 'job_fit_score':
                    original_resume_eval = self.llm.get_response(prompt=JOB_FIT_PROMPT.format(job_description=json.dumps(job_details), resume=json.dumps(json_formatted_resume)),need_json_output=True)
                    refined_resume_eval = self.llm.get_response(prompt=JOB_FIT_PROMPT.format(job_description=json.dumps(job_details), resume=json.dumps(resume_details)),need_json_output=True)
                    print("Job Fit Score(original resume): ", original_resume_eval.get("overall_score"))
                    print("Job Fit Score(refine resume): ", refined_resume_eval.get("overall_score"))
                    print("Missing skills(original resume): ", original_resume_eval.get("missing_skills"))
                    print("Missing skills(refine resume): ", refined_resume_eval.get("missing_skills"))
                    job_alignment_original = json.dumps(original_resume_eval)
                    job_alignment_refined = json.dumps(refined_resume_eval)

                else:
                    user_personlization = globals()[metric](json.dumps(resume_details), json.dumps(user_data))
                    job_alignment = globals()[metric](json.dumps(resume_details), json.dumps(job_details))
                    job_match = globals()[metric](json.dumps(user_data), json.dumps(job_details))
                    print("User Personlization Score(resume,master_data): ", user_personlization)
                    print("Job Alignment Score(resume,JD): ", job_alignment)
                    print("Job Match Score(master_data,JD): ", job_match)

            print("\nDone!!!")
        except Exception as e:
            print(e)
            return None