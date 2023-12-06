from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
#from private_gpt.open_ai.openai_models import OpenAICompletion
from private_gpt.open_ai.openai_models import (
    OpenAICompletion,
    OpenAIMessage,
)
from private_gpt.server.completions.completions_router import completions_router, prompt_completion, CompletionsBody
from private_gpt.server.chat.chat_router import chat_router, chat_completion, ChatBody
from private_gpt.server.chat.chat_service import ChatService

from llama_index.llms import ChatMessage, ChatResponse, MessageRole

create_document_router = APIRouter(prefix="/v1")



@create_document_router.post("/prompt-responses", response_model=list[dict])
async def get_prompt_responses(request: Request) -> JSONResponse:
    prompts = [
        "What is the capital of France?",
        "Who wrote Hamlet?",
        "How does photosynthesis work?",
    ]

    service = request.state.injector.get(ChatService)
    all_messages = []
    new_message = ChatMessage(content=prompts[0], role=MessageRole.USER)
    all_messages.append(new_message)

    prompt_responses = []

    query_stream = service.stream_chat(
        messages=all_messages,
        use_context=True,
    )

    full_response: str = ""
    stream = query_stream.response
    for delta in stream:
        if isinstance(delta, str):
            full_response += str(delta)
        elif isinstance(delta, ChatResponse):
            full_response += delta.delta or ""

    prompt_responses = {"Test": full_response}

    # try:
    #     for prompt in prompts:
            # Step 1: Get completion from /completions route
            
            #completions_body = CompletionsBody(prompt=prompt)
            #completion_response = prompt_completion(request=request, body=completions_body)
            

            #prompt_responses.append({"prompt": prompt, "response": chat_response})
            
    # except HTTPException as e:
    #     return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)

    return JSONResponse(content=prompt_responses)
