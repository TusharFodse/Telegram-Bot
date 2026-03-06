from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
import os
from tools.fetch_news import Genrate_topic
from agents.summmary_agent import Summary_agent 
from langchain.agents import create_agent
load_dotenv()

OPEN_ROUTER_KEY=os.getenv('OPENROUTER_KEY')




class Sorting_agent():
    def __init__(self):
        self.prompt='''
       You are a Senior Technology Intelligence Analyst.

Your job is to sort the given AI and technology news articles based on their overall importance and strategic impact.

Evaluate each article based on:

- Global economic impact
- Breakthrough or innovation level
- AI research significance
- Enterprise adoption potential
- Market-moving influence
- Long-term industry disruption

Classify and rank the news into three tiers:

🔥 Tier 1 – Critical Industry Impact
⚡ Tier 2 – Major Development
📌 Tier 3 – Informational / Minor Update

Within each tier, sort from most important to least important.

Return output in this format:

========================================

🔥 Tier 1 – Critical Industry Impact

1. Title
Impact Reason:
Link:

----------------------------------------

⚡ Tier 2 – Major Development

1. Title
Impact Reason:
Link:

----------------------------------------

📌 Tier 3 – Informational / Minor Update

1. Title
Impact Reason:
Link:

========================================

Be concise, analytical, and professional.
Do not rewrite full summaries unless necessary.
Only return sorted results.
'''
        self.llm=ChatOpenRouter(model="meta-llama/llama-3-8b-instruct",api_key=OPEN_ROUTER_KEY)
        self.sort_agent=create_agent(model=self.llm,system_prompt=self.prompt)

    def sorting_data(self,article):
        print("At sorting agent Article is ",article)
        sorted_data=self.sort_agent.invoke(
            {"messages":[{"role":"user",'content':article}]}
        )
        print("Sort Data :-")

        print(sorted_data)
        return sorted_data['messages'][-1].content
    

# print("Final Data :-",final_data)
# sorted_data=Sorting_agent()
# sorted_data=sorted_data.sorting_data(final_data)
