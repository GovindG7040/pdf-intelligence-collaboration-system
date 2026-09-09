import { useEffect, useState } from "react";
import {
    Link,
    useNavigate,
    useParams,
} from "react-router-dom";

import {
    getDocument,
    getComments,
    addComment,
    createShareLink,
    askDocumentQuestion,
} from "../services/api";

function Document() {

    const { documentId } = useParams();
    const navigate = useNavigate();

    const [document, setDocument] = useState(null);

    // Comments
    const [comments, setComments] = useState([]);
    const [commentText, setCommentText] = useState("");
    const [commentLoading, setCommentLoading] = useState(false);

    // Sharing
    const [invitedEmail, setInvitedEmail] = useState("");
    const [shareLink, setShareLink] = useState("");
    const [shareLoading, setShareLoading] = useState(false);

    // Chat
    const [question, setQuestion] = useState("");
    const [messages, setMessages] = useState([]);
    const [chatLoading, setChatLoading] = useState(false);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    // ==========================================
    // LOAD DOCUMENT
    // ==========================================

    useEffect(() => {

        const loadData = async () => {

            try {

                setLoading(true);

                const [
                    documentData,
                    commentsData,
                ] = await Promise.all([
                    getDocument(documentId),
                    getComments(documentId),
                ]);

                setDocument(documentData);
                setComments(commentsData);

            } catch (error) {

                console.error(error);

                if (error.response?.status === 401) {

                    localStorage.removeItem("token");

                    navigate("/login");

                    return;

                }

                setError(
                    error.response?.data?.detail ||
                    "Failed to load document."
                );

            } finally {

                setLoading(false);

            }
        };

        loadData();

    }, [documentId, navigate]);

    // ==========================================
    // ADD COMMENT
    // ==========================================

    const handleAddComment = async () => {

        if (!commentText.trim()) {
            return;
        }

        setCommentLoading(true);

        try {

            const newComment = await addComment(
                documentId,
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
    // CREATE SHARE LINK
    // ==========================================

    const handleCreateShare = async () => {

        setShareLoading(true);
        setError("");

        try {

            const data = await createShareLink(
                documentId,
                invitedEmail
            );

            setShareLink(
                data.share_url ||
                data.url ||
                ""
            );

        } catch (error) {

            console.error(error);

            setError(
                error.response?.data?.detail ||
                "Failed to create share link."
            );

        } finally {

            setShareLoading(false);

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

            const response = await askDocumentQuestion(
                documentId,
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
                Loading document...
            </div>
        );

    }

    // ==========================================
    // ERROR
    // ==========================================

    if (error && !document) {

        return (

            <div className="error-page">

                <h2>
                    Unable to load document
                </h2>

                <p>
                    {error}
                </p>

                <Link to="/dashboard">
                    Back to Dashboard
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

            {/* ======================================
                HEADER
            ====================================== */}

            <header className="document-header">

                <Link to="/dashboard">
                    ← Dashboard
                </Link>

                <div>

                    <h1>
                        {document.filename}
                    </h1>

                    <p>
                        {document.created_at
                            ? new Date(
                                document.created_at
                            ).toLocaleString()
                            : ""}
                    </p>

                </div>

            </header>

            {error && (

                <div className="error-message">
                    {error}
                </div>

            )}

            <main>

                {/* ==================================
                    AI SUMMARY
                ================================== */}

                <section className="summary-card">

                    <h2>
                        AI Summary
                    </h2>

                    <p>
                        {document.summary ||
                            "No summary available."}
                    </p>

                </section>

                {/* ==================================
                    COLLABORATION AREA
                ================================== */}

                <div className="collaboration-grid">

                    {/* =================================
                        COMMENTS
                    ================================= */}

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
                                                    "User"}
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

                            <textarea
                                value={commentText}
                                onChange={(event) =>
                                    setCommentText(
                                        event.target.value
                                    )
                                }
                                placeholder="Add a comment..."
                                rows="3"
                            />

                            <button
                                onClick={handleAddComment}
                                disabled={
                                    commentLoading ||
                                    !commentText.trim()
                                }
                            >
                                {commentLoading
                                    ? "Posting..."
                                    : "Add Comment"}
                            </button>

                        </div>

                    </section>

                    {/* =================================
                        AI CHAT
                    ================================= */}

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
                                            className={`chat-message ${
                                                message.role
                                            }`}
                                        >

                                            <strong>
                                                {message.role ===
                                                "user"
                                                    ? "You"
                                                    : "AI"}
                                            </strong>

                                            <p>
                                                {message.content}
                                            </p>

                                            {message.sources
                                                ?.length > 0 && (

                                                <small>
                                                    Sources:
                                                    {" "}
                                                    Pages{" "}
                                                    {message.sources.join(
                                                        ", "
                                                    )}
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
                                    setQuestion(
                                        event.target.value
                                    )
                                }
                                onKeyDown={(event) => {

                                    if (
                                        event.key ===
                                            "Enter" &&
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

                {/* ==================================
                    SHARING
                ================================== */}

                <section className="panel share-panel">

                    <h2>
                        🔗 Share this PDF
                    </h2>

                    <p>
                        Create a unique link that lets
                        others view and collaborate on this
                        document without signing in.
                    </p>

                    <div className="share-form">

                        <input
                            type="email"
                            value={invitedEmail}
                            onChange={(event) =>
                                setInvitedEmail(
                                    event.target.value
                                )
                            }
                            placeholder="Invited email (optional)"
                        />

                        <button
                            onClick={handleCreateShare}
                            disabled={shareLoading}
                        >
                            {shareLoading
                                ? "Creating..."
                                : "Create Share Link"}
                        </button>

                    </div>

                    {shareLink && (

                        <div className="share-result">

                            <p>
                                Share this link:
                            </p>

                            <input
                                type="text"
                                value={shareLink}
                                readOnly
                                onFocus={(event) =>
                                    event.target.select()
                                }
                            />

                            <button
                                onClick={() =>
                                    navigator.clipboard.writeText(
                                        shareLink
                                    )
                                }
                            >
                                Copy Link
                            </button>

                        </div>

                    )}

                </section>

            </main>

        </div>

    );
}

export default Document;