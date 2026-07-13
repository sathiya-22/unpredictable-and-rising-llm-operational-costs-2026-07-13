## LLM Cost Predictor Prototype

The pervasive challenge of unpredictable and escalating operational costs associated with Large Language Models (LLMs) in production environments is a major concern for AI developers. Factors such as token consumption prior to actual prompt processing, and the varying efficiencies across different LLM versions or providers, make cost management a complex task. This prototype directly addresses this problem by offering a transparent way to estimate token usage and associated costs, enabling better financial planning and optimization.

This tool provides a clear mechanism to:
1.  **Count input tokens** before an API call, highlighting potential pre-processing costs.
2.  **Execute an LLM call** using a configurable model.
3.  **Report actual input and output tokens** consumed.
4.  **Estimate total cost** based on a defined cost-per-token rate.

By centralizing configuration and providing immediate feedback on token consumption, developers can make informed decisions about prompt engineering, model selection, and overall LLM deployment strategies, leading to more predictable and manageable operational expenses.

### Usage:

1.  **Set up your environment:**
    Create a `.env` file in the project root with your Google Gemini API key:
    ```
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the prototype:**
    ```bash
    python main.py
    ```

Observe the token counts and estimated costs for the sample prompt. Modify `main.py` or `config.py` to experiment with different prompts, models, and parameters.
