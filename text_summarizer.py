import os
import httpx
import gradio as gr

# Configurable via environment variables
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("MODEL_NAME", "INSERT YOUR MODEL NAME HERE")
HTTP_TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "60"))


def summarize_text(text: str, bullets: int = 3) -> str:
    """Call the Ollama endpoint to summarize text with DeepSeek.

    Args:
        text: Input text to summarize
        bullets: Number of bullet points desired
    Returns:
        The summarized text or an error message
    """

    if not text or not text.strip():
        return "Please enter some text to summarize."

    prompt = f"Summarize the following text in {bullets} bullet points:\n\n{text}"
    payload = {"model": MODEL_NAME, "prompt": prompt, "stream": False}

    try:
        with httpx.Client(timeout=HTTP_TIMEOUT) as client:
            resp = client.post(OLLAMA_URL, json=payload)
    except httpx.RequestError as e:
        return f"Error: upstream service unreachable: {e}"

    if resp.status_code != 200:
        return f"Error from upstream ({resp.status_code}): {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        return "Error: invalid JSON from upstream service"

    return data.get("response", "No summary generated.")



# Create Gradio interface
with gr.Blocks(title="AI-Powered Text Summarizer") as interface:
    gr.Markdown("# AI-Powered Text Summarizer")
    gr.Markdown(
        "Enter text and choose how many bullet points you want. The app calls your local Ollama endpoint."
    )
    with gr.Row():
        txt = gr.Textbox(label="Input Text", lines=10, placeholder="Paste text to summarize...")
    with gr.Row():
        bullets = gr.Slider(1, 10, value=3, step=1, label="Bullet Points")
    with gr.Row():
        btn = gr.Button("Summarize")
    out = gr.Textbox(label="Summarized Text")

    btn.click(summarize_text, inputs=[txt, bullets], outputs=out)

# Launch the web app
if __name__ == "__main__":
    # Listen on all interfaces for container/cloud use; change as needed.
    interface.launch(server_name="0.0.0.0")


# # Test Summarization
# if __name__ == "__main__":
#     sample_text = """
#     Artificial Intelligence is transforming industries across the world. AI models like DeepSeek-R1 enable businesses to automate tasks,
#     analyze large datasets, and enhance productivity. With advancements in AI, applications range from virtual assistants to predictive analytics
#     and personalized recommendations.
#     """
#     print("### Summary ###")
#     print(summarize_text(sample_text))
