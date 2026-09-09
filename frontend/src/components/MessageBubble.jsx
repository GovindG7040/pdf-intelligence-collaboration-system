import SourceList from "./SourceList";

function MessageBubble({ message }) {

    // ==========================================
    // CHECK MESSAGE TYPE
    // ==========================================

    const isUser = message.role === "user";

    // ==========================================
    // UI
    // ==========================================

    return (

        <div

            className={

                isUser

                    ? "message-row user"

                    : "message-row assistant"

            }

        >

            <div

                className={

                    isUser

                        ? "message-bubble user-bubble"

                        : "message-bubble assistant-bubble"

                }

            >

                <div className="message-header">

                    <span className="message-avatar">

                        {

                            isUser

                                ? "👤"

                                : "🤖"

                        }

                    </span>

                    <strong>

                        {

                            isUser

                                ? "You"

                                : "Assistant"

                        }

                    </strong>

                </div>

                <p className="message-content">

                    {message.content}

                </p>

                {

                    !isUser && (

                        <SourceList

                            sources={message.sources}

                        />

                    )

                }

            </div>

        </div>

    );

}

export default MessageBubble;