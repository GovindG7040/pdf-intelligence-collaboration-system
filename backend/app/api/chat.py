from fastapi import APIRouter, HTTPException

from app.models.chat_models import (
    ChatRequest,
    ChatResponse,
    Source,
)
from app.services.chat_service import ChatService

# =====================================================
# CREATE ROUTER
# =====================================================

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

# =====================================================
# CREATE CHAT SERVICE
# =====================================================

chat_service = ChatService()

# =====================================================
# CHAT ENDPOINT
# =====================================================

@router.post("/", response_model=ChatResponse,)
def chat(request: ChatRequest):         # Define a POST endpoint for the chat service that takes a ChatRequest and returns a ChatResponse. request: ChatRequest is a Pydantic model that validates the incoming request data. The response_model=ChatResponse specifies that the response will be validated against the ChatResponse model.

    try:

        result = chat_service.ask(request.question)

        return ChatResponse(

            answer=result["answer"],

            sources=[Source(file=source["file"]) for source in result["sources"]],

        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )