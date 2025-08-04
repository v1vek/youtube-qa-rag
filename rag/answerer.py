from config import openAiClient, OPENAI_MODEL

def generate_answer(query: str, chunks: list[dict], model=OPENAI_MODEL) -> str:
    """
    Generate an answer to a query based on relevant chunks using OpenAI's API.

    :param query: The search query.
    :param chunks: A list of dictionaries containing relevant text chunks.
    :param model: The OpenAI model to use for generating the answer.
    :return: The generated answer as a string.
    """
    context = "\n\n".join(
        f"[{c['start_time']}-{c['end_time']}]\n{c['content']}" for c in chunks
    )
    
    system_prompt = (
        "You are a helpful assistant answering questions from Youtube videos. "
        "Use the transcript chunks below to answer the question in your own words. Do not quote directly unless necessary. If possible, provide a short explanation or summary using the retrieved content."
    )

    response = openAiClient.chat.completions.create(
        model=model,
        messages=[
            { "role": "system", "content": system_prompt },
            { "role": "user", "content": f"Video transcript context:\n\n{context}" },
            { "role": "user", "content": f"Question: {query}" }
        ],
    )

    content = response.choices[0].message.content if response.choices and response.choices[0].message.content is not None else None
    return content.strip() if content else "No answer generated."