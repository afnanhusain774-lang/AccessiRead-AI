import requests
import json
import subprocess
import time

def ensure_ollama_is_running():
    """Checks if Ollama is running, and launches it safely if it's not."""
    url = "http://localhost:11434/api/tags"
    try:
        # Step 1: See if it's already awake
        requests.get(url, timeout=3)
        return True
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        print("⚠️ Ollama server not detected. Attempting auto-start...")
        try:
            # Step 2: Fire up the Ollama background process
            subprocess.Popen(
                ["ollama", "serve"], 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL
            )
            
            # Step 3: Give it a patient, safe loop to wake up without throwing errors
            for attempt in range(10):  # Try for up to 20 seconds total
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

def ask_ollama(text_to_simplify):
    # Make sure Ollama is awake before firing our API query
    if not ensure_ollama_is_running():
        return "❌ Error: Could not launch Ollama. Please make sure Ollama is installed on your machine!"

    url = "http://localhost:11434/api/generate"
    
    prompt = (
        f"You are an accessibility assistant helping individuals with learning difficulties. "
        f"Take the following text and rewrite it in ultra-simple language using clear, short bullet points: \n\n{text_to_simplify}"
    )
    
    payload = {
        "model": "llama3.2:1b",  
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=45) # Patient timeout for generating long text
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "No response text found.")
        else:
            return f"❌ Ollama Error: Received status code {response.status_code}"
    except Exception as e:
        return f"❌ Error: {str(e)}"