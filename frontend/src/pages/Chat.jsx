import { useState } from "react";

import Header from "../components/Header";
import MessageList from "../components/MessageList";
import ChatInput from "../components/ChatInput";

import { askQuestion } from "../services/api";

import "../styles/chat.css";

function Chat() {

    // ==========================================
    // STATE
    // ==========================================

    const [question, setQuestion] = useState("");

    const [messages, setMessages] = useState([]);

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");

    // ==========================================
    // ASK QUESTION
    // ==========================================

    const handleAsk = async () => {

        if (!question.trim()) {

            return;

        }

        setLoading(true);

        setError("");

        // --------------------------------------
        // User Message
        // --------------------------------------

        const userMessage = {

            role: "user",

            content: question,

        };

        // --------------------------------------
        // Temporary Assistant Message
        // --------------------------------------

        const thinkingMessage = {

            role: "assistant",

            content: "Thinking...",

            sources: [],

        };

        setMessages((previousMessages) => [

            ...previousMessages,

            userMessage,

            thinkingMessage,

        ]);

        try {

            const response = await askQuestion(question);

            const assistantMessage = {

                role: "assistant",

                content: response.answer,

                sources: response.sources,

            };

            setMessages((previousMessages) => {

                const updatedMessages = [...previousMessages];

                updatedMessages[updatedMessages.length - 1] = assistantMessage;

                return updatedMessages;

            });

            setQuestion("");

        }

        catch (error) {

            console.error(error);

            setError(

                error.response?.data?.detail ||

                "Something went wrong."

            );

        }

        finally {

            setLoading(false);

        }

    };

    // ==========================================
    // UI
    // ==========================================

    return (

        <div className="app-container">

            <Header />

            {

                error && (

                    <div className="error-message">

                        {error}

                    </div>

                )

            }

            <MessageList

                messages={messages}

            />

            <ChatInput

                question={question}

                setQuestion={setQuestion}

                loading={loading}

                handleAsk={handleAsk}

            />

        </div>

    );

}

export default Chat;