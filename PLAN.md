Here is a comprehensive, deterministic plan designed specifically to be copy-pasted into an AI coding assistant (like Claude Code, Cursor, or Gemini CLI) so it can execute the environment setup, context compression, and inference seamlessly. 

---

## High-Level Overview

To replicate Chris Hay’s 370k context compression on an Apple Silicon MacBook, your AI agent will need to complete four phases:
1.  **Environment Setup:** Install `uv` (a fast Python package installer) and Apple's `mlx` framework.
2.  **Asset Acquisition:** Clone the target document (Apollo 11 transcript) and the activation engineering toolkit (`chuk-lazarus`).
3.  **Knowledge Build (The 2.8MB Compression):** Process the 370k token document through Gemma 3 4B, extracting and saving the 10KB residual boundary vectors at the end of each 512-token window. 
4.  **Bounded Inference:** Run the query against the compressed store using the external token-matching index and residual stream injection.

---

## The Recipe: Step-by-Step Execution Plan

### Phase 1: Environment Setup
*   **Step 1:** Ensure `uv` is installed on the host system. (If not, run `curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh`).
*   **Step 2:** Create a new Python virtual environment using `uv venv` and activate it.
*   **Step 3:** Install required ML libraries. The agent must run:
    ```bash
    uv pip install mlx transformers huggingface_hub
    ```
*   **Step 4:** Authenticate with Hugging Face. Gemma 3 requires accepting an end-user license agreement. The agent should prompt the user to ensure they have run `huggingface-cli login` with a valid token that has Gemma 3 access.

### Phase 2: Cloning the Repositories
*   **Step 1:** Clone the `apollo-demo` repository to get the raw text document.
    ```bash
    git clone https://github.com/chrishayuk/apollo-demo.git
    ```
    > The target file will be located at `./apollo-demo/docs/apollo11_clean.txt`
*   **Step 2:** Clone Chris Hay's interpretability and residual checkpointing toolkit (`lazarus`).
    ```bash
    git clone https://github.com/chrishayuk/chuk-lazarus.git
    cd chuk-lazarus
    ```
*   **Step 3:** Install the Lazarus dependencies using `uv`.
    ```bash
    uv pip install -e .
    ```

### Phase 3: Building the "Markov Store" (Context Compression)
*   **Step 1:** Execute the `knowledge build` command via the Lazarus CLI. This will chunk the Apollo 11 transcript, run the forward passes, and save the residual state boundaries to a local directory (compressing the 56GB theoretical KV cache down to ~2.8MB). 
    *   *Agent Command:*
    ```bash
    uv run lazarus knowledge build \
      -m mlx-community/gemma-3-4b-it-bf16 \
      -i ../apollo-demo/docs/apollo11_clean.txt \
      -o ./apollo11_store
    ```
    > **Note to Agent:** This process will take a while as it processes all 370,000 tokens through the 4B parameter model. Monitor the output logs for completion.

### Phase 4: Bounded Inference (Querying the Store)
*   **Step 1:** Once the build is complete, execute a query using the `knowledge query` command. This uses the external index to find the relevant 512-token window, loads the boundary residual, and answers the prompt.
    *   *Agent Command:*
    ```bash
    uv run lazarus knowledge query \
      -m mlx-community/gemma-3-4b-it-bf16 \
      -s ./apollo11_store \
      -p "find 3 amusing moments in the transcript" \
      --max-tokens 400
    ```

---

Are you planning to run this setup on your own machine today, or are you just gathering the architecture details for now?