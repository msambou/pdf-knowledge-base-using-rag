# PDF Knowledge Base Q&A using Retrieval-Augmented Generation (RAG)

## What?
This is a classic RAG where users can upload PDF documents and ask questions to the LLM about the content of the PDF. Good for documents pertaining to policies, contracts, etc. where users want quick questions to be answered factually.

## Why?
It's time consuming to have to go through enitre lenghty contract or policy documents just to answer a simple question like, "By doing XYZ, I'm following the compliant rules?". Using RAG with LLM have made it easier to query documents directly in a short period of time.

## How?
I'll use an LLM as the reasoning layer and RAG for document retrieval. I'll not be relying on the LLM's memory. 

Instead of this:
> LLM, Do you know what's in this document?

I'm doing:
> Here are the relevant excerpts from the PDF. Answer using only these.

### Key Idea:
The LLM never reads the whole PDF. It only sees **small retrieved chunks** that I choose.

## Phases
The project has two phases, **Indexing Phase** and **Question Asking Phase**.

### Phase A: Indexing (Building the Knowledge Base)
* This is usually a one-time thing
* This happens when the PDF is uploaded
* 
    ```shell
    PDF -> Text -> Chunks -> Embeddings -> Vector Store
    ```
* PDF is converted into clean text using a tool like PyPDF
* `Chunking` is used to organize large texts into smaller ones. Because retrieval works best on small, focused passages, it's good to chunk them. This is a very important step. Also, embedding models have context limits and so chunking is needed.
* **Embedding**: Each chunk is converted into a vector using an embedding model. Embeddings turn text into numbers. Similar meanings -> closer vectors.

    > “Who is eligible for leave?”
    >
    > will retrieve chunks about eligibility, even if the wording differs.
* Vector Store (FAISS)
    - Facebook AI Similarity Search (FAISS)
    - Stores vectors, Associated metadata (source PDF, page number, chunk ID)
    - FAISS give us fast similarity search which is fully local, no database setup needed


### Phase B: Asking Questions
The user’s question is:

* Embedded using the same embedding model
* Compared against stored vectors

FAISS returns:
* Top-k most relevant chunks (e.g. 3–5)

### Prompt Grounding
Now you assemble a prompt like:

> **System instruction**
>
> You are a helpful assistant.
>
> Answer the question using only the provided context.
>
> If the answer is not in the context, say “I don’t know.”

> **Context**
>
> [Chunk 1]
>
> [Chunk 2]
>
> [Chunk 3]

> **Question**
>
> “What documents are required for reimbursement?”

