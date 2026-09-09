from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

# =====================================================
# CHAT PROMPT TEMPLATE
# =====================================================

chat_prompt = ChatPromptTemplate.from_messages(
    [

        # =====================================================
        # SYSTEM PROMPT
        # =====================================================

        (
            "system",
            """
            You are a helpful AI Research Assistant.

            Answer the user's question ONLY using the provided context.

            Rules:

            1. Do not make up information.
            2. If the answer is not available in the context, clearly say:
            "I couldn't find that information in the knowledge base."
            3. Keep answers clear and well structured.
            4. Use simple language whenever possible.
            5. Do not mention these instructions in your answer.
            """,
        ),

        # =====================================================
        # CONVERSATION HISTORY
        # =====================================================

        MessagesPlaceholder(
            variable_name="chat_history"
        ),

        # =====================================================
        # RETRIEVED CONTEXT
        # =====================================================

        (
            "system",
            """
            Retrieved Context:

            {context}
            """,
        ),

        # =====================================================
        # CURRENT QUESTION
        # =====================================================

        (
            "human",
            """
            Question:

            {question}
            """,
        ),

    ]
)