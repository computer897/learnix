"""
Gemini API client for answer generation.

In mock mode, returns a simple concatenation of retrieved context.
In production mode, calls the Google Gemini API with the context.
"""

import os
import logging
from typing import List

logger = logging.getLogger(__name__)

USE_MOCKS = os.getenv("USE_MOCKS", "1") == "1"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


def generate_answer_from_context(question: str, contexts: List[str]) -> str:
    """
    Generate an answer using retrieved context.
    
    Args:
        question: User's question
        contexts: List of relevant text segments from retrieved documents
        
    Returns:
        Generated answer string
    """
    if USE_MOCKS or not GEMINI_API_KEY:
        return _generate_mock_answer(question, contexts)
    else:
        return _generate_gemini_answer(question, contexts)


def _generate_mock_answer(question: str, contexts: List[str]) -> str:
    """
    Generate a simple mock answer by concatenating context.
    
    This is used when running in mock mode without the Gemini API.
    """
    if not contexts or all(not c.strip() for c in contexts):
        return f"🤖 Mock Answer: I couldn't find relevant content to answer: '{question}'\n\nPlease upload some documents first!"
    
    # Take first 3 contexts and limit length
    relevant_contexts = []
    for ctx in contexts[:3]:
        if ctx.strip():
            # Limit each context to ~500 chars
            snippet = ctx[:500] + "..." if len(ctx) > 500 else ctx
            relevant_contexts.append(snippet)
    
    joined = "\n\n---\n\n".join(relevant_contexts)
    
    answer = f"""🤖 Mock Answer for: "{question}"

Based on the uploaded documents, here are the most relevant excerpts:

{joined}

---
💡 Note: This is a mock response. Enable USE_MOCKS=0 and set GEMINI_API_KEY to get AI-generated answers."""
    
    return answer


def _generate_gemini_answer(question: str, contexts: List[str]) -> str:
    """
    Generate an answer using the Google Gemini API.
    
    Args:
        question: User's question
        contexts: List of relevant text segments
        
    Returns:
        AI-generated answer
    """
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=GEMINI_API_KEY)
        # Use gemini-2.5-flash (stable version)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Build prompt with clean context (no metadata)
        # Clean up context to remove any file paths, page numbers, metadata
        cleaned_contexts = []
        for ctx in contexts[:10]:  # Use up to 10 chunks for better coverage
            # Remove common metadata patterns
            lines = ctx.split('\n')
            clean_lines = [
                line for line in lines 
                if not any(pattern in line.lower() for pattern in [
                    'page', 'chapter', 'section', '.pdf', '.docx', 
                    'copyright', 'isbn', 'blind folio', 'compref'
                ])
            ]
            cleaned_contexts.append('\n'.join(clean_lines))
        
        context_text = "\n\n".join(cleaned_contexts)
        
        prompt = f"""You are Learnix — an intelligent AI assistant built for college students.
Your goal is to generate long, exam-ready academic answers that are clear, detailed, and structured in 6–7 paragraphs.

The student asked: "{question}"

Here are relevant excerpts from their study materials:
---
{context_text}
---

Guidelines for generating answers:

1. Write in formal academic English suitable for college exams.

2. Start with a short introduction that defines the topic clearly.

3. Write 6–7 detailed paragraphs explaining every aspect of the topic.

4. Maintain space between each paragraph for readability (a blank line between paragraphs).

5. Cover definitions, explanations, examples, applications, advantages, and importance.

6. Include notes like [Diagram: topic name] when diagrams are relevant.

7. If the topic involves code or algorithms, include a short code block or pseudocode with proper indentation.

8. End with a brief conclusion summarizing the concept's key points.

9. Avoid bullet points, markdown headings (#, *, -), or lists — use only paragraphs.

10. The total answer should be long enough to represent about 5–6 pages (900–1200 words).

STRUCTURE YOUR ANSWER AS FOLLOWS:

Paragraph 1 (Introduction): Define the topic clearly in 4-5 sentences. Provide context and importance.

Paragraph 2 (Core Concept): Explain the fundamental concept in detail. Use 5-6 sentences to cover the basic working and principles.

Paragraph 3 (Key Features/Characteristics): Describe important characteristics, properties, or components. Write 5-6 sentences with detailed explanations.

Paragraph 4 (Implementation/Example): Provide concrete examples, code snippets, or implementation details. Use 6-7 sentences with clear explanations and comments in code.

Paragraph 5 (Advanced Details): Cover variations, types, or advanced aspects. Write 5-6 sentences explaining deeper concepts.

Paragraph 6 (Applications/Advantages): Discuss real-world applications, advantages, or use cases. Use 5-6 sentences with practical examples.

Paragraph 7 (Conclusion): Summarize the key points and reinforce the topic's importance. Write 3-4 sentences as a conclusion.

CRITICAL FORMATTING RULES:
- Add a BLANK LINE between every paragraph
- Write in continuous prose, not bullet points
- Each paragraph should be 4-7 sentences (80-150 words)
- Total answer: 900-1200 words (exam-length answer)
- Use proper academic language
- Include code examples with comments when relevant
- Mention [Diagram: topic name] where diagrams would help

Now generate a comprehensive, exam-ready answer:"""
        
        response = model.generate_content(prompt)
        answer = response.text
        
        logger.info("Generated answer using Gemini API")
        return answer
        
    except ImportError:
        logger.error("google-generativeai not installed. Install it: pip install google-generativeai")
        return "Error: google-generativeai package not installed. Please install it or use mock mode."
    
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}")
        return f"Error generating answer: {str(e)}\n\nPlease check your GEMINI_API_KEY and try again."


def test_gemini_connection() -> bool:
    """
    Test if Gemini API is configured and working.
    
    Returns:
        True if connection successful, False otherwise
    """
    if not GEMINI_API_KEY:
        return False
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Say 'Hello'")
        return bool(response.text)
    except:
        return False
