# Reader
## Methods
get_screenshot_type(img: Image)
- Description:
    - Reads an image and outputs what type of image it is
- Parameters:
    - img: Image
        - The Image object to read
- Return:
    - A string describing what information the screenshot has (used for read_screenshot)
read_screenshot(img: Image, type: str)
- Description:
    - Reads an image and outputs data about what it sees
- Parameters:
    - img: Image
        - The Image object to read
    - type: str
        - The type of screenshot (start_turn, tech_tree, etc.)
- Return:
    - A JSON file of data 