
![StudyBite Logo](./frontend/icon.svg)

# **StudyBite: Visual Learning Companion**  



## **"Transform confusion into clarity. Visualize knowledge. Master any concept."**  



## **Problem Statement:**  

Students find it difficult to grasp certain ideas through learning limited to written text. It is necessary to have a visual and interactive tool that can illustrate concepts and aid understanding.



## **Overview:**  
**StudyBite** is a cutting-edge educational chatbot crafted to assist students in understanding intricate ideas and clarifying uncertainties through **visual learning**. By offering interactive **graphics**, brief **video segments**, and a **Create Notes** function, **StudyBite** provides a more captivating and intuitive learning journey than conventional text-focused responses.


## **Objective:**  

Empower students to understand difficult concepts faster by combining AI-driven explanations with tailored visual clips, fostering a deeper and more memorable learning process.

## Installation

env.list file which should contain 

   
[Guide to get GROQ API key](https://www.youtube.com/watch?v=TTG7Uo8lS1M)

[Guide to get GEMINI API key](https://www.youtube.com/watch?v=OVnnVnLZPEo)

[Guide to get BING Search API key](https://www.youtube.com/watch?v=gqMwGVvZMDY)

[Guide to get ELEVEN LABS key](https://www.youtube.com/watch?v=9zFBc-yH0hU)

#### To Get Bing Search API for free contact Team CoderOff on whatsapp


```bash
    

    GROQ_API_KEY=api_key
    BING_API_KEY=api-key
    GEMINI_API_KEY=api-key
    11_LABS=api-key
    model='llama3-groq-70b-8192-tool-use-preview'
```

### Step 1 :

Install the Packages for StudyBite to work.

```bash
  cd git clone https://github.com/shreesha345/hackathon/
```
### Step 2 :

Install Docker from https://www.docker.com/

### Step 3 : 

```bash
    python run.py start
```


## **Key Features:**  
- **Visual Explanations:** Generate custom visuals or clips based on the student’s query.  
- **Topic-Specific Video Clips:** Extract and present concise video snippets focused on the exact topic the student needs to learn.  
- **Create Notes:** Enable students to compile and organize notes directly from the chatbot’s responses and visual aids, making revision easier and more structured.  



## **Who Can Benefit:**  
- **Students:** Enhance learning by visualizing tough concepts and organizing study materials effectively.  
- **Educators:** Use **StudyBite** as a supplementary tool to support teaching, provide quick visual aids, and assist in note creation.

## File Descriptions

### Configuration Files
- **eslint.config.js**: Configures ESLint for TypeScript, React, and hooks.
- **postcss.config.js**: Enables TailwindCSS and Autoprefixer plugins for styling.
- **tailwind.config.js**: Sets up TailwindCSS with content sources and no plugins.
- **tsconfig.app.json**: Defines strict linting rules and compiler options for TypeScript.
- **tsconfig.node.json**: Manages TypeScript project references with specific configurations.
- **vite.config.ts**: Configures Vite for strict linting, ES2022+ compatibility, and bundler mode.

### Core Application Files
- **index.html**: Establishes the root for a Vite-powered React application.
- **package-lock.json**: Locks dependencies to specific versions for consistency.

### Backend Services
- **app.py**: FastAPI app handling chat interactions with a LangChain-based educational agent.
- **dubapi.py**: FastAPI service for dubbing uploaded videos into specified languages.
- **notesapi.py**: Sets up AI agents to create, edit, and proofread educational content.
- **search.py**: Performs Bing searches and extracts full-text articles using BeautifulSoup.
- **youtube_search.py**: Retrieves YouTube video details using `yt_dlp`.


## **Credits:**  
This project was made possible by Shreesha, Samarth,Laksh and Alen.

## **Conclusion:**  
**"Education thrives when learning is visual, interactive, and engaging."**
