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
UI Scale: Small
Map size: Tiny (121 tiles)

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

## Game state representation
1. 11 x 11 matrices of the tiles (FoW, field, crop, forest, ruins, etc.)
2. Each tile using a different matrix?

## Roadmap
In-depth description of how the AI will make a turn, from start to finish.

### Get data
1. Take screenshots of game to get map data
2. Check current tech tree
3. Read/parse data from these images to get a complete image of game state
4. Store this data

### Process data
1. Convert categorical data to numerical data through one-hot encoding
2. Append to matrix of data
3. Get an output from the model
4. Convert output into tangible actions

### Make turn
1. Get actions needed to be made
2. Filter out "impossible" moves
3. Execute them in the correct order (as described above)
4. End turn

