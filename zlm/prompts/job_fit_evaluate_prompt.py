JOB_FIT_PROMPT = """
As an AI assistant evaluating how well a candidate’s resume matches a job description.
### **Evaluation Criteria**:
1. **Skills Match (weight1: 25%)** – Do the required skills match those in the resume?  
2. **Work Experience (weight2: 25%)** – Are past job roles relevant to the position?  
3. **Project Experience (weight3: 20%)** – Do projects demonstrate required expertise?  
4. **Education (weight4: 25%)** – Does the degree meet job requirements?
5. **Summary (weight5: 5%)** – Does Summary align with the job role in the job description? 

### **Inputs**:
**Job Description:**  
{job_description}
**Candidate Resume:**  
{resume}

### Output in JSON format:
- provide scores, including keys: "skills_score", "experience_score", "projects_score", "education_score", "summary_score" (each scored 1.0-10.0)
- also calculate the overall score "overall_score" using formula: overall_score = skills_score * weight1 + experience_score * weight2 + projects_score * weight3 + education_score * weight4 + summary_score * weight5
- list missing skills in the resume and return as a key "missing_skills".
"""

CONTENT_PRESERVED_RATE = """
As an AI assistant evaluating how much key information is retained in the refined resume. 
 
### **Task:**   
- Identify any indispensable missing details.

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
- calculate the overall rate "overall_rate" as a percentage, using formula: overall_rate = (skills_rate+experience_rate+projects_rate+education_rate)*22% + summary_rate*12%
- list missing key information in the refined resume and return as a key "missing_info".
"""