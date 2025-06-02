# AskLytics

**AskLytics** is an intelligent, conversational data analytics assistant that enables users to ask natural language questions and fetch business insights directly from a MySQL database. Built using **FastAPI** (for the backend) and **Streamlit** (for the frontend), it leverages **LLMs (Groq + LLaMA 3.1 8B)** to dynamically generate and execute safe SQL queries.

---

## 🚀 Features

- 💬 Conversational chat interface for business data queries
- 🧠 LLM-based natural language to SQL translation
- ✅ Automatically retries failed queries (up to 3 times)
- 🔒 SQL safety guardrails (blocks DDL/DML like `DROP`, `DELETE`, etc.)
- 💾 Maintains conversation context per session
- 🧹 Clear chat history per `conversation_id`
- 🧪 Health check endpoint
- 📊 Streamlit frontend with scrollable chat history and persistent input

---

## 📁 Project Structure

```
AskLytics/
├── Backend/
│   ├── app.py                    # FastAPI main backend entry point
│   ├── chat.py                   # Handles chat interactions and query execution
│   ├── config.py                 # Configuration and constants
│   ├── helper.py                 # Utility functions (e.g., get/create conversation)
│   ├── prompts.py                # Prompt templates for LLM
│   ├── pydanticModel.py          # Pydantic models for input/output validation
│   └── requirements.txt          # Python dependencies for backend
│
├── Frontend/
│   ├── app.py                    # Streamlit or frontend app entry point
│   └── requirements.txt          # Python dependencies for frontend
│
├── .gitignore                   # Files and folders to ignore in Git
└── README.md                    # Project documentation
```

---

```markdown
## 🚀 Setup Instructions

Follow these steps to run the AskLytics project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/AskLytics.git
cd AskLytics
```

### 2. Backend Setup

```bash
cd Backend
```

- (Optional) Create and activate a virtual environment:
  ```bash
  python -m venv .venv
  source .venv/bin/activate  # On Windows: .venv\Scripts\activate
  ```

- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

- Create a `.env` file in the `Backend/` directory and add the following:
  ```env
  GROQ_API_KEY=your_api_key
  DB_CONNECTION_STRING=your_db_connection_string
  ```

- Run the backend FastAPI server:
  ```bash
  uvicorn app:app --reload --port 8005
  ```

### 3. Frontend Setup

```bash
cd Frontend
```

- (Optional) Create and activate a virtual environment:
  ```bash
  python -m venv .venv
  source .venv/bin/activate  # On Windows: .venv\Scripts\activate
  ```

- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

- Run the Streamlit frontend:
  ```bash
  streamlit run app.py
  ```

### 4. Test the Application

- Check if backend is running:
  [http://localhost:8005/health-check](http://localhost:8005/health-check)

- Frontend should open automatically in your browser.

✅ You're ready to start asking analytics questions using natural language!
```


---

## 📦 API Endpoints

- `GET /health-check` → Check server status
- `POST /chat` → Send a user message and get response
- `POST /clear_chat` → Clear conversation history

---

## 🧠 Model Info

- **Model Used**: `llama-3.1-8b-instant` via **Groq API**
- Prompts the model for SQL query generation from conversation context

---

## ⚠️ Notes

- Does not allow DML/DDL queries like DELETE, DROP, UPDATE, etc.
- Queries must be SELECT-type only to ensure safety
- Retry mechanism handles 3 iterations with model refinement

---

## 📄 License

This project is for internal and educational use. Licensing to be determined.

---

## 👨‍💻 Author

Made with ❤️ by Akash Kumar Singh