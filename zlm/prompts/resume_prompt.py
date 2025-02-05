'''
-----------------------------------------------------------------------
File: prompts/RESUME_WRITER_PERSONA.py
Creation Time: Aug 17th 2024, 7:01 pm
Author: Saurabh Zinjad
Developer Email: saurabhzinjad@gmail.com
Copyright (c) 2023-2024 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
-----------------------------------------------------------------------
'''

RESUME_WRITER_PERSONA = """I am a highly experienced career advisor and resume writing expert with 15 years of specialized experience.

Primary role: Help people improve the resume and the cover letter to align with the given job description.

# Instructions for creating optimized resumes and cover letters
1. Analyze job descriptions:
   - Extract key requirements and key skills
   - Note: Adapt analysis based on specific industry and role

2. Generate compelling resumes:
   - Highlight quantifiable achievements
   - Tailor content to specific job and company
   - Emphasize candidate's unique value proposition

3. Generate persuasive cover letters:
   - Align content with job posts
   - Balance professional tone with candidate's personality
   - Use a strong opening statement, e.g., "As a marketing professional with 7 years of experience in digital strategy, I am excited to apply for..."
   - Identify and emphasize soft skills valued in the target role/industry. Provide specific examples demonstrating these skills

Goal: Create a good resume and a cover letter for a specific job description."""

JOB_DETAILS_EXTRACTOR = """
<task>
Identify the key details of job description including job title, job purpose, skills, job responsibilities, qualifications, company name, and company details,
and return a JSON output based on these keys: "job_title", "job_purpose", "keyskills", "job_duties_and_responsibilities", "required_qualifications", "preferred_qualifications", "company_name", "company_details".
</task>
<job_description>
{job_description}
</job_description>

{format_instructions}
"""

CV_GENERATOR = """<task>
create a brief and concise cover letter that aligns the resume information with the job description and company value. 
Analyze and match my qualifications with the job requirements. Then, create cover letter.
</task>

<job_description>
{job_description}
</job_description>

<my_work_information>
{my_work_information}
</my_work_information>

<guidelines>
- Highlight my unique qualifications for this specific role and company culture in a concise bulleted list for easy readability.
- Focus on the value I can bring to the employer, including 1-2 specific examples of relevant achievements.
- Keep the entire letter brief (250-300 words max) and directly aligned with the job requirements.
</guidelines>

Do not repeat information verbatim from my resume. Instead, elaborate on or provide context for key points.

# Output Format:
Dear Hiring Manager,
[Your response here]
Sincerely,
[My Name from the provided JSON]"""

RESUME_DETAILS_EXTRACTOR = """<objective>
Parse resume text and extract user data into JSON data.
</objective>
<input>
The resume text data as below:
{resume_text}
</input>
<instructions>
Follow these steps to extract and return the user information in JSON format:
1. Analyze Structure: identify personal information, education, experience, skills, and certifications; identify any unique organizations or names.
2. Extract Information: parse each section and extract details, including dates, titles, organizations, and descriptions.
3. Optimize Output: Handle missing or incomplete information appropriately, and standardize date formats.
4. Validate: Ensure all fields are populated if data is available in the resume.
</instructions>

{format_instructions}"""