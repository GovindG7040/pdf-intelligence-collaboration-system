# PDF Intelligence & Collaboration System

An AI-powered PDF intelligence and collaboration platform that allows users to upload PDFs, automatically generate summaries, ask questions about documents, and collaborate through shareable links and comments.

## 🚀 Live Demo

Frontend: https://pdf-intelligence-collaboration-frontend.onrender.com

Backend API: https://pdf-intelligence-collaboration-system-88gx.onrender.com

## ✨ Features

### Authentication
- User signup and login
- Password hashing using bcrypt
- JWT-based authentication
- Protected document APIs

### PDF Intelligence
- Authenticated PDF upload
- PDF file validation
- 20 MB upload limit
- Automatic AI-generated document summaries
- Dashboard with uploaded documents
- Filename-based document search

### AI PDF Chat
- Ask questions about uploaded PDFs
- Retrieval-Augmented Generation (RAG)
- Semantic document retrieval using Gemini embeddings
- Conversation history for follow-up questions
- Source page references in AI responses
- Works for both authenticated users and shared guests

### Collaboration
- Generate unique shareable links for documents
- Guests can access shared documents without creating an account
- Guests can add comments
- Document owners can collaborate through comments and AI chat

### Security
- Passwords stored using bcrypt hashing
- JWT authentication
- Owner-based document access control
- Unauthorized users cannot access private documents
- Secrets stored using environment variables

## 🏗️ Architecture

```text
React + Vite Frontend
        |
        | REST API
        v
FastAPI Backend
        |
        +------------------+
        |                  |
        v                  v
   SQLite Database      ChromaDB
        |                  |
        |                  |
        v                  v
 Users / Documents     PDF Embeddings
 Shares / Comments
                           |
                           v
                    Gemini Embeddings
                           |
                           v
                    RAG Retrieval
                           |
                           v
                      Gemini LLM