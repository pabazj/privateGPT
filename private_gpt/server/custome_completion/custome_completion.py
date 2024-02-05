from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import BaseModel
from starlette.responses import StreamingResponse, JSONResponse
from private_gpt.open_ai.openai_models import OpenAICompletion, OpenAIMessage
from private_gpt.open_ai.extensions.context_filter import ContextFilter
from private_gpt.server.chat.chat_router import ChatBody, chat_completion
from private_gpt.server.utils.auth import authenticated
from private_gpt.prompts import PROMPTS
import logging

custome_completions_router = APIRouter(prefix="/v1")
logger = logging.getLogger(__name__)

class CustomeCompletionsBody(BaseModel):
    input: str
    section: str
    system_prompt: str | None = None
    use_context: bool = False
    context_filter: ContextFilter | None = None
    include_sources: bool = False
    stream: bool = False

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "input": "How do you fry an egg?",
                    "section": "objectives",
                    "system_prompt": "You are a rapper. Always answer with a rap.",
                    "stream": False,
                    "use_context": False,
                    "include_sources": False,
                }
            ]
        }
    }

@custome_completions_router.post(
    "/custom/completions",
    response_model=None,
    summary="Completion",
    responses={200: {"model": OpenAICompletion}},
    tags=["Contextual Completions"],
)
def prompt_completion(
    request: Request, body: CustomeCompletionsBody
) -> OpenAICompletion | StreamingResponse:
    """Generate completion based on the provided section and input."""
    section = body.section
    input_text = body.input

    # Find the relevant prompt based on the section
    relevant_prompt = next(
        (prompt["prompt"] for prompt in PROMPTS if prompt["section"] == section),
        None
    )

    if not relevant_prompt:
        # Handle the case when no relevant prompt is found for the given section
        return JSONResponse(
            status_code=400,
            content={"detail": "No prompt found for the specified section."},
        )
    # logger.info("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$=%s", relevant_prompt)
    # Construct the prompt by combining the input and the relevant prompt
    prompt = f"{input_text}\n{relevant_prompt}"

    # Use the modified prompt to generate a response
    messages = [OpenAIMessage(content=prompt, role="user")]
    chat_body = ChatBody(
        messages=messages,
        use_context=body.use_context,
        stream=body.stream,
        include_sources=body.include_sources,
        context_filter=body.context_filter,
    )

    return chat_completion(request, chat_body)