from langchain_core.chat_history import InMemoryChatMessageHistory

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
)


class MemoryService:
    """
    Manages conversation history for multiple chat sessions.
    """

    def __init__(self):

        # ----------------------------------------
        # Session Memories
        # ----------------------------------------

        self.chat_histories = {}

        print("Conversation memory initialized.")

    # =====================================================
    # GET SESSION MEMORY
    # =====================================================

    def _get_session_history(self, session_id: str,):
        """
        Returns the chat history for a session.
        Creates one if it does not exist.
        """

        if session_id not in self.chat_histories:

            self.chat_histories[session_id] = (
                InMemoryChatMessageHistory()
            )

        return self.chat_histories[session_id]

    # =====================================================
    # ADD USER MESSAGE
    # =====================================================

    def add_user_message(self, session_id: str, message: str,):

        history = self._get_session_history(session_id)

        history.add_message(

            HumanMessage(
                content=message
            )

        )

    # =====================================================
    # ADD AI MESSAGE
    # =====================================================

    def add_ai_message(self, session_id: str, message: str,):

        history = self._get_session_history(session_id)

        history.add_message(

            AIMessage(
                content=message
            )

        )

    # =====================================================
    # GET CHAT HISTORY
    # =====================================================

    def get_history(self, session_id: str,):

        history = self._get_session_history(session_id)

        return history.messages

    # =====================================================
    # CLEAR MEMORY
    # =====================================================

    def clear_memory(self, session_id: str,):

        history = self._get_session_history(session_id)

        history.clear()

        print(f"Conversation cleared for session: {session_id}")