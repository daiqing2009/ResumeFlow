ACHIEVEMENTS = """Instructions: Refine and rewrite the given "achievements" section in JSON format. 
Follow these criteria:
1. Only Return refined "achievements" section as a response, don't include other sections.
2. Return achievements as a list of string as your response.
3. Format your response as the following template.
    "achievements": [
        "Won E-yantra Robotics Competition 2018 - IITB.",
        "1st prize in “Prompt Engineering Hackathon 2023 for Humanities”",
        "Received the 'Extra Miller - 2021' award at Winjit Technologies for outstanding performance."
    ]

4. Retain at most 3 key achievements most aligned with job requirements.
5. If no data is given, return an empty list. 
6. Avoid adding or altering achievements beyond formatting improvements.

<RESUME>
{section_data}
</RESUME>

<job_description>
{job_description}
</job_description>
"""

CERTIFICATIONS = """Instructions: Refine and rewrite the given "certifications" section in JSON format. 
Follow these criteria:
1. Only return refined "certifications" section as a response, don't include other sections.
2. Retain all relevant certification details.
3. Format your response as the following template.
  "certifications": [
    {{
      "name": "Deep Learning Specialization",
    }},
    {{
      "name": "Server-side Backend Development",
    }}
  ]

4. Each certification as a string text to output.
5. If no data is provided, return an empty list. 
6. Avoid adding new certifications not present in the original data.

<RESUME>
{section_data}
</RESUME>

<job_description>
{job_description}
</job_description>
"""

EDUCATIONS = """Instruction: Refine and rewrite the given "education" section in JSON format. 
Follow these criteria:
1. Only return "education" section as a response, don't include other sections.
2. Format your response as the following template.
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

2. Retain all provided details of education and degree, including institution names, degrees, dates, GPA.
3. Avoid missing or adding any educational details in your response.

<RESUME>
{section_data}
</RESUME>

<job_description>
{job_description}
</job_description>
"""

PROJECTS = """Instructions: Refine and rewrite the given "projects" section in JSON format. 
Follow these criteria:
1. Only return refined "projects" section as a response, don't include other sections.
2. Return "projects" section using the template below.
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

3. Retain at most top 3 relevant projects to the job requirements.
4. In each project description, it should include info, such as Task, Feature, Result.
5. Improve clarity and alignment with the job requirements.
6. Avoid adding details not given in the original resume data..

<RESUME>
{section_data}
</RESUME>

<job_description>
{job_description}
</job_description>
"""

SKILLS = """Instructions: Refine and rewrite the given "skill_section" section of resume in JSON format.
Follow these criteria:
1. Only return refined "skill_section" section as a response, don't include other sections.
2. Format your response as the following template.
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

3. Ensure most relevant skills as the job requires are retained.
4. Add other relevant skills showed in other sections of resume if they are aligned with job requirements.
5. Remove irrelevant details.
6. Avoid adding new skills that are not showed in resume..

<RESUME>
{section_data}
</RESUME>

<job_description>
{job_description}
</job_description>
"""

EXPERIENCE = """Instructions: Refine and rewrite the given "work_experience" section in JSON format. 
Follow these criteria:
1. Return refined "work_experience" section as a response, don't include other sections.
2. Format each experience as the following output template.
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

3. In each experience, description should include information about responsibilities and impacts as string text.
4. Ensure clarity, structure, and alignment with the job description.
5. Retain at most top 3 relevant experience without altering factual details.
6. Avoid adding details not given in the original resume data.

<RESUME>
{section_data}
</RESUME>

<job_description>
{job_description}
</job_description>
"""

SUMMARY = """Instructions: Refine and rewrite the given "summary" section in JSON format. 
Follow these criteria:
1. Return refined "summary" section as a response, don't include other sections.
2. Retain key details while enhancing clarity, conciseness, and alignment with the job description. 
3. Only return "summary" section as a response like the following template, don't include any other sections.
    {{
      "summary": "Results-driven Marketing Professional with 5+ years of experience in digital marketing, brand strategy, and campaign management. Proven track record of increasing online engagement by 40% and driving a 25% boost in sales through data-driven strategies. Skilled in SEO, social media marketing, and analytics tools like Google Analytics and HubSpot. Passionate about creating innovative marketing solutions to help businesses grow. Seeking to leverage expertise in a dynamic, growth-oriented organization."
    }}

4. Ensure a strong, informative summary without adding new, unprovided content.
5. Remove irrelevant and redundant content.
6. No more than 100 words.

<RESUME>
{section_data}
</RESUME>

<job_description>
{job_description}
</job_description>
"""