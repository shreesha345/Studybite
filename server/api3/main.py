from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from crewai import Agent, Task, Crew, LLM
from fastapi.middleware.cors import CORSMiddleware
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai.tools import tool
from dotenv import load_dotenv
import os
from langchain_community.tools.bing_search import BingSearchResults
from langchain_community.utilities import BingSearchAPIWrapper
from youtube_search import youtube_video_main

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify allowed origins like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Specify allowed methods, e.g., ["GET", "POST"]
    allow_headers=["*"],  # Specify allowed headers, e.g., ["Authorization", "Content-Type"]
)

@tool("search engine")
def search_engine(question: str) -> str:
    """search the internet using this tool with just your query"""
    api_wrapper = BingSearchAPIWrapper(bing_subscription_key=os.getenv("BING_API_KEY"), k=3)
    tool = BingSearchResults(api_wrapper=api_wrapper).invoke(question)
    return tool

# @tool("video search")
# def youtube_search_tool(search_term:str) -> str:
#     "searching the youtube to get the best videos for your query"
#     youtube_video_main(search_term)


my_llm = LLM(
              model='gemini/gemini-1.5-flash-002',
              api_key=os.getenv("GEMINI_API_KEY"),
              temperature=0.7
            )

# Agent 1
Lead_Educator = Agent(
  role='Lead Educator',
  goal=
"""
    To oversee the project, ensuring all educational materials are accurate, engaging, and aligned with
    educational standards, while leading the team to create comprehensive, multi-format resources for 
    students across subjects and make sure that it is 1400 and more.
""",
    

  backstory=
"""
    The Lead Educator is an experienced educator with over 15 years of teaching and curriculum
    development expertise. After working in both traditional classrooms and as an instructional designer,
    they realized the need to create a more accessible, interactive, and flexible learning experience for
    students. Passionate about educational equity, they took on the role of leading this team to create
    high-quality notes and videos that would be available to a wide range of learners. With a strong
    understanding of pedagogy and educational standards, the Lead Educator guides the team, ensuring
    that content is aligned with curriculum goals and meets the needs of diverse students.
""",            
  tools=[search_engine],  # Optional, defaults to an empty list
  llm=my_llm,
  verbose=True,
  max_retry_limit=2,
  allow_delegation=True
)


# Agent 2
Multi_Subject_Educators = Agent(
  role='Multi Subject Educators',
  goal=
"""
    To create clear, concise, and engaging notes across multiple subjects, ensuring that complex topics
    are broken down into digestible content. The Multi-Subject Educator will also help script educational
    videos to support the written notes, providing students with diverse learning formats.
""",

  backstory=
"""
    The Multi-Subject Educator is a versatile teacher with a broad knowledge base across most of the 
    subjects With years of experience teaching students of varying age
    groups, they have developed a unique ability to simplify complex concepts from different disciplines,
    making learning engaging and accessible. Their passion for education stems from a belief in the
    interconnectedness of subjects, and they enjoy showing students how knowledge from one area can
    complement and enrich another. They are adept at tailoring content to diverse learning needs,
    providing students with a well-rounded educational experience.
""",            
  tools=[],  # Optional, defaults to an empty list
  llm=my_llm,  # Optional
  verbose=True,
  max_retry_limit=2
)

# agent 3
Content_Writer = Agent(
  role='Content Writer',
  goal=
"""
    To write engaging, clear, and well-structured notes and video scripts that are both informative and
    student-friendly, ensuring that the content resonates with a diverse range of learners.
""",

  backstory=
"""
    The Content Writer has a natural gift for language and a passion for making complex information
    easy to understand. After studying Literature and Education, they began creating educational
    content, refining their ability to turn dry facts into engaging, accessible material. They believe that
    the best notes are those that are not only accurate but also compelling and easy to follow. By
    crafting clear, student-friendly content, the Content Writer aims to transform traditional educational
    materials into something students can actively engage with and enjoy.
""",            
  tools=[],  # Optional, defaults to an empty list
  llm=my_llm,  # Optional
  verbose=True,
  max_retry_limit=2
)

