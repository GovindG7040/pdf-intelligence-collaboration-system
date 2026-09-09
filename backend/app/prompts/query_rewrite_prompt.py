from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

# =====================================================
# QUERY REWRITE PROMPT
# =====================================================

query_rewrite_prompt = ChatPromptTemplate.from_messages(

    [

        (

            "system",

            """
You are an AI assistant responsible ONLY for rewriting user questions for document retrieval.

Your task is to convert the latest user question into a standalone question when necessary.

IMPORTANT:

- First determine whether the latest question already makes sense by itself.
- If it is already a complete, standalone question, return it EXACTLY as written.
- Only rewrite the question when it contains references such as "it", "they", "them", "this", "that", "he", "she", etc. that depend on the conversation history.

Rules:

1. Preserve the user's exact intent.
2. Resolve ambiguous references using the conversation history.
3. Do NOT answer the question.
4. Do NOT add new information.
5. Do NOT remove information.
6. Do NOT infer missing facts.
7. Return ONLY the rewritten question.
8. If no rewriting is required, copy the question exactly.

Examples:

User Question:
What are Transformers?

Output:
What are Transformers?

----------------------------------------

Conversation:
User: What are Transformers?

User Question:
Who introduced them?

Output:
Who introduced Transformers?

----------------------------------------

Conversation:
User: Explain Machine Learning.

User Question:
What are its applications?

Output:
What are the applications of Machine Learning?
""",

        ),

        MessagesPlaceholder(
            variable_name="chat_history"
        ),

        (

            "human",

            "{question}",

        ),

    ]

)