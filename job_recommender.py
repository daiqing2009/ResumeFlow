from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
import numpy as np
import os
import torch
# Set the environment variable to avoid loading the torch classes
torch.classes.__path__ = [] # add this line to manually set it to empty. 

# Load the pre-trained model
ITEM_SEPARATOR = " \n "
# embedder = SentenceTransformer("jensjorisdecorte/JobBERT-v2")
embedder = SentenceTransformer("all-MiniLM-L6-v2")
max_seq_length = embedder.max_seq_length
print(f"Max sequence length: {max_seq_length}")
print(f"embedding dimension: {embedder.get_sentence_embedding_dimension()}")
def len_func(text):
    """Calculates the length of a text."""
    return len(embedder.tokenizer.tokenize(text))

text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n",ITEM_SEPARATOR, " "], #first split at paragraph level, if the chunk size exceeds, at sentence/item level, if still exceeds at word level.
    chunk_size = max_seq_length/2,
    chunk_overlap = max_seq_length/4,
    length_function = len_func,
    is_separator_regex=False
)

def get_embeddings(texts):
    """Gets embeddings for a list of texts using a pre-trained model."""
    # fill the empty texts with empty string
    # print(f"Texts: {texts}")
    # texts = [text if text else "" for text in texts]
    
    lengths = [len_func(text) for text in texts]
    # print(f"Lengths of texts: {lengths}")
    # max_length = max(lengths)
    # print(f"Max length of texts: {max_length}")

    splited_texts = [text_splitter.split_text(text) for text in texts]
    # print(f"Splitted texts: {len(splited_texts)} and original texts: {len(texts)}")
    # flatten the list of lists
    flatted_texts = [item for sublist in splited_texts for item in sublist]
    # print(f"Flattened texts: {len(flatted_texts)}")
    # get the embeddings
    embeddings_flatted = embedder.encode(flatted_texts, show_progress_bar=False)
    # print(f"Embeddings flatted: {embeddings_flatted.shape}")
    # average the embeddings of the flated texts
    embeddings = np.zeros((len(splited_texts), embedder.get_sentence_embedding_dimension()))
    pointer = 0
    for i, sublist in enumerate(splited_texts):
        # print(f"Sublist {i}: {len(sublist)}")
        embeddings[i] = embeddings_flatted[pointer:pointer + len(sublist)].mean(axis=0) 
        pointer += len(sublist)
    # print(f"Pointer: {pointer} and flatted texts: {len(flatted_texts)}")
    # print(f"Embeddings: {embeddings.shape}")
    return embeddings

#read extracted resume and job description data
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "data")
FILENAME_JOB_EXT = "jd_ext_local.json"
FILENAME_JOB_POSTINGS = "posting_samples.csv"
FILENAME_RES_EXT = "resume_ext.json"

import pandas as pd
import json
from pymilvus import MilvusClient, Collection
import numpy as np

class Job_Recommender:
    """
    A class to recommend jobs based on resume and job description data.
    """
    def __init__(self, db_path= "job_recommend.db"):
        """_summary_
        Args:
            db_path (str, optional): _description_. Defaults to "job_recommend.db".
            dimension (int, optional): _description_. Defaults to 384.
        """
        db_path = os.path.join(DATA_FOLDER, "db", db_path)
        print(f"DB path: {db_path}")
        self.client = MilvusClient(db_path)
        self.collection_name = "my_job_collection"
        if self.client.has_collection(collection_name=self.collection_name):
            self.client.drop_collection(collection_name=self.collection_name)
            
        dimension = embedder.get_sentence_embedding_dimension()
        self.client.create_collection(
            collection_name= self.collection_name,
            dimension=dimension,
            auto_id=True,
        )

    def init(self):
        '''
        Populate the collection with data.
        '''
        df_jd_ext = pd.read_json(f"{DATA_FOLDER}/init/{FILENAME_JOB_EXT}")
        # df_job_posting = pd.read_csv(f"{DATA_FOLDER}/init/{FILENAME_JOB_POSTINGS}")
        df_jd_ext["id"] = df_jd_ext.index + 1
        
        # add vectors to job extraction data based on required qulification
        df_jd_ext["vector"] = df_jd_ext["required_qualifications"].apply(lambda x: get_embeddings([ITEM_SEPARATOR.join(x)])[0])

        res = self.client.insert(
            collection_name=self.collection_name,
            data=df_jd_ext.to_dict(orient="records"),
        )
        # print(f"Inserted: {res} records")
        return res


    def recommend_by_resumeExt(self, field , filter=None, limit=10, output_fields=['*']):
        """Search for similar vectors in the collection."""
        #TODO: check schema of resume extraction
        
        vector = get_embeddings([ITEM_SEPARATOR.join(field)])
        # print(f"Vector: {type(vector)} and {vector[0].shape}")
        res = self.client.search(
            collection_name= self.collection_name,
            data=[vector[0]],
            filter=filter,
            limit=limit,
            output_fields=output_fields
        )
        print(f"got({len(res[0])}) recommendations")
        # print([rec['entity'] for rec in res[0]])
        return [rec['entity'] for rec in res[0]]

    # TODO: support incremental update of the collection."

if __name__ == "__main__":
    import random

    with open(f"{DATA_FOLDER}/init/{FILENAME_RES_EXT}", "r") as f:
        df_res = pd.read_json(f, orient="records" )
        f.close()
    
    job_recommender = Job_Recommender()
    job_recommender.init()
    print(f"df of length({len(df_res)}) sample: {df_res.iloc[:2]}")
    # Recommend jobs based on resume extraction
    for i in range(5):
        random_index = random.randint(0, len(df_res) - 1)
        res_ext = df_res.iloc[random_index]['skill_section']
        print(f"Resume ({random_index}) extraction: {type(res_ext)}")
        recommendations = job_recommender.recommend_by_resumeExt(res_ext, limit=2)
        # print(f"Recommendation0: {recommendations[0]}")
        print(f"Recommendation job titles: {[rec['job_title'] for rec in recommendations]}")


    

