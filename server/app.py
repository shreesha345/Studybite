from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from pydantic import BaseModel
from typing import List, Dict
from uuid import uuid4
import os
from dotenv import load_dotenv
from langchain.agents import create_tool_calling_agent, AgentExecutor, tool
from langchain_groq import ChatGroq
from langchain_community.utilities import BingSearchAPIWrapper
from langchain_community.tools.bing_search import BingSearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from trafilatura import fetch_url, extract
from transcript import fetch_transcript
# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize the LLM
llm = ChatGroq(
    model="gemma2-9b-it",
    temperature=0.7,
    timeout=None,
    max_retries=2,
    groq_api_key=groq_api_key
)

# llm = ChatGroq(
#     model="llama3-groq-70b-8192-tool-use-preview",
#     temperature=0.7,
#     timeout=None,
#     max_retries=2,
#     groq_api_key=groq_api_key
# )

@tool
def search_bing(query: str) -> str:
    """Search for up-to-date information from reputable sources."""
    api_wrapper = BingSearchAPIWrapper(bing_subscription_key=os.getenv("BING_API_KEY"), k=3)
    tool = BingSearchResults(api_wrapper=api_wrapper)
    return tool.invoke(query)

@tool
def get_youtube_transcript(url:str) -> str:
    """get the transcript from youtube with just one url as input"""
    return fetch_transcript(url)

@tool
def interactive(question: str, options: List[str], answer: str) -> str:
    """
    Formats an MCQ into HTML, including the correct answer. this is used for intractive the user
    
    Parameters:
    - question: The MCQ question as a string.
    - options: A list of options for the MCQ.
    - answer: The correct answer (e.g., 'A', 'B', etc.) inside <value></value>
    
    Returns:
    - HTML code as a string.
    """
    # Generate the HTML using the provided question, options, and answer
    mcq_html = f"""
        {question}
            <form>
                {''.join(f'<div><input type="radio" name="option" value="{chr(65+i)}"> {chr(65+i)}. {option}</div>' for i, option in enumerate(options))}
            </form>
            <div class="answer" style="display:none;">
                Correct Answer: <value>{answer}</value>
            </div>
    """
    return mcq_html


tools = [interactive,search_bing,get_youtube_transcript]  # Add other tools like search_bing, extract_content as needed

# Define system prompt
system_prompt = """
Expert Professor System Name Studybite

You are an expert professor who explains concepts clearly and creates interactive learning experiences.
Note:
Core Behavior
1. Explain concepts clearly with examples
2. Use code blocks with proper syntax highlighting (```python, ```cpp, etc.)
3. Create interactive MCQs after every explanation

MCQ Rules
Always present MCQs in this interactive HTML format:
Question
```langauge_name(only used to display code otherwise NO using it)
code problems if needed
```
<form>
    <div><input type="radio" name="option" value="A">options</div>
    <div><input type="radio" name="option" value="B">options</div>
    <div><input type="radio" name="option" value="C">options</div>
    <div><input type="radio" name="option" value="D">options</div>
    <div><input type="radio" name="option" value="E">options</div>
</form>
<div class="answer" style="display:none;">
    Correct Answer: <value>answer</value>
</div>

Response Flow
1. Explain the topic
2. Give examples
3. Add MCQs in HTML format
4. Never mention HTML formatting
5. Stay conversational

That's it! Simple, clear, and gets the job done.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store chat histories for different users
chat_histories: Dict[str, List[Dict[str, str]]] = {}

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat/{user_id}", response_model=ChatResponse)
async def chat_endpoint(user_id: str, chat_message: ChatMessage):
    if user_id not in chat_histories:
        chat_histories[user_id] = []

    chat_history = chat_histories[user_id]
    
    langchain_chat_history = []
    for message in chat_history:
        if message["role"] == "human":
            langchain_chat_history.append(HumanMessage(content=message["content"]))
        elif message["role"] == "ai":
            langchain_chat_history.append(AIMessage(content=message["content"]))

    # Check if the request is for MCQ
    if "generate mcq" in chat_message.message.lower():
        # Use the generate_mcq_html tool to create MCQs
        output = interactive(chat_message.message)
    else:
        # Use the agent_executor for regular responses
        output = agent_executor.invoke({
            "input": chat_message.message,
            "chat_history": langchain_chat_history
        })['output']

    chat_histories[user_id].append({"role": "human", "content": chat_message.message})
    chat_histories[user_id].append({"role": "ai", "content": output})

    return ChatResponse(response=output)

@app.post("/clear_history/{user_id}")
async def clear_history(user_id: str):
    if user_id in chat_histories:
        chat_histories[user_id] = []
        return {"message": f"Chat history cleared for user {user_id}"}
    else:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
