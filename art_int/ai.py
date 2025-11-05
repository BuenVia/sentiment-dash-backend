import json, os, sqlite3
from .prompts import system_prompt, user_prompt
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama
from langchain.messages import ToolMessage

load_dotenv()

class AIModel():
    
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt

    # CREATE FAKE DATA
    # Creates AI generated data by calling Claude and returning a JSON response.
    def chat(self):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.user_prompt}
        ]
        try:
            # chat = ChatOllama(model="llama3.2")
            chat = ChatAnthropic(model="claude-haiku-4-5-20251001", api_key=self.api_key, max_retries=2)
            response = chat.invoke(messages)
            response = response.content.replace("```json", "").replace("```", "")
            result = json.loads(response)
            return result
        except Exception as err:
            return err
    
    # Main function to call chat function which creates AI generated review data
    def get_ai_data(self):
        response = self.chat()
        return response

    # GET AI SUMMARY
    # Tool function that reads the database and returns the reviews
    @tool
    def get_db_data(query: str = "SELECT feedback_text, sentiment_score, sentiment_label FROM feedback_feedback LIMIT = 2", limit: int = 5) -> str:
        """Search the reviews database for records which mach the query.

        Args:
            query (str): search terms to look for
            limit (int, optional): Maximum number of results to look for. Defaults to 5.

        Returns:
            str: a string of the results.
        """
        DB = "db.sqlite3"
        with sqlite3.connect(DB) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return result

    # Handles the request to get an AI summary. A tool cool is made to read the database and the a call to Claude to summarise the data in Markdown form.
    def get_req(self):
        try:
            tools = [self.get_db_data]
            api_key = os.getenv("ANTHROPIC_API_KEY")
            model = ChatAnthropic(model="claude-haiku-4-5-20251001", api_key=api_key, max_retries=2)
            agent = create_agent(model=model, tools=tools, system_prompt="You are a helpful assistant.")
            result = agent.invoke(
                {"messages": [{"role": "user", "content": "What are the latest reviews in the database?"}]},
                context={"user_role": "expert"}
                )
            tool_message = [m for m in result["messages"] if isinstance(m, ToolMessage)]
            
            if tool_message[0].content != "":
                data = tool_message[0].content
                messages = [
                    {"role": "system", "content": "You are a helpful assistant who specialises in providing feedback and summarys on customer review data."},
                    {"role": "user", "content": f"""
                    Use the following data to provide a summary on recent customer feedback. You should explain the general feeling amongst customers and also any common themes. Your summarys must be less than 100 words and always returned in Markdown.\n
                    {data}
                    """}
                ]
                response = model.invoke(messages)
                return response.content
            return "No data was found. Please try again."
        except Exception as err:
            return f"The call was unsuccessful. Please try again. If this persists, contact the site admin.\n\n{err}"

