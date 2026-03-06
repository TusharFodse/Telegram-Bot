import os
import datetime
import json
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from dotenv import load_dotenv
import praw
curr_year=datetime.datetime.now().year

load_dotenv()
# search=DuckDuckGoSearchResults(max_results=5)
wrapper=DuckDuckGoSearchAPIWrapper(time='d')
model_key=os.getenv('OPENROUTER_KEY')
class Genrate_topic():
    def genrate_topic_api(self):
        print("Run Function when Main Run........")
        self.all_result_dict={}
        topic_list=["Artificial Intelligence","Large Language Models","Agentic AI","AI Hardware (NVIDIA, AI chips)","Robotics","Edge AI","AI Startups and Funding"]
        for new_topic in topic_list:
            result=wrapper.results(
                f"{new_topic} at {curr_year}"
                ,max_results=5
            )
            self.all_result_dict[new_topic]=result 
        print("ALL results :-")
        print(self.all_result_dict)   
        data=self.all_result_dict 
        
        return data
    
