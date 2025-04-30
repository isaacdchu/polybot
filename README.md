# Polybot
An AI bot that plays polytopia (steam version on mac)

## Settings
Suggestions: OFF
Info on Build: ON
Confirm Turn: ON
Replay Fog: ON
Shared Fog: OFF
Auto Focus: ON
Language: English
UI Scale: Medium

## How it works (hopefully)
1. Take screenshot of game window
2. Get information: current stars, stars per turn, etc.
3. Look at current technology tree
4. Analyze possible captures (villages/enemy cities/ruins/starfish)
5. Analyze possible resource gathering (farming/fishing/harvesting)
6. Analyze possible constructions (ports/bridges/roads)
7. Analyze possible unit moves/attacks/creation
8. Execute decisions in the following order:
    1. Ruins / Starfish
    2. Technology
    3. Resources
    4. Constructions
    5. Captures
    6. Unit actions
9. End turn
