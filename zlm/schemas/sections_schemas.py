'''
-----------------------------------------------------------------------
File: schemas/sections_schmas.py
Creation Time: Aug 18th 2024, 2:26 am
Author: Saurabh Zinjad
Developer Email: saurabhzinjad@gmail.com
Copyright (c) 2023-2024 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
-----------------------------------------------------------------------
'''

from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl

class Achievements(BaseModel):
    achievements: Optional[List[str]] = Field(default=None,description="job relevant key accomplishments, awards, or recognitions that demonstrate your skills and abilities.")

class Certification(BaseModel):
    name: Optional[str]= Field(default="",description="The name of the certification.")
    by: Optional[str]= Field(default="",description="The organization or institution that issued the certification.")
    link: Optional[str]= Field(default="",description="A link to verify the certification.")

class Certifications(BaseModel):
    certifications: Optional[List[Certification]] = Field(default=None,description="job relevant certifications that you have earned, including the name, issuing organization, and a link to verify the certification.")

class Education(BaseModel):
    degree: Optional[str] = Field(default="",description="The degree or qualification obtained and The major or field of study. e.g., Bachelor of Science in Computer Science.")
    university: Optional[str] = Field(default="",description="The name of the institution where the degree was obtained with location. e.g. Arizona State University, Tempe, USA")
    from_date: Optional[str] = Field(default="",description="The start date of the education period. e.g., Aug 2023")
    to_date: Optional[str] = Field(default="",description="The end date of the education period. e.g., May 2025")
    courses: Optional[List[str]] = Field(default=None,description="Relevant courses or subjects studied during the education period. e.g. [Data Structures, Algorithms, Machine Learning]")

class Educations(BaseModel):
    education: Optional[List[Education]] = Field(default=None,description="Educational qualifications, including degree, institution, dates, and relevant courses.")

class Link(BaseModel):
    name: Optional[str]= Field(default="",description="The name or title of the link.")
    link: Optional[str]= Field(default="",description="The URL of the link.")

class Project(BaseModel):
    name: str | None= Field(description="The name or title of the project.")
    type: str | None = Field(description="The type or category of the project, such as hackathon, publication, professional, and academic.")
    link: str | None= Field(description="A URL or link to the project repository.")
    resources: Optional[List[Link]] = Field(description="Additional resources related to the project, such as documentation, slides, or videos.")
    from_date: str | None= Field(description="The start date of the project. e.g. Aug 2023")
    to_date: str | None= Field(description="The end date of the project. e.g. Nov 2023")
    description: List[str] | None = Field(description="project details")

class Projects(BaseModel):
    projects: Optional[List[Project]] = Field(default=None,description="Project experiences, including project name, type, link, resources, dates, and description.")

class SkillSection(BaseModel):
    name: Optional[str] = Field(default="",description="skills relevant to the job, such as hard skills and soft skills.")
    skills: Optional[List[str]] = Field(default=None,description="Specific skills or competencies within the skill group, such as Python, JavaScript, C#, SQL in programming languages.")

class SkillSections(BaseModel):
    skill_section: Optional[List[SkillSection]] = Field(default=None,description="Skill sections, each containing a group of skills and competencies relevant to the job.")

class Experience(BaseModel):
    role: str = Field(default="",description="job title. e.g. Software Engineer.")
    company: str = Field(default="",description=" name of the company or organization.")
    location: Optional[str] = Field(default="",description="location of the company or organization. e.g. San Francisco, USA.")
    from_date: Optional[str] = Field(default="",description="start date of the employment period. e.g., Aug 2023")
    to_date: Optional[str] = Field(default="",description="end date of the employment period. e.g., Nov 2025")
    description: Optional[List[str]] = Field(default=None,description="work experience, tailored to match job requirements and highly relevant to the specific job.")

class Experiences(BaseModel):
    work_experience: Optional[List[Experience]] = Field(default=None,description="Work experiences, including job title, company, location, dates, and description.")

class Media(BaseModel):
    linkedin: Optional[HttpUrl] = Field(default=None,description="LinkedIn profile URL")
    github: Optional[HttpUrl] = Field(default=None,description="GitHub profile URL")
    medium: Optional[HttpUrl] = Field(default=None,description="Medium profile URL")
    devpost: Optional[HttpUrl] = Field(default=None,description="Devpost profile URL")

class ResumeSchema(BaseModel):
    name: Optional[str] = Field(default="",description="The full name of the candidate.")
    summary: Optional[str] = Field(default="", description="A brief summary or objective statement highlighting key skills, experience, and career goals.")
    phone: Optional[str] = Field(default="", description="The contact phone number of the candidate.")
    email: Optional[str] = Field(default="", description="The contact email address of the candidate.")
    media: Optional[Media] = Field(default=None,description="Links to professional social media profiles, such as LinkedIn, GitHub, or personal website.")
    work_experience: Optional[List[Experience]] = Field(default=None,description="Work experiences, including job title, company, location, dates, and description.")
    education: Optional[List[Education]] = Field(default=None,description="Educational qualifications, including degree, institution, dates, and relevant courses.")
    skill_section: Optional[List[SkillSection]] = Field(default=None,description="Skill sections, each containing a group of skills and competencies relevant to the job.")
    projects: Optional[List[Project]] = Field(default=None,description="Project experiences, including project name, type, link, resources, dates, and description.")
    certifications: Optional[List[Certification]] = Field(default=None,description="job relevant certifications that you have earned, including the name, issuing organization, and a link to verify the certification.")
    achievements: Optional[List[str]] = Field(default=None,description="job relevant key accomplishments, awards, or recognitions that demonstrate your skills and abilities.")