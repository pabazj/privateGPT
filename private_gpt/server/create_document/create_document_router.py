from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from private_gpt.server.chat.chat_service import ChatService
from llama_index.llms import ChatMessage, ChatResponse, MessageRole

create_document_router = APIRouter(prefix="/v1")


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


def process_prompts(service: ChatService, prompts: list[str]) -> dict:

    #Process a list of prompts and get responses for each prompt.
    
    prompt_responses = {}

    for idx, prompt in enumerate(prompts):
        all_messages = [ChatMessage(content=prompt, role=MessageRole.USER)]
        response = get_chat_responses(service, all_messages)
        prompt_responses[f"Prompt_{idx + 1}"] = response

    return prompt_responses


@create_document_router.post("/prompt-responses", response_model=list[dict])
async def get_prompt_responses(request: Request) -> JSONResponse:
    prompts = [
        """
        Write a technical, paragraph OF MAXIMUM 350 WORD that
        1. introduces the objective of the project the team worked on. Why they worked on it. What were they trying to achieve.
        2. What were the standard process((es) or technology that is currently used to achieve the same result and why were these standard technologies insufficient.
        3. End your paragraph with a statement in the format of: In order to develop a (state the objective of the system that they were trying to develop), we encountered the following technological uncertainties:
        Now list in short bullet points the uncertainties that they encountered and one or two sentences about why the uncertainties exist and the difficulties they present towards achieving the objective or relevant sections of the objective of the project. Start each uncertainty statement with: We were uncertain whether we could develop a system that does (mention what the system is supposed to do with respect to this particular uncertainty and the goal of the project). Write a sentence about what the standard technology/technologies is to address this uncertainty and why it is insufficient.
        Keep the tone academic, technical and report writing format, highlighting the core technology. Use the first person voice and assume you are the team.
        """,
        """
        write an account of the work done, use an academic tone with MAXIMUM 700 WORDs, with a focus on highlighting the technology
        break the work done down into a minimal number of paragraphs, where each paragraph demonstrates this cycle of work: hypotheses -> experimentation -> result
        """,
        """ 
        The team achieved the following technological advancements:
        The team gained new knowledge around the development of <paraphrase of the first TU sentence>. To this end, they learned that <paraphrase of the primary accomplishment(s) that map(s) to the TU’s hypothesis>. These technological advancements made it possible to <succinctly describe what the primary TA was>. Therefore, their hypothesis was proven (in)correct and the technological uncertainty was/remains (un)solved. Prior to the work performed by the team within the year, the standard practice was to <paraphrase standard practice sentence of the TU>.
        """,
    ]

    try:
        service = request.state.injector.get(ChatService)
        prompt_responses = process_prompts(service, prompts)
        return JSONResponse(content=prompt_responses)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
