ACHIEVEMENTS = """Instructions: Optimize the given "achievements" section in JSON format. 
- Each achievement as a string text to output.
- Retain at most 3 key achievements most aligned with job requirements.
- If no data is given, return an empty list. 
- Avoid adding or altering achievements beyond formatting improvements.
- Ensure integrity, readability and accuracy.
- Avoid hallucination.

<RESUME>
{section_data}
</RESUME>

<job_description>
{job_description}
</job_description>

<output_example>
  "achievements": [
    "Won E-yantra Robotics Competition 2018 - IITB.",
    "1st prize in “Prompt Engineering Hackathon 2023 for Humanities”",
    "Received the 'Extra Miller - 2021' award at Winjit Technologies for outstanding performance."
  ]
</output_example>

"""

CERTIFICATIONS = """Instructions: Optimize the given "certifications" section in JSON format. 
- Retain all relevant certification details.
- Each certification as a string text to output.
- If no data is provided, return an empty list. 
- Avoid adding new certifications not present in the original data.
- Ensure integrity and accuracy.
- Avoid hallucination.

<RESUME>
{section_data}
</RESUME>

<job_description>
{job_description}
</job_description>

<output_example>
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
  ]
</output_example>

"""

EDUCATIONS = """Instruction: Optimize the given "education" section in JSON format. 
- Ensure integrity and consistency.
- Retain all provided details of education and degree, including institution names, degrees, dates, GPA. 
- Avoid missing or adding any educational details.
- Avoid hallucination.

<RESUME>
{section_data}
</RESUME>

<job_description>
{job_description}
</job_description>

<output_example>
"education": [
  {{
    "degree": "Masters of Science - Computer Science (Thesis)",
    "university": "Arizona State University, Tempe, USA",
    "from_date": "Aug 2023",
    "to_date": "May 2025",
    "grade": "3.8/4"
  }},
  {{
    "degree": "Bachelor of Science - Computer Science",
    "university": "Bangalore University, Bangalore, India",
    "from_date": "Aug 2019",
    "to_date": "May 2023",
    "grade": "3.6/4"
  }}
]
</output_example>

"""

PROJECTS = """Instructions: Improve the given "projects" section in JSON format. 
- Retain listed projects in the resume.
- Improve clarity and alignment with the job requirements.
- Use clear, concise and professional language. 
- Format each project with bullet points.
- In each project description, it should include info, such as Task, Feature, Result.
- Avoid hallucination or adding details not given in the original resume data..

<RESUME>
{section_data}
</RESUME>

<job_description>
{job_description}
</job_description>

<output_template>
"projects": [
    {{
      "name": "project name1",
      "link": "https://devpost.com/software/project1",
      "from_date": "Nov 2023",
      "to_date": "Nov 2023",
      "description": [
        "introduction of project task, key features, and results."
      ]
    }},
    {{
      "name": "project name2",
      "link": "https://devpost.com/software/project2",
      "from_date": "June 2022",
      "to_date": "July 2022",
      "description": [
        "introduction of project task, key features, and results."
      ]
    }}
  ]
</output_template>

"""

SKILLS = """Instructions: Optimize the given "skill_section" section in JSON format.
- Enhance the structure and alignment with the job description.
- Ensure most relevant skills in resume are retained.
- Add other relevant skills showed in other sections of resume if they are aligned with job requirements.
- Remove irrelevant details.
- Use precise and professional language.
- Avoid adding new skills that are not showed in resume.
- Avoid hallucination.

<RESUME>
{section_data}
</RESUME>

<job_description>
{job_description}
</job_description>

<output_example>
"skill_section": [
    {{
      "name": "Programming Languages",
      "skills": ["Python", "JavaScript"]
    }},
    {{
      "name": "Cloud and DevOps",
      "skills": [ "Azure", "AWS"]
    }}
  ]
</output_example>

"""

EXPERIENCE = """Instructions: Optimize the given "work_experience" section in JSON format. 
- Format each project as the following output_example.
- In each experience, description should include information about responsibilities and impacts as string text.
- Improve clarity, structure, and alignment with the job description.
- Retain all important and relevant experience without altering factual details.
- Avoid adding details not given in the original resume data.

<RESUME>
{section_data}
</RESUME>

<job_description>
{job_description}
</job_description>

<output_example>
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
    }}
  ]
</output_example>

"""

SUMMARY = """Instructions: Optimize the given "summary" section in JSON format. 
- Retain key details while enhancing clarity, conciseness, and alignment with the job description. 
- Ensure a strong, informative summary without adding new, unprovided content.
- Remove irrelevant and redundant content.
- No more than 100 words.
- Avoid hallucination

<RESUME>
{section_data}
</RESUME>

<job_description>
{job_description}
</job_description>

<output_example>
{{
  "summary": "Results-driven Marketing Professional with 5+ years of experience in digital marketing, brand strategy, and campaign management. Proven track record of increasing online engagement by 40% and driving a 25% boost in sales through data-driven strategies. Skilled in SEO, social media marketing, and analytics tools like Google Analytics and HubSpot. Passionate about creating innovative marketing solutions to help businesses grow. Seeking to leverage expertise in a dynamic, growth-oriented organization."
}}
</output_example>

"""