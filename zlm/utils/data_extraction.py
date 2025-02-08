'''
-----------------------------------------------------------------------
File: data_extraction.py
Creation Time: Oct 31st 2023 2:17 pm
Author: Saurabh Zinjad, Amey Bhilegonkar
Developer Email: zinjadsaurabh1997@gmail.com, abhilega@asu.edu
Copyright (c) 2023 Saurabh Zinjad. All rights reserved | GitHub: Ztrimus, ameygoes
-----------------------------------------------------------------------
'''
import re
import json
import PyPDF2
import pdfplumber
import requests
from bs4 import BeautifulSoup
import streamlit as st
from langchain_community.document_loaders import PlaywrightURLLoader, UnstructuredURLLoader, WebBaseLoader

def read_data_from_url(url):
        try: 
            url_content = ""

            basic_selectors = ["header", "footer"]
            linkedin_selectors = ["#main-content > section.right-rail",
                                  ".job-alert-redirect-section", ".similar-jobs"]
            
            # TODO: Filter out selectors bassed on the website
            all_selectors = basic_selectors

            unstr_loader = UnstructuredURLLoader(urls=[url], ssl_verify=False, remove_selectors=all_selectors)
            playwright_loader = PlaywrightURLLoader(urls=[url], remove_selectors=all_selectors)
            web_loader = WebBaseLoader(url)

            pages = []
            for loader in [playwright_loader, unstr_loader, web_loader]:
                pages = loader.load()
                if pages != []:
                    break

            for page in pages:
                if page.page_content.strip() != "":
                    # text = page.extract_text().split("\n")
                    text_list = page.page_content.split("\n")

                    # Remove Unicode characters from each line
                    cleaned_texts = [re.sub(r'[^\x00-\x7F]+', '', line) for line in text_list]
                    cleaned_texts = [text.strip() for text in cleaned_texts if text.strip() not in ['', None]]

                    # Join the lines into a single string
                    cleaned_texts_string = '\n'.join(cleaned_texts)
                    url_content += cleaned_texts_string
                
                return url_content
        except Exception as e:
            print(e)
            return None

def clean_text(text):
    """Remove (cid:xxx) encoding issues and non-ASCII characters."""
    text = re.sub(r"\(cid:\d+\)", "", text)  # Remove (cid:xxx) patterns
    text = re.sub(r"[^\x00-\x7F]+", " ", text)  # Remove non-ASCII characters
    # text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
    return text

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"  # Extract selectable text
    return text

def extract_text(pdf_path: str):
    extracted_text = extract_text_from_pdf(pdf_path)
    cleaned_text = clean_text(extracted_text)
    return cleaned_text.strip()
    # resume_text = ""
    #
    # with open(pdf_path, 'rb') as file:
    #     pdf_reader = PyPDF2.PdfReader(file)
    #     num_pages = len(pdf_reader.pages)
    #
    #     for page_num in range(num_pages):
    #         page = pdf_reader.pages[page_num]
    #         text = page.extract_text()
    #         if not text:
    #             continue
    #         text_lines = text.split("\n")
    #         cleaned_text = [re.sub(r'[^\w\s,.!?@#&()\-\']+', '', line) for line in text_lines]
    #         # Remove Unicode characters from each line
    #
    #         # Join the lines into a single string
    #         cleaned_text_string = '\n'.join(cleaned_text).strip()
    #         resume_text += cleaned_text_string + "\n"
    #
    #     return resume_text.strip()

def get_url_content(url: str):
    """ Extract text content from any given web page

    Args:
        url (str): Webpage web link
    """    
    try:
        # getting response object
        res = requests.get(url)
        # Initialize the object with the document
        soup = BeautifulSoup(res.content, "html.parser")
        
        # Get the whole body tag
        tag = soup.body
        text_content = ""
        # TODO: Preprocessing of data, like remove html tags, remove unwanted content, etc.
        
        # Print each string recursively
        for string in tag.strings:
            string = string.strip()
            if string:
                text_content += string + "\n"

        return text_content
    except Exception as e:
        print(e)
        return None