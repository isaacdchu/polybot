# Camera
## Methods
center_camera()
- Description:
    - Moves camera to the center of the board
- Parameters:
    - None
- Return:
    - None
tech_tree_camera()
- Description:
    - Sets the camera to view the tech tree
    - Also moves cursor away from tech tree nodes to ensure no interference with screenshots
- Parameters:
    - None
- Return:
    - None
tech_info_camera(tech_name: str)
- Description:
    - Sets the camera to view a specified technology in the tech tree
- Parameters:
    - tech_name: str
        - The name of the technology to focus on
- Return:
    - None
reset_camera()
- Description:
    - Brings camera back to view the game board, with nothing selected
    - Does not move the mouse
- Parameters:
    - None
- Return:
    - None