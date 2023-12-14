from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from private_gpt.server.chat.chat_service import ChatService
from llama_index.llms import ChatMessage, ChatResponse, MessageRole
import itertools
from private_gpt.prompts import PROMPTS

create_document_router = APIRouter(prefix="/v1")
SOURCES_SEPARATOR = "\n\n Sources: \n"

def get_chat_responses(service: ChatService, messages: list[ChatMessage]) -> str:

    #get chat responses from the chat service.

    full_response = ""
    query_stream = service.stream_chat(messages=messages, use_context=True)

    for delta in query_stream.response:
        if isinstance(delta, str):
            full_response += str(delta)
        elif isinstance(delta, ChatResponse):
            full_response += delta.delta or ""

    return full_response

def process_prompts_with_history(service: ChatService, prompts: list[dict], history: list[list[str]]) -> list[dict]:
    # Process a list of prompts and get responses for each prompt, considering the history.
    prompt_responses = []
    history_messages = build_history(history)

    for prompt_info in prompts:
        section_number = prompt_info["section"]
        prompt = prompt_info["prompt"]
        all_messages = history_messages + [ChatMessage(content=prompt, role=MessageRole.USER)]
        response = get_chat_responses(service, all_messages)
        prompt_responses.append({"sec": section_number, "prompt": prompt, "response": response})

    return prompt_responses


def build_history(history: list[list[str]]) -> list[ChatMessage]:
    # Build a history of messages based on the provided history list.
    history_messages: list[ChatMessage] = list(
        itertools.chain(
            *[
                [
                    ChatMessage(content=interaction[0], role=MessageRole.USER),
                    ChatMessage(
                        # Remove from history content the Sources information
                        content=interaction[1].split(SOURCES_SEPARATOR)[0],
                        role=MessageRole.ASSISTANT,
                    ),
                ]
                for interaction in history
            ]
        )
    )

    # Max 20 messages to try to avoid context overflow
    return history_messages[:20]


@create_document_router.post("/prompt-responses", response_model=list[dict])
async def get_prompt_responses(request: Request) -> JSONResponse:

    history = [
    ]

    try:
        service = request.state.injector.get(ChatService)
        prompt_responses = process_prompts_with_history(service, PROMPTS, history)
        return JSONResponse(content=prompt_responses)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
