import os
import pandas as pd
import ast
DATA_FOLDER = os.path.join(os.path.dirname(__file__))
FILENAME_JOB_EXT = "jd_ext_local.json"
FILENAME_JOB_POSTINGS = "posting_samples.csv"
FILENAME_RES_EXT_RAW = "resume_ext_raw.csv"
FILENAME_RES_EXT = "resume_ext.json"
RES_COLS_DISP = ['summary','skill_section' , 'work_experience', 'projects', 'education', 'certifications']
# RES_COLS_EVAL = ['skill_section.hard_skills', 'skill_section.soft_skills' , 'education', 'work_experience', 'certifications', 'achievements']
RES_COLS_EVAL = ['skill_section.hard_skills', 'skill_section.soft_skills', 'work_experience', 'projects']
RECOMM_COLS_DISP = ['job_title','company_name','job_responsibilities','required_qualifications','preferred_qualifications', 'keywords']


if __name__ == "__main__":
    df_res = pd.DataFrame(columns=RES_COLS_DISP)
    with open(f"{DATA_FOLDER}/{FILENAME_RES_EXT_RAW}", "r") as f:
        df_res = pd.read_csv(f, index_col=0)
        f.close()
    # change the column values from str to list
    for col in RES_COLS_EVAL:
        if col in df_res.columns:
            try:
                print(f"Column({col}) is of type {type(df_res[col][0])} befoere processing")
                df_res[col] = df_res[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
                print(f"Column({col}) is of type {type(df_res[col][0])} after processing")
                print(df_res[col][0:2])
            except Exception as e:
                st.error(f"An error occurred while processing column {col}: {e}")
                print(e)
    # fill the empty columns with 
    df_res['name'].fillna('James Bond', inplace=True)
    df_res['phone'].fillna('+44 1962 0072025', inplace=True)
    df_res['email'].fillna('007@sis.gov.uk', inplace=True)
    df_res['github'].fillna('github.com/jamespond', inplace=True)
    df_res['linkedin'].fillna('linkin.com/jamespond', inplace=True)
    df_res['media'] = df_res.apply(lambda row: {'github': row['github'], 'linkedin':row['linkedin']}, axis=1) # required for resume builder
    df_res["skill_section"] = df_res['skill_section.hard_skills']+ df_res['skill_section.soft_skills']
    print (f"Resume data: {df_res[['work_experience', 'projects']].head()}")
    
    # write the processed data to a new file
    df_res.to_json(f"{DATA_FOLDER}/{FILENAME_RES_EXT}", index=False)
