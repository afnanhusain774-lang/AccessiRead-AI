import requests
import json
import subprocess
import time

def ensure_ollama_is_running():
    url = "http://localhost:11434/api/tags"
    try:
        requests.get(url, timeout=3)
        return True
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        print("⚠️ Ollama server not detected. Attempting auto-start...")
        try:
            subprocess.Popen(
                ["ollama", "serve"], 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL
            )
            for attempt in range(10):
                time.sleep(2)
                try:
                    requests.get(url, timeout=3)
                    print("✅ Ollama successfully started in the background!")
                    return True
                except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                    continue
        except FileNotFoundError:
            return False
    return False

def ask_ollama(text_to_simplify, mode="Accessibility"):
    if not ensure_ollama_is_running():
        return "❌ Error: Could not launch Ollama. Please make sure Ollama is installed!"

    url = "http://localhost:11434/api/generate"
    
    # Cleaned up and safe instructions to prevent false safety triggers
    if mode == "Brainrot":
        system_instruction = (
            "You are a funny translator that rewrites text into modern Gen-Z internet slang. "
            "Translate the text into highly humorous bullet points using harmless words like: "
            "skibidi, rizz, sigma, mewing, fanum tax, W, L, living rent-free, and cooked. "
            "Ensure the translation remains entirely safe, clean, school-appropriate, and respectful."
        )
    else:
        system_instruction = (
            "You are an accessibility assistant helping individuals with learning difficulties. "
            "Take the following text and rewrite it in ultra-simple language using clear, short bullet points."
        )
    
    prompt = f"{system_instruction}\n\nText to translate:\n{text_to_simplify}"
    
    payload = {
        "model": "llama3.2:1b",  
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=45)
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "No response text found.")
        else:
            return f"❌ Ollama Error: Received status code {response.status_code}"
    except Exception as e:
        return f"❌ Error: {str(e)}"
