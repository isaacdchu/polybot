# Reader
## Methods
read_screenshot(img: Image, type: str = None)
- Description:
    - Reads an image and outputs data about what it sees
- Parameters:
    - img: Image
        - The Image object to read
        - Automatically detects what type of image the screenshot is
    - type: str = None
        - Optional parameter that can force the method to read the image a given type
- Return:
    - A JSON file of data 