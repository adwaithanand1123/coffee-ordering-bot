# coffee-ordering-bot
"NAO robot-based coffee ordering HRI system using Python and Choregraphe."

This is an HRI project developed using SoftBank Robotics' NAO robot and a Python socket server.

## Features
- Finite State Machine for dialogue management
- Slot-filling dialogue logic for ordering drinks
- Multimodal output: speech + gesture via Choregraphe
- NLP using spaCy
- Modular architecture (NAO frontend + Python backend)

## How to Run
1. Start `main_coffee_server.py`
2. Open Choregraphe project file and run the behavior
3. Interact using text input to simulate conversation

## Files
- `main_coffee_bot.py`: Dialogue logic
- `main_coffee_server.py`: Socket communication
- `project.pml`: Choregraphe behavior file
