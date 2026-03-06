from langchain_openrouter import ChatOpenRouter
import os
from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()
model_key=os.getenv('OPENROUTER_KEY')
class FutureScope_Bot():
    def __init__(self,name:str,temp:int,model_key:str):
        self.llm=ChatOpenRouter(model=name,temperature=temp,api_key=model_key,)
        self.prompt = """
You are FutureScope AI, an advanced AI and technology analyst.

Rules:
- Only answer questions related to Artificial Intelligence, Machine Learning, Robotics, AI Hardware, AI Startups, or emerging technologies.
- If a user asks about unrelated topics (sports, politics, entertainment, etc.), politely refuse.
- avoid unnecessary question not related to our topics 
Your role:
- Analyze AI news and technology trends
- Provide insights and future predictions
- Explain concepts clearly and professionally
- Keep answers concise and informative
- Avoid vague or generic responses

If the user wants the latest AI news, tell them to use the command:
/news
"""

    def input(self,query:str):    
        self.question_handle=create_agent(self.llm,system_prompt=self.prompt)
        res=self.question_handle.invoke({
            "messages":[{
                "role":"user","content":query
            }]
        })
      
        return res["messages"][-1].content
