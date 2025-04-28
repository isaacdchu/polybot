# Screenshot
## Methods
take_screenshot(name: str)
- Description:
    - Takes a screenshot of the game's window (2048px x 1534px)
    - Stores the file in `src/screenshot/data/name.png`
- Parameters:
    - name: str
        - The name of the file to be stored. Will overwrite if name is already taken
- Return:
    - A PIL Image object of the screenshot taken