# Agent 4
Proofreader = Agent(
  role='Proofreader',
  goal=
"""
    To ensure that all educational content—notes, video scripts, and other written materials—are error-
    free, concise, and easy to understand, helping students learn without unnecessary confusion or
    distractions and too if flowcharts and diagram is needed then use Mermaid structure.
""",

  backstory=
"""
    The Editor/Proofreader is a meticulous professional with a keen eye for detail. After years of working
    in publishing and content editing, they developed a deep understanding of how important clarity
    and precision are in educational materials. With a background in English and editing, they joined the
    team to ensure that the content—whether notes or video scripts—is polished, grammatically correct,
    and easy to follow. They are passionate about ensuring that students are not distracted by errors and
    can focus on learning effectively.
""",            
  tools=[search_engine],  # Optional, defaults to an empty list
  llm=my_llm,  # Optional
  verbose=True,
  max_retry_limit=2,
  
)

# Youtube_Expert = Agent(
#   role='Youtube Expert content Extractor',
#   goal= 
#   """
#   I need you to locate a YouTube video that includes <iframe> tags for embedding purposes, ideally with a detailed explanation or demonstration of how embedding works. The content should be clear, easy to follow, and suitable for educational or tutorial purposes. Provide me with the link to the video and a brief summary of its content.
#   """,

#   backstory= 
#   """
#   The Youtube Expert is skilled at finding content that includes specific technical details, such as embedding videos. With years of experience in curating and extracting valuable YouTube resources, this agent is focused on identifying tutorials or guides that showcase the technical use of YouTube features, such as embedding videos via <iframe> tags.
#   """,

#   tools=[youtube_search_tool],  # Optional, defaults to an empty list
#   llm=my_llm,  # Optional
#   verbose=True,
#   max_retry_limit=2
# )

task1 = Task(
    expected_output=(
        "A detailed Notes of {topic}, covering all the foundation to advanced"
    ),
    description=(
        "Research and generate a comprehensive Notes for {topic}, ensuring the content is "
        "thorough, includes significant ,covering all the foundation to advanced and avoids superficial summaries."
    ),
    agent=Lead_Educator,
)

task2= Task(
        expected_output=(
        "provide all the details for the perticular subject knowledge and also provide some examples"
        "make sure that it is easy to understand and also basic to advanced"
    ),
    description= (
        "provide easy to understand concepts and make sure that you provide them with examples how the user wants"
    ),
    agent=Multi_Subject_Educators
)

task3= Task(
        expected_output=(
            "should be simple easy to understand and intresting with examples how the user wants"
    ),
    description= (
        "should be simple and easy understanding"
    ),
    agent=Content_Writer,
    output_file='output.md'
)

# Create Crew
my_crew = Crew(
    agents=[Lead_Educator, Multi_Subject_Educators, Content_Writer, Proofreader],
    tasks=[task1, task2, task3],
    verbose=True
)

# Input query model
class QueryModel(BaseModel):
    topic: str

# Status dictionary to track job progress and result
status = {"status": "idle", "message": "No active process", "output_file": None}

@app.post("/process")
async def process_topic(query: QueryModel, background_tasks: BackgroundTasks):
    """
    Endpoint to process a topic and write the output to a file.
    """
    global status
    status["status"] = "running"
    status["message"] = "Processing the topic..."
    status["output_file"] = None

    def run_crew():
        global status
        try:
            crew = my_crew.kickoff(inputs={"topic": query.topic})
            with open('output.md', 'w') as f:
                f.write(str(crew))
            status["status"] = "completed"
            status["message"] = "Processing completed successfully."
            status["output_file"] = 'output.md'
        except Exception as e:
            status["status"] = "failed"
            status["message"] = str(e)
            status["output_file"] = None

    # Run the crew process in the background
    background_tasks.add_task(run_crew)
    return {"status": "started", "message": "The process has started."}

@app.get("/status")
async def get_status():
    """
    Endpoint to get the current status of the process.
    """
    return status

@app.get("/output")
async def get_output():
    """
    Endpoint to retrieve the output file content after the process is complete.
    """
    if status["status"] != "completed":
        raise HTTPException(status_code=400, detail="Process not completed yet.")
    try:
        with open(status["output_file"], 'r') as f:
            content = f.read()
        return {"status": "completed", "output": content}
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Output file not found.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
