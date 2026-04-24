from ocr import UniversalOCR
import requests
import os

# ---------- INIT ----------
ocr1 = UniversalOCR(
    tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma4:e2b"

def ask_llm(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]


def process_file(path):
    text = ocr1.read(path)

    print("\n📄 Extracted Text Preview:\n")
    print(text[:1000])

    prompt = f"""
Summarize and extract key insights from this document:

{text}
"""
    return ask_llm(prompt)


def chat():
    print("\n💬 Chat mode (type 'exit' to quit)\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        response = ask_llm(user_input)
        print("AI:", response)


if __name__ == "__main__":
    while True:

        print("1. Upload PDF/Image")
        print("2. Chat only")
        print("3. exit")

        choice = input("Choose option: ")

        if choice == "1":
            path = input("Enter file path: ")

            if not os.path.exists(path):
                print("❌ File not found")
            else:
                result = process_file(path)
                print("\n🤖 AI Response:\n")
                print(result)

        elif choice == "2":
            chat()
        elif choice == "3":
            break