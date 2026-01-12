from typing import List

def build_prompt(question: str, contexts: List[str]) -> str:
    context_block = "\n\n".join(
        f"[Context {i+1}]\n{ctx}" for i, ctx in enumerate(contexts)
    )

    return f"""
You are an assistant answering questions strictly using the provided context.

Rules:
- Use only the context below.
- If the answer is not in the context, say "I don't know based on the provided document."
- Do not use prior knowledge.

Context:
{context_block}

Question:
{question}

Answer:
""".strip()
