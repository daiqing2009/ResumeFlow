ACHIEVEMENTS = """write a resume section of "Achievements" in JSON format for a job applicant.

Instructions:
- Analyze the given resume data
- Highlight relevant achievements tailored to the job description. 
- Remain the provided achievements.  
- Highlight the strongest matches in the section.   
- Ensure clarity, relevance, and grammatical accuracy.

<achievements>
{section_data}
</achievements>

<job_description>
{job_description}
</job_description>

<example>
  "achievements": [
    "Won E-yantra Robotics Competition 2018 - IITB.",
    "1st prize in “Prompt Engineering Hackathon 2023 for Humanities”",
    "Received the 'Extra Miller - 2021' award at Winjit Technologies for outstanding performance."
  ]
</example>

{format_instructions}
"""

CERTIFICATIONS = """Write a resume section of "Certifications" in JSON format for a job applicant.

Instructions:
- Analyze the given resume data and extract the information of certifications.
- Remain certifications highlighted in the given data.
- Align certifications with the requirements in the job description.
- Ensure grammatical accuracy and clarity. 

<CERTIFICATIONS>
{section_data}
</CERTIFICATIONS>

<job_description>
{job_description}
</job_description>

<example>
  "certifications": [
    {{
      "name": "Deep Learning Specialization",
      "by": "DeepLearning.AI, Coursera Inc.",
      "link": "https://www.coursera.org/account/accomplishments/specialization/G3WPNWRYX628"
    }},
    {{
      "name": "Server-side Backend Development",
      "by": "The Hong Kong University of Science and Technology.",
      "link": "https://www.coursera.org/account/accomplishments/verify/TYMQX23D4HRQ"
    }}
  ],
</example>

{format_instructions}
"""

EDUCATIONS = """Write a resume section of "Education" in JSON format for a job applicant.

Instructions:
- Analyze the education details provided.  
- Create a section highlighting the strongest matches.  
- Ensure clarity, accuracy, and alignment with the job description.  
- Use active voice and concise language.

<Education>
{section_data}
</Education>

<job_description>
{job_description}
</job_description>

<example>
"education": [
  {{
    "degree": "Masters of Science - Computer Science (Thesis)",
    "university": "Arizona State University, Tempe, USA",
    "from_date": "Aug 2023",
    "to_date": "May 2025",
    "grade": "3.8/4",
    "coursework": [
      "Operational Deep Learning",
      "Software verification, Validation and Testing",
      "Social Media Mining"
    ]
  }}
],
</example>

{format_instructions}
"""

PROJECTS = """Write a resume section in JSON format of "Project Experience" for a job applicant.

Instructions:
- Refine the description of projects to align with job requirements.  
- Highlight three relevant projects with impacts. 
- Format each project with 3 bullet points.  
- Quantify results and follow “Did X by doing Y, achieved Z” format.  
- Use the STAR method (Situation, Task, Action, Result).
- Structure each project using concise, active, and job-relevant language.

<PROJECTS>
{section_data}
</PROJECTS>

<job_description>
{job_description}
</job_description>

<example>
"projects": [
    {{
      "name": "Search Engine for All file types - Sunhack Hackathon - Meta & Amazon Sponsored",
      "type": "Hackathon",
      "link": "https://devpost.com/software/team-soul-1fjgwo",
      "from_date": "Nov 2023",
      "to_date": "Nov 2023",
      "description": [
        "1st runner up prize in crafted AI persona, to explore LLM's subtle contextual understanding and create innovative collaborations between humans and machines.",
        "Devised a TabNet Classifier Model having 98.7% accuracy in detecting forest fire through IoT sensor data, deployed on AWS and edge devices 'Silvanet Wildfire Sensors' using technologies TinyML, Docker, Redis, and celery."
      ]
    }}
  ]
  </example>

  {format_instructions}
  """

SKILLS = """Write a resume section of "Skills" in JSON format for a job applicant.

Instructions:
- Analyze the provided skills and job description.  
- Focus on specific skills required for the job.
- Highlight the most relevant skills in a JSON format.
- Ensure clarity, accuracy, and alignment with the job description. 
- Proofread for grammatical accuracy and clarity.

<SKILL_SECTION>
{section_data}
</SKILL_SECTION>

<job_description>
{job_description}
</job_description>

<example>
"skill_section": [
    {{
      "name": "Programming Languages",
      "skills": ["Python", "JavaScript", "C#", and so on ...]
    }},
    {{
      "name": "Cloud and DevOps",
      "skills": [ "Azure", "AWS", and so on ... ]
    }}
  ]
</example>

  {format_instructions}
  """

EXPERIENCE = """Write a resume section of "Work Experience" in JSON format for a job applicant. 

Instructions:
- Match work experience tailored to the job requirements.
- Highlight three relevant experiences with clear outcomes.
- Include 3 bullet points per experience, quantifying results when possible.  
- Use the STAR method (Situation, Task, Action, Result).
- Format bullet points.
- Use clear, concise, and job-relevant language. 

<work_experience>
{section_data}
</work_experience>

<job_description>
{job_description}
</job_description>

<example>
"work_experience": [
    {{
      "role": "Software Engineer",
      "company": "Winjit Technologies",
      "location": "Pune, India"
      "from_date": "Jan 2020",
      "to_date": "Jun 2022",
      "description": [
        "Engineered 10+ RESTful APIs Architecture and Distributed services; Designed 30+ low-latency responsive UI/UX application features with high-quality web architecture; Managed and optimized large-scale Databases. (Systems Design)",  
        "Initiated and Designed a standardized solution for dynamic forms generation, with customizable CSS capabilities feature, which reduces development time by 8x; Led and collaborated with a 12 member cross-functional team. (Idea Generation)" 
      ]
    }},
    {{
      "role": "Research Intern",
      "company": "IMATMI, Robbinsville",
      "location": "New Jersey (Remote)"
      "from_date": "Mar 2019",
      "to_date": "Aug 2019",
      "description": [
        "Conducted research and developed a range of ML and statistical models to design analytical tools and streamline HR processes, optimizing talent management systems for increased efficiency.",
        "Created 'goals and action plan generation' tool for employees, considering their weaknesses to facilitate professional growth."
      ]
    }}
  ],
</example>

{format_instructions}
"""

SUMMARY = """Write a resume section of "Summary" in JSON format for a job applicant.

Instructions:
- Improve the content of summary section
- Match experience and personal summary tailored to the job requirements.
- Remain the key information of original resume
- Ensure clarity, accuracy, and make the summary informative

<summary>
{section_data}
</summary>

<job_description>
{job_description}
</job_description>

<example>
{{
  "summary": "Results-driven Marketing Professional with 5+ years of experience in digital marketing, brand strategy, and campaign management. Proven track record of increasing online engagement by 40% and driving a 25% boost in sales through data-driven strategies. Skilled in SEO, social media marketing, and analytics tools like Google Analytics and HubSpot. Passionate about creating innovative marketing solutions to help businesses grow. Seeking to leverage expertise in a dynamic, growth-oriented organization."
}}
</example>
{format_instructions}
"""