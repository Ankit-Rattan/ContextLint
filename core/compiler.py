from typing import List
from core.parser import parse_source_file
from core.tokenizer import count_tokens

# This is your "Secret Sauce" — the system instructions that force the LLM
# to turn trash inputs into high-performing, structured prompts.
META_PROMPT = """You are an expert Prompt Engineer and Systems Architect. 
Your task is to take a vague, unoptimized user prompt along with its accompanying file context, and compile it into a highly optimized, fully structured prompt template.

The output MUST be written in clean, professional Markdown syntax. 

Follow this exact structural layout for the output:
1. # OBJECTIVE: A clear, single-sentence summary of what the prompt is trying to achieve.
2. ## CONTEXT: High-level background derived from the provided source files.
3. ## SOURCE FILES: If files were provided, list them here using structural blocks or markdown code fences so the target LLM understands the codebase layout.
4. ## INSTRUCTIONS & STEPS: A logical, sequential list of instructions for the target LLM to execute.
5. ## CONSTRAINTS & GUARDRAILS: Strict rules, edge cases to avoid, or formatting boundaries.
6. ## EXPECTED OUTPUT FORMAT: Specify exactly what the resulting output should look like (e.g., JSON schema, Markdown, code snippet).

Ensure the resulting prompt uses clear structural tags (like XML tags like <context> or markdown headers) because modern LLMs process structured blocks drastically better than raw walls of text. Do not include conversational filler in your response; output ONLY the compiled markdown prompt.
"""

class PromptCompiler:
    def __init__(self, model_name: str = "gpt-4"):
        self.model_name = model_name

    def compile(self, vague_prompt: str, file_paths: List[str]) -> dict:
        """
        Gathers raw text, strips file bloat, measures token differences,
        and builds the final payload to be passed to the LLM Gateway.
        """
        raw_context_pieces = []
        raw_token_count = count_tokens(vague_prompt, self.model_name)
        
        # 1. Parse files and measure raw token usage
        for path in file_paths:
            # parse_source_file handles removing empty lines and stripping trailing whitespaces
            cleaned_file_content = parse_source_file(path)
            raw_token_count += count_tokens(cleaned_file_content, self.model_name)
            raw_context_pieces.append(cleaned_file_content)
            
        # 2. Combine the gathered context
        combined_context = "\n\n".join(raw_context_pieces)
        
        # 3. Build the payload that will hit the LLM
        user_payload = f"""--- USER VAGUE PROMPT ---
{vague_prompt}

--- PROVIDED CONTEXT FILES ---
{combined_context}
"""
        
        # Calculate final payload tokens (including our meta instructions)
        total_compiled_tokens = (
            count_tokens(META_PROMPT, self.model_name) + 
            count_tokens(user_payload, self.model_name)
        )
        
        return {
            "system_instruction": META_PROMPT,
            "user_payload": user_payload,
            "metrics": {
                "raw_input_tokens": raw_token_count,
                "compiled_payload_tokens": total_compiled_tokens,
                # We can calculate final savings once the LLM returns its response
            }
        }