import os
import google.generativeai as genai
from google.generativeai.types import TokenCountResponse, GenerateContentResponse
from config import Settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Main function to demonstrate LLM cost predictability and optimization.
    It configures the LLM, counts input tokens, makes a generation call,
    and reports token usage and estimated cost.
    """
    logging.info("Starting LLM Cost Predictor Prototype...")

    # Load settings from environment variables or .env file
    settings = Settings()

    # Configure the Generative AI model with the API key
    try:
        genai.configure(api_key=settings.api_key.get_secret_value())
        logging.info("Google Generative AI configured successfully.")
    except ValueError as e:
        logging.error(f"Failed to configure Google Generative AI: {e}")
        logging.error("Please ensure GEMINI_API_KEY is set in your environment or .env file.")
        return

    # Initialize the Generative Model
    try:
        model = genai.GenerativeModel(
            model_name=settings.model_name,
            generation_config={
                "temperature": settings.temperature,
                "max_output_tokens": settings.max_tokens,
            }
        )
        logging.info(f"Initialized model: {settings.model_name} with temp={settings.temperature}, max_output_tokens={settings.max_tokens}")
    except Exception as e:
        logging.error(f"Error initializing generative model: {e}")
        return

    # Define a sample prompt
    sample_prompt = (
        "Draft a short, engaging blog post about the benefits of "
        "sustainable urban farming for community development. "
        "Focus on economic, environmental, and social aspects."
    )
    logging.info(f"\n--- Sample Prompt ---\n{sample_prompt}\n---------------------")

    # --- Step 1: Predict input token cost before API call ---
    try:
        token_count_response: TokenCountResponse = model.count_tokens(sample_prompt)
        predicted_input_tokens = token_count_response.total_tokens
        logging.info(f"Predicted input tokens (pre-API call): {predicted_input_tokens}")
    except Exception as e:
        logging.warning(f"Could not predict input tokens: {e}")
        predicted_input_tokens = 0

    # --- Step 2: Make the actual LLM call ---
    try:
        response: GenerateContentResponse = model.generate_content(sample_prompt)
        logging.info("LLM generation successful.")

        # --- Step 3: Extract actual token usage ---
        if response.usage_metadata:
            actual_prompt_tokens = response.usage_metadata.prompt_token_count
            actual_candidate_tokens = response.usage_metadata.candidates_token_count
            total_tokens_used = response.usage_metadata.total_token_count
        else:
            actual_prompt_tokens = predicted_input_tokens # Fallback if usage_metadata is missing
            actual_candidate_tokens = len(response.text.split()) # Very rough estimate
            total_tokens_used = actual_prompt_tokens + actual_candidate_tokens
            logging.warning("Usage metadata not available. Using estimated token counts.")

        logging.info(f"\n--- Token Usage Report ---")
        logging.info(f"Actual Input Tokens (Prompt): {actual_prompt_tokens}")
        logging.info(f"Actual Output Tokens (Candidates): {actual_candidate_tokens}")
        logging.info(f"Total Tokens Used: {total_tokens_used}")

        # --- Step 4: Estimate Cost ---
        estimated_cost = total_tokens_used * settings.cost_per_token
        logging.info(f"Estimated Cost per Token: ${settings.cost_per_token:.6f}")
        logging.info(f"Estimated Cost for this operation: ${estimated_cost:.6f}")

        logging.info(f"\n--- Generated Content ---\n{response.text}\n-------------------------")

    except genai.types.BlockedPromptException as e:
        logging.error(f"Prompt was blocked by safety settings: {e}")
    except Exception as e:
        logging.error(f"An error occurred during content generation: {e}")

    logging.info("LLM Cost Predictor Prototype finished.")

if __name__ == "__main__":
    main()
