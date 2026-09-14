# ✦ DHRIVA — AI Assistant

> A modern AI chatbot built with Python, Streamlit, and Groq, featuring persistent conversations, secure user authentication, PDF document Q&A, OCR support, chat management, and export capabilities.

DHRIVA is a conversational AI application designed to provide a clean and practical chatbot experience while demonstrating real-world application development concepts such as authentication, persistent storage, document processing, API integration, error handling, and responsive UI design.

[![GitHub](https://img.shields.io/badge/GitHub-Dhruvanthi--KR-blue?logo=github)](https://github.com/Dhruvanthi-KR/DHRIVA-AI)
[![Live Demo](https://img.shields.io/badge/Live-DHRIVA-green?logo=streamlit)](https://dhriva-ai.streamlit.app/)
---

## ✨ Features

### 🤖 AI Chat

- Natural-language conversations powered by Groq
- Streaming AI responses
- Markdown-formatted responses
- Regenerate assistant responses
- Persistent conversation history
- Custom DHRIVA assistant identity

### 🔐 Authentication

- User registration and login
- Password confirmation during signup
- Minimum password validation
- Secure password hashing using PBKDF2-HMAC SHA-256
- Unique salt for password storage
- User-specific chat data
- Logout functionality

### 💬 Chat Management

- Create new conversations
- Automatically save conversations
- Persistent chat history
- Search previous conversations
- Rename conversations
- Delete conversations
- Open previous conversations
- Automatically generate chat titles

### 📄 Document Q&A

DHRIVA can answer questions based on uploaded PDF documents.

**Text-based PDFs**

- Extracts text using `pypdf`

**Scanned PDFs**

- Automatically falls back to OCR
- Converts PDF pages using `pdf2image`
- Extracts text using Tesseract OCR

The extracted document content is provided as context to the AI so users can ask questions about their uploaded documents.

### 📥 Chat Export

Conversations can be exported as:

- TXT
- JSON

### 🛡️ Validation & Error Handling

DHRIVA includes validation and error handling for:

- Empty messages
- Excessively long messages
- Invalid login credentials
- Duplicate email registration
- Password mismatch
- Short passwords
- Invalid or unreadable PDFs
- PDFs with no extractable text
- AI/API failures

### 🎨 User Interface

- Custom dark-themed interface
- DHRIVA branding
- Custom Streamlit sidebar styling
- Sidebar open/close control
- Responsive layout
- Mobile-friendly styling
- Clean chat interface
- User account section
- Document upload area

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Streamlit | Web application framework |
| Groq API | AI response generation |
| SQLite | User authentication database |
| PBKDF2-HMAC SHA-256 | Password hashing |
| pypdf | PDF text extraction |
| pdf2image | PDF page conversion |
| Tesseract OCR | OCR for scanned PDFs |
| Pillow | Image processing |
| python-dotenv | Environment variable management |
| CSS | Custom user interface styling |

---

## 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │        USER         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     Streamlit UI    │
                         │       app.py        │
                         └──────────┬──────────┘
                                    │
                  ┌─────────────────┼─────────────────┐
                  │                 │                 │
                  ▼                 ▼                 ▼
           Authentication     Chat Management    PDF Processing
                  │                 │                 │
                  ▼                 ▼                 ▼
              SQLite DB        Chat Storage       pypdf / OCR
                  │                 │                 │
                  └─────────────────┼─────────────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      Groq API       │
                         │   AI Model Response │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Streaming Reply   │
                         │     to the User     │
                         └─────────────────────┘
```

---

## 📁 Project Structure

```text
My_ChatBot/
│
├── app.py
│
├── backend/
│   ├── chat_manager.py
│   ├── groq_client.py
│   └── prompts.py
│
├── frontend/
│   └── style.css
│
├── utils/
│   ├── auth.py
│   └── storage.py
│
├── assets/
│   └── bot-message-square.svg
│
├── data/
│   ├── chats/
│   └── users.db
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

> `data/chats/`, `data/users.db`, and `.env` are local files and should not be committed to the repository.

---

## 🔄 Application Flow

### 1. Authentication

```text
User
 │
 ├── Login
 │     └── Verify credentials
 │
 └── Sign Up
       ├── Validate input
       ├── Hash password
       └── Store user in SQLite
```

After successful authentication, the user enters the main DHRIVA interface.

---

### 2. Chat Flow

```text
User Message
      │
      ▼
Input Validation
      │
      ▼
Conversation History
      │
      ▼
Groq API
      │
      ▼
Streaming Response
      │
      ▼
Save Conversation
      │
      ▼
Display Response
```

---

### 3. Document Q&A Flow

```text
Upload PDF
    │
    ▼
Try pypdf Extraction
    │
    ├── Text Found ──────────────┐
    │                            │
    └── No Text                  │
          │                      │
          ▼                      │
      OCR Fallback               │
      pdf2image                  │
          │                      │
      Tesseract OCR              │
          │                      │
          └──────────┬───────────┘
                     ▼
              Extracted Text
                     │
                     ▼
              Document Context
                     │
                     ▼
                  Groq API
                     │
                     ▼
              Document Answer
```

---

## 🔐 Security

DHRIVA does not store passwords as plain text.

During registration:

```text
Password
   │
   ▼
Generate unique salt
   │
   ▼
PBKDF2-HMAC SHA-256
   │
   ▼
Salt + Password Hash
   │
   ▼
SQLite
```

During login, the entered password is hashed using the stored salt and compared with the stored hash.

### Environment Variables

API credentials are stored using environment variables.

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

**Never commit your actual `.env` file or API key to GitHub.**

---

## ⚙️ Installation

### Prerequisites

Make sure you have:

- Python 3.10+
- Git
- Tesseract OCR
- Poppler
- A Groq API key

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/DHRIVA-AI-Assistant.git
cd DHRIVA-AI-Assistant
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open locally through the Streamlit development server.

---

## 📄 PDF & OCR

For scanned PDF support, DHRIVA uses:

- `pdf2image`
- `pytesseract`
- Tesseract OCR
- Poppler

Text-based PDFs are processed using `pypdf`.

If normal PDF extraction does not return text, DHRIVA automatically falls back to OCR.

---

## 🧪 Input Validation

DHRIVA validates user messages before sending them to the AI service.

```text
Trim whitespace
      │
      ▼
Check empty message
      │
      ▼
Check character limit
      │
      ▼
Send to AI
```

Messages longer than **5000 characters** are rejected.

---

## 💾 Data Storage

DHRIVA uses local storage for application data.

### User Database

```text
data/users.db
```

Stores registered user information.

### Chat History

```text
data/chats/
```

Stores conversations separately for each authenticated user.

---

## 📤 Export

Users can export their current conversation as:

### TXT

A readable text transcript containing:

```text
USER:
...

ASSISTANT:
...
```

### JSON

The conversation is exported as structured JSON containing message roles and content.

---

## 🎨 User Interface

DHRIVA uses a custom dark-themed interface designed with CSS.

The interface includes:

- DHRIVA branding
- Custom sidebar
- Sidebar open/close control
- Chat history
- Document upload
- Chat search
- Rename and delete controls
- Export controls
- Account section
- Logout
- Responsive mobile layout

---

## 🧩 Key Components

### `app.py`

Main Streamlit application responsible for:

- Application initialization
- Authentication flow
- UI rendering
- PDF processing
- Chat interaction
- Export functionality

### `backend/groq_client.py`

Handles communication with the Groq API and streams AI responses.

### `backend/chat_manager.py`

Manages:

- Current conversation
- Chat creation
- Message handling
- Saving conversations
- Loading conversations
- Renaming chats
- Deleting chats

### `backend/prompts.py`

Contains the system prompt and DHRIVA's assistant behavior.

### `utils/auth.py`

Handles:

- Database initialization
- Password hashing
- Password verification
- User registration
- User authentication

### `utils/storage.py`

Handles persistent storage of user conversations.

### `frontend/style.css`

Contains the custom DHRIVA interface styling and responsive design.

---

## 🚧 Future Improvements

Possible future enhancements include:

- 🎙️ Voice-based conversations
- 🧠 Improved conversation memory
- 📚 Support for additional document formats
- 🔍 Semantic document search
- 📊 Document summarization
- 🌐 Production deployment
- ☁️ Cloud database integration
- 👤 Profile management
- 🔗 Conversation sharing
- 🤖 Multiple AI model selection

---

## 🎯 What This Project Demonstrates

DHRIVA demonstrates practical experience with:

- Generative AI applications
- Groq API integration
- Prompt engineering
- Streaming AI responses
- Authentication systems
- Password security
- SQLite database management
- Persistent application state
- PDF processing
- OCR pipelines
- File handling
- Error handling
- Input validation
- Responsive UI development
- Modular Python architecture
- Git/GitHub project management

---

## 👩‍💻 Author

### Dhruvanthi K R

AI and Python project focused on building practical applications with generative AI, document processing, authentication, persistent storage, and modern web interfaces.

---

## ⭐ Project

If you find this project useful, consider giving the repository a ⭐ on GitHub.
