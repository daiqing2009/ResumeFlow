'''
-----------------------------------------------------------------------
File: schemas/job_details_schema.py
Creation Time: Aug 17th 2024, 8:18 pm
Author: Saurabh Zinjad
Developer Email: saurabhzinjad@gmail.com
Copyright (c) 2023-2024 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
-----------------------------------------------------------------------
'''

from typing import List, Optional
from pydantic import BaseModel, Field

class JobDetails(BaseModel):
    job_title: str = Field(description="job title")
    job_purpose: str = Field(description="job role")
    keyskills: List[str] = Field(description="Required skills")
    job_duties_and_responsibilities: List[str] = Field(description="job responsibilities.")
    required_qualifications: List[str] = Field(description="job qualifications.")
    preferred_qualifications: Optional[List[str]] = Field(default=None, description="Additional qualifications as a plus")
    company_name: str = Field(description="Company name")
    company_details: str = Field(description="Company's business details")