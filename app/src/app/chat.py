import ollama


def invoke_chat():
    response = ollama.chat(
        model="mistral",
        messages=[
            {"role": "user", "content": "Explain RAG in one sentence."}
        ]
    )

    # return (response["message"]["content"])
    return response