# Proyect: GitHub Assistant AI using MCP

A weekend project that connects a React UI to OpenAI's **Model Context Protocol (MCP)** to perform GitHub operations using natural language.

The app allows users to:

- Ask for their latest commits in a repository
- Trigger GitHub actions like creating branches
- Interact with a memory-aware assistant powered by OpenAI's Assistants API

---

## 🧰 Technologies Used

### 🖥️ Frontend

- React (Create React App)
- Axios

### 🧠 Backend

- Python
- FastAPI
- OpenAI API (MCP + Assistants + Threads + Tool Use)
- GitHub REST API (via Personal Access Token)

### 🐳 Infrastructure

- Docker
- Docker Compose

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/luisSilvaEs/github-assistant-ai.git
cd github-assistant-ai
```

### 2. Add environment variables

Create a .env file inside `backend/`:

```bash
# backend/.env
OPENAI_API_KEY=sk-xxx
GITHUB_PAT=ghp-xxx
GITHUB_USER=your-github-username
OPENAI_ASSISTANT_ID=asst-xxx
```

> [!IMPORTANT]
> ⚠️ Do NOT commit this file. It should be ignored via .gitignore.

## 3. MCP function

```json
{
  "name": "get_last_commits",
  "description": "Get the last commits from a GitHub repository",
  "strict": false,
  "parameters": {
    "type": "object",
    "properties": {
      "repo_name": {
        "type": "string",
        "description": "The name of the repository"
      },
      "count": {
        "type": "integer",
        "description": "Number of commits to fetch (default 3)"
      }
    },
    "required": ["repo_name"]
  }
}
```

> [!NOTE]
> Do not forget to create an AI Assistant first [https://platform.openai.com/assistants/](https://platform.openai.com/assistants/)
> Also, there is a cost for using Open AI API and it is additional to the cost if you are already paying Chat GPT. Therefore, consider a $10USD montly. If call to the API exceeds free tier, the cost fill increase. You can set alarms though.

## 4. Run the app with Docker

```bash
docker compose up --build
```

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend: [http://localhost:8000](http://localhost:8000)

## Example Usage

You can type prompts like:

- “Show me the last 5 commits from my-repo-name”

“Create a new branch from development called feature/api-integration”

- The assistant will interpret the command and call your GitHub tools accordingly.

### MCP & Tooling Notes

This app uses:

- OpenAI Assistants API with custom tools
- Threads for persistent conversation context
- Function calling to bridge ChatGPT with GitHub's API
