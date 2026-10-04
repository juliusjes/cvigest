from google import genai


def send_prompt(prompt, model):
    client = genai.Client()
    interaction = client.interactions.create(model=model, input=prompt)
    out = interaction.output_text
    return out



if __name__ == "__main__":
    import dotenv

    import os

    print(os.getenv("GEMINI_API_KEY"))

    out = send_prompt("respond with a random green animal")
    print(out)
