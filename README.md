# Titanic Dataset Chat Agent

A production-ready chat agent for exploring the Titanic dataset using natural language, powered by FastAPI, Streamlit, LangChain, and HuggingFace LLMs.

## Features
- Natural language Q&A about the Titanic dataset
- Automatic visualizations (matplotlib) when relevant
- Secure, modular, and production-ready
- Conversational memory, query logging, and more

## Folder Structure

```
project/
    backend/
        main.py
        agent.py
        data_loader.py
        utils.py
    frontend/
        app.py
    titanic.csv
    requirements.txt
    README.md
```

## Setup Instructions

### 1. Clone the repository

```
git clone <repo-url>
cd Assignment
```

### 2. Add Titanic Dataset

Place `titanic.csv` in the project root. You can download it from [Kaggle Titanic Dataset](https://www.kaggle.com/c/titanic/data).

### 3. Set HuggingFace API Token

Create a `.env` file in `backend/` with:

```
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
```

Get your token from https://huggingface.co/settings/tokens

### 4. Install Requirements

```bash
pip install -r requirements.txt
```

### 5. Run FastAPI Backend

```bash
cd backend
uvicorn main:app --reload
```

### 6. Run Streamlit Frontend

```bash
cd ../frontend
streamlit run app.py
```

### 7. Deploying Streamlit

- For Streamlit Cloud, push your repo and set environment variables in the cloud dashboard.

## Security Notes
- Never executes raw LLM-generated code
- All queries and actions are logged
- Input length and timeouts enforced

## Advanced Features
- Conversational memory
- Dataset caching
- Rate limiting
- Answer evaluation

---

**Built by a Senior AI Engineer.**
