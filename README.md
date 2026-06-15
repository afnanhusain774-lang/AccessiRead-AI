# AccessiRead AI
Tagline
An offline, intelligent desktop accessibility companion empowering neurodivergent students by instantly simplifying complex text.

# Inspiration
Reading dense textbooks, complex research articles, or confusing news updates can be an overwhelming barrier for students with learning differences or neurodivergent profiles such as dyslexia, ADHD, or hyperlexia. Iwanted to build a seamless, distraction-free desktop tool that instantly strips away complicated vocabulary and transforms walls of text into highly structured, clear, and action-oriented bullet points—making learning accessible to everyone.

# What it does
AccessiRead AI lives on the user's desktop. When a student encounters a difficult piece of writing anywhere on their computer (browser, PDF viewer, or e-book reader), they simply highlight and copy it. With a single click of our application's button, the app grabs the text from their clipboard, communicates with a local language model, and returns an ultra-simplified summary.

# How I built it
The application is structured cleanly using a modern local AI architecture:

Frontend UI: Built using Python and PyQt6 to create a custom, high-contrast dark-themed desktop interface optimized for readability and focus.

AI Backend Engine: Configured to integrate seamlessly with Ollama, running the lightweight and highly efficient Llama 3.2:1b model entirely offline on the user's machine.

Asynchronous Multi-threading: Implemented using QThread and pyqtSignal workers to ensure that when the AI engine is processing data, the main user interface stays perfectly fluid, responsive, and never crashes or freezes.

Automation: Added sub-process management to automatically detect and safely launch the background Ollama server if it isn't already active.

# Challenges I ran into
As a solo creator learning to coordinate desktop apps and AI, managing synchronous delays was a major hurdle. Initially, when the AI was thinking, the entire desktop interface would lock up and throw "(Not Responding)" errors. Learning to break the architecture apart into multithreaded background workers so the window stays active and movable was a massive milestone. Ialso engineered patient, loop-based exception handling to prevent application crashes while waiting for the local AI model to boot up.

# Accomplishments that I proud of
Iare proud to have built a fully functioning, locally hosted machine learning application with zero experience! The entire system runs entirely locally and offline—meaning students do not need an active internet connection, don't have to worry about data privacy, and don't need to pay for expensive API keys.

# What I learned
I learned the fundamentals of visual interface design with PyQt6, asynchronous programming in Python, how local open-source LLMs communicate via local API payloads, and how to elegantly debug server timeouts.

What's next for AccessiRead AI
I plan to introduce system-wide keyboard global hotkeys (e.g., Ctrl + Shift + A) so students don't even have to open the window to simplify text, add Text-to-Speech (TTS) capabilities to read the simplified points aloud, and build a history tab to save previously summarized materials for easy studying later.
