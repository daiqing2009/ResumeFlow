JOB_FIT_PROMPT = """Instruction: You are an AI recruiter evaluating how well a candidate’s resume matches a job description. Grade it based on these criteria
### **Evaluation Criteria**:
1. **Skills Match** – Give higher score if more qualifications in job description show in the resume. And give less points if missing part of qualifications. Give zero point if no alignment with job requirements.
2. **Work Experience** – Give higher score if past job roles align with the job description. Lower score if less related. Give zero point if no alignment with job requirements.
3. **Project Experience** – Give higher score if projects demonstrate required skills or qualifications. Lower score if irrelevant. Give zero point if no alignment with job requirements.
4. **Education** – Give 10 points if Candidate's degree and study field meet the requirement on education background in the job description, or give 0 point if it doesn't meet job requirements.
5. **Summary** – You should give a higher score if the summary contains required or preferred qualifications in the job description, and give a lower score if information is unrelated or not informative.

**Job Description:**  
{job_description}
**Candidate Resume:**  
{resume}

### Output in JSON format:
- provide scores as keys: "skills_score", "experience_score", "projects_score", "education_score", "summary_score" (each scored 1.0-10.0).
"""

CONTENT_PRESERVED_RATE = """Instruction: You are an AI content reviewer, you need to evaluate how much key information is retained in the refined resume. 

### **Evaluation Criteria**:
1. **Skills** – Do key skills remain in the refined resume?  
2. **Work Experience** – Do work experience remain in the refined resume?
3. **Project Experience** – Does highly relevant project experience remain in the refined resume? 
4. **Education** – Does the information of education background remain in the refined resume?
5. **Summary** – Does key information of summary remain in the refined resume? 

### **Original Resume:**  
{original_resume}  

### **Refined Resume:**  
{refined_resume}  

### **Cosine Similarity score of original resume and refined resume:** {cosine_score} 

### **Output in JSON format :**
- calculate a rate for each section of resume (each rated 0.0-1.0) and return as keys: "skills_rate", "experience_rate", "projects_rate", "education_rate", "summary_rate"
- calculate the overall rate "overall_rate" as a percentage, using formula: overall_rate = (skills_rate+experience_rate+projects_rate+education_rate)*23% + summary_rate*8%
"""

MISSING_SKILL_PROMPT = """
Instruction: As an AI assistant, you need to identify skills missing in the resume but existing in the job description.

### **Inputs**:
**Required Skills of Job Description:**  
{job_description}

**Listed Skills of Candidate's Resume:**  
{resume}

### Output in JSON format:
- Analyze the given skills information
- List required skills missing in the resume but existing in the job description and return as a key "missing_skills".
- Remain the original keywords of skills in the job description, do not modify its words and meaning
"""