RESUME_CONVERT = """
Instruction: Convert the resume data in plain text into JSON format as the following template:
** output template:
{
    'name': "name data",
    'phone': "phone data",
    'email': "email data",
    'linkedin': "linkedin data",
    'summary': "summary data", 
    'work_experience': ["work experience data"], 
    'education': ["education data"],
    'achievements': ["achievements data"], 
    'skill_section': ["skill data"], 
    'projects': ["project data"]
    'certifications': ["certifications data"]
}
** Note that do not alter or modify original data information, should include all keys showed in the template, and keep the value of keys as empty if no relevant data is found in the resume.

"""

JD_CONVERT = """
Instruction: Convert the job description in plain text into JSON format as the following template.
** output template:
{
    'company_name': "company name",
    'url': "url",
    'job_title': "job title",
    'responsibilities': ["responsibilities data"],
    'qualifications': ["qualifications data"], 
    'preferred_experience': ["preferred skill data"], 
    'overview': "overview of job description"
}
Note that do not alter or modify original data information, should include all keys in the template, and keep the value of keys as empty if no relevant data is found in the job description data.

"""
