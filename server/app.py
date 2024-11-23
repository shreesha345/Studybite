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

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize the LLM
llm = ChatGroq(
    model="llama3-groq-70b-8192-tool-use-preview",
    temperature=0.7,
    timeout=None,
    max_retries=2,
    groq_api_key=groq_api_key
)

@tool
def search_bing(query: str) -> str:
    """Search for up-to-date information from reputable sources."""
    api_wrapper = BingSearchAPIWrapper(bing_subscription_key=os.getenv("BING_API_KEY"), k=3)
    tool = BingSearchResults(api_wrapper=api_wrapper)
    return tool.invoke(query)

@tool
def extract_content(link: str) -> str:
    """Extract the give url to provide indept reuslt"""
    downloaded = fetch_url(link)
    result = extract(downloaded, output_format="json", include_comments=False)
    return result

@tool
def generate_mcq_html(question: str, options: List[str], answer: str) -> str:
    """
    Formats an MCQ into HTML, including the correct answer.
    
    Parameters:
    - question: The MCQ question as a string.
    - options: A list of options for the MCQ.
    - answer: The correct answer (e.g., 'A', 'B', etc.).
    
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
                Correct Answer: {answer}
            </div>
    """
    return mcq_html


tools = [generate_mcq_html,search_bing,extract_content]  # Add other tools like search_bing, extract_content as needed

# Define system prompt
system_prompt = """
Expert Professor with Internet and Web Scraping Abilities
You are an expert professor with a vast amount of knowledge across a wide range of fields, including science, technology, mathematics, history, literature, art, and more. You also generate HTML content for MCQs when asked. Respond with valid HTML when requested.
Note: if requested to provide the Mcqs then it should be in the format of html no providing it in the text way. make sure if the the Mcq question is full given.
only the options and the answers are in html content and Never tell that it is formated in Html
if you want to display the code use ```python`` or ``cpp`` etc..
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
        output = generate_mcq_html(chat_message.message)
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
    uvicorn.run(app, host="0.0.0.0", port=8000)
