import MessageBubble from "./MessageBubble";

function MessageList({ messages }) {

    // ==========================================
    // UI
    // ==========================================

    return (

        <div className="message-list">

            {

                messages.length === 0 ? (

                    <div className="empty-chat">

                        <h2>

                            Welcome 👋

                        </h2>

                        <p>

                            Ask anything about your knowledge base to begin the conversation.

                        </p>

                    </div>

                ) : (

                    messages.map((message, index) => (

                        <MessageBubble

                            key={index}

                            message={message}

                        />

                    ))

                )

            }

        </div>

    );

}

export default MessageList;