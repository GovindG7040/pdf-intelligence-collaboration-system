from pydantic import BaseModel, Field


# =====================================================
# REQUEST MODEL
# =====================================================

class ChatRequest(BaseModel):
    """
    Request model for the chat endpoint.
    """

    question: str = Field(
        ...,
        min_length=1,
        description="User question",
        examples=["What is Machine Learning?"],
    )


# =====================================================
# SOURCE MODEL
# =====================================================

class Source(BaseModel):
    """
    Represents a source document used to answer the question.
    """

    file: str


# =====================================================
# RESPONSE MODEL
# =====================================================

class ChatResponse(BaseModel):
    """
    Response model for the chat endpoint.
    """

    answer: str

    sources: list[Source]