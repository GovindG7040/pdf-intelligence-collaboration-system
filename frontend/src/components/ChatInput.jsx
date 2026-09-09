function ChatInput({

    question,

    setQuestion,

    loading,

    handleAsk,

}) {

    // ==========================================
    // HANDLE KEY PRESS
    // ==========================================

    const handleKeyDown = (event) => {

        // Enter → Send

        if (

            event.key === "Enter"

            &&

            !event.shiftKey

        ) {

            event.preventDefault();

            handleAsk();

        }

    };

    // ==========================================
    // UI
    // ==========================================

    return (

        <div className="chat-input-container">

            <textarea

                className="chat-input"

                rows="3"

                placeholder="Ask anything about your knowledge base..."

                value={question}

                onChange={(event) =>

                    setQuestion(event.target.value)

                }

                onKeyDown={handleKeyDown}

            />

            <button

                className="send-button"

                onClick={handleAsk}

                disabled={loading}

            >

                {

                    loading

                        ? "Thinking..."

                        : "Send"

                }

            </button>

        </div>

    );

}

export default ChatInput;