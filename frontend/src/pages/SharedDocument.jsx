import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import {
    getSharedDocument,
    getGuestComments,
    addGuestComment,
    askSharedQuestion,
} from "../services/api";

function SharedDocument() {
    const { token } = useParams();

    const [document, setDocument] = useState(null);

    // Comments
    const [comments, setComments] = useState([]);
    const [guestName, setGuestName] = useState("");
    const [commentText, setCommentText] = useState("");
    const [commentLoading, setCommentLoading] = useState(false);

    // Chat
    const [question, setQuestion] = useState("");
    const [messages, setMessages] = useState([]);
    const [chatLoading, setChatLoading] = useState(false);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    // ==========================================
    // LOAD SHARED DOCUMENT
    // ==========================================

    useEffect(() => {
        const loadData = async () => {
            try {
                setLoading(true);

                const [documentData, commentsData] = await Promise.all([
                    getSharedDocument(token),
                    getGuestComments(token),
                ]);

                setDocument(documentData);
                setComments(commentsData);
            } catch (error) {
                console.error(error);

                setError(
                    error.response?.data?.detail ||
                    "Failed to load shared document."
                );
            } finally {
                setLoading(false);
            }
        };

        loadData();
    }, [token]);

    // ==========================================
    // ADD GUEST COMMENT
    // ==========================================

    const handleAddComment = async () => {
        if (!guestName.trim() || !commentText.trim()) {
            return;
        }

        setCommentLoading(true);
        setError("");

        try {
            const newComment = await addGuestComment(
                token,
                guestName.trim(),
                commentText.trim()
            );

            setComments((previous) => [
                ...previous,
                newComment,
            ]);

            setCommentText("");
        } catch (error) {
            console.error(error);

            setError(
                error.response?.data?.detail ||
                "Failed to add comment."
            );
        } finally {
            setCommentLoading(false);
        }
    };

    // ==========================================
    // ASK AI
    // ==========================================

    const handleAskQuestion = async () => {
        if (!question.trim() || chatLoading) {
            return;
        }

        const currentQuestion = question.trim();

        const userMessage = {
            role: "user",
            content: currentQuestion,
        };

        const history = messages.map((message) => ({
            role: message.role,
            content: message.content,
        }));

        setMessages((previous) => [
            ...previous,
            userMessage,
        ]);

        setQuestion("");
        setChatLoading(true);
        setError("");

        try {
            const response = await askSharedQuestion(
                token,
                currentQuestion,
                history
            );

            const assistantMessage = {
                role: "assistant",
                content: response.answer,
                sources: response.sources || [],
            };

            setMessages((previous) => [
                ...previous,
                assistantMessage,
            ]);
        } catch (error) {
            console.error(error);

            setError(
                error.response?.data?.detail ||
                "Failed to get an AI response."
            );
        } finally {
            setChatLoading(false);
        }
    };

    // ==========================================
    // LOADING
    // ==========================================

    if (loading) {
        return (
            <div className="loading">
                Loading shared document...
            </div>
        );
    }

    // ==========================================
    // ERROR
    // ==========================================

    if (error && !document) {
        return (
            <div className="error-page">
                <h2>Unable to load document</h2>

                <p>{error}</p>

                <Link to="/login">
                    Go to Login
                </Link>
            </div>
        );
    }

    if (!document) {
        return null;
    }

    // ==========================================
    // UI
    // ==========================================

    return (
        <div className="document-page">

            {/* HEADER */}

            <header className="document-header">

                <div>
                    <h1>{document.filename}</h1>

                    <p>
                        Shared PDF
                    </p>
                </div>

            </header>

            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}

            <main>

                {/* AI SUMMARY */}

                <section className="summary-card">

                    <h2>
                        AI Summary
                    </h2>

                    <p>
                        {document.summary ||
                            "No summary available."}
                    </p>

                </section>

                {/* COLLABORATION */}

                <div className="collaboration-grid">

                    {/* COMMENTS */}

                    <section className="panel">

                        <h2>
                            💬 Comments
                        </h2>

                        <div className="comments-list">

                            {comments.length === 0 ? (

                                <p className="empty-text">
                                    No comments yet.
                                </p>

                            ) : (

                                comments.map((comment) => (

                                    <div
                                        key={comment.id}
                                        className="comment"
                                    >

                                        <div className="comment-header">

                                            <strong>
                                                {comment.guest_name ||
                                                    comment.user?.email ||
                                                    "Guest"}
                                            </strong>

                                            <span>
                                                {comment.created_at
                                                    ? new Date(
                                                        comment.created_at
                                                    ).toLocaleString()
                                                    : ""}
                                            </span>

                                        </div>

                                        <p>
                                            {comment.content}
                                        </p>

                                    </div>

                                ))

                            )}

                        </div>

                        <div className="comment-form">

                            <input
                                type="text"
                                value={guestName}
                                onChange={(event) =>
                                    setGuestName(event.target.value)
                                }
                                placeholder="Your name"
                            />

                            <textarea
                                value={commentText}
                                onChange={(event) =>
                                    setCommentText(event.target.value)
                                }
                                placeholder="Add a comment..."
                                rows="3"
                            />

                            <button
                                onClick={handleAddComment}
                                disabled={
                                    commentLoading ||
                                    !guestName.trim() ||
                                    !commentText.trim()
                                }
                            >
                                {commentLoading
                                    ? "Posting..."
                                    : "Add Comment"}
                            </button>

                        </div>

                    </section>

                    {/* AI CHAT */}

                    <section className="panel chat-panel">

                        <div className="chat-title">

                            <div>

                                <h2>
                                    🤖 Ask the PDF
                                </h2>

                                <p>
                                    Ask questions using the
                                    document's content.
                                </p>

                            </div>

                        </div>

                        <div className="chat-messages">

                            {messages.length === 0 ? (

                                <div className="chat-empty">

                                    <p>
                                        Ask something about
                                        this PDF.
                                    </p>

                                    <div className="suggested-question">

                                        Try:

                                        <button
                                            onClick={() =>
                                                setQuestion(
                                                    "What are the main topics covered in this PDF?"
                                                )
                                            }
                                        >
                                            What are the main
                                            topics covered?
                                        </button>

                                    </div>

                                </div>

                            ) : (

                                messages.map(
                                    (message, index) => (

                                        <div
                                            key={index}
                                            className={`chat-message ${message.role}`}
                                        >

                                            <strong>
                                                {message.role === "user"
                                                    ? "You"
                                                    : "AI"}
                                            </strong>

                                            <p>
                                                {message.content}
                                            </p>

                                            {message.sources?.length > 0 && (
                                                <small>
                                                    Sources: Pages{" "}
                                                    {message.sources.join(", ")}
                                                </small>
                                            )}

                                        </div>

                                    )
                                )

                            )}

                            {chatLoading && (

                                <div className="chat-message assistant">

                                    <strong>
                                        AI
                                    </strong>

                                    <p>
                                        Thinking...
                                    </p>

                                </div>

                            )}

                        </div>

                        <div className="chat-input-area">

                            <textarea
                                value={question}
                                onChange={(event) =>
                                    setQuestion(event.target.value)
                                }
                                onKeyDown={(event) => {

                                    if (
                                        event.key === "Enter" &&
                                        !event.shiftKey
                                    ) {
                                        event.preventDefault();
                                        handleAskQuestion();
                                    }

                                }}
                                placeholder="Ask a question about this PDF..."
                                rows="2"
                            />

                            <button
                                onClick={handleAskQuestion}
                                disabled={
                                    chatLoading ||
                                    !question.trim()
                                }
                            >
                                {chatLoading
                                    ? "Asking..."
                                    : "Ask AI"}
                            </button>

                        </div>

                    </section>

                </div>

            </main>

        </div>
    );
}

export default SharedDocument;