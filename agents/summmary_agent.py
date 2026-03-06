from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
import os
import datetime
import json
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from tools.fetch_news import Genrate_topic
curr_year=datetime.datetime.now().year

load_dotenv()
model_key=os.getenv('OPENROUTER_KEY')


# print("return data :- ",news_data_api)

class Summary_agent():
    def __init__(self,news_data_api):
        print("Run by Summary Agent Genrative_Topic")
        news_data_api=Genrate_topic().genrate_topic_api()
        format_news=''
        for key in news_data_api:
            for item in news_data_api[key]:
                format_news +=f'''
                            Title:-{item['title']}
                            Snippet:-{item['snippet']}
                            Link:-{item['link']}
                            ------------------------------------                                                   
                           '''
                print('format news :-',format_news)
                # break
        self.summary=self.run(format_news)

    def run(self,data):
        self.llm=ChatOpenRouter(model="meta-llama/llama-3-8b-instruct",api_key=model_key,temperature=0.7)
        prompt='''
                You are an AI Technology Intelligence Analyst.

Your task is to analyze each news article and generate:

1. A concise 2–4 line summary
2. The original article link
3. A star rating out of 5 (with decimal allowed)
4. A one-line justification for the rating

Rate the news based on:
- Global impact
- Technological innovation level
- Industry disruption potential
- Market or funding significance
- Long-term strategic importance

Format your response exactly like this:

--------------------------------------------------

**1. Title of the Article**

Summary:
(2–4 lines explaining the news clearly and professionally)

Link:
(Original link)

Rating:
X.X / 5 ⭐

Reason:
(One-line explanation for rating)

--------------------------------------------------

Do not add extra commentary.
Keep tone professional and analytical.
Avoid repetition.
                '''
        
        news_agent=create_agent(self.llm,system_prompt=prompt)

        res= news_agent.invoke(
            {"messages":[{"role":"user","content":data}]}
        )
        
        print("News is :- ",res['messages'][-1].content)
        output=res['messages'][-1].content
        return output 
# news_agent_reason=Summary_agent(news_data_api)