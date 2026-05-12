from typing import List

from langchain_core.documents import Document


def generate_grounded_answer(question: str, documents: List[Document]) -> tuple[str, bool]:
    """
    Simple extractive answer generator.

    For this portfolio project, the API returns a grounded answer based only on
    retrieved source chunks. This avoids hallucinated responses and keeps the
    project deterministic for CI testing.
    """

    if not documents:
        return (
            "I could not find enough information in the knowledge base to answer that question.",
            False,
        )

    context = " ".join(document.page_content for document in documents)

    answer = (
        f"Based on the retrieved knowledge base content: {context[:900]}"
    )

    if len(context) > 900:
        answer += "..."

    return answer, True