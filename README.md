# ManualImageClassification

Displays each image in the directory given and allows user to create bounding boxes
which get saved with the image path in the json output.

Tested on Linux using Python 3.5

### Install 

- If using `apt` package manager,
    - `sudo apt install python3-tk python3-pil.imagetk`
- clone this repo
- `pip3 install -r requirements.txt`

### Usage

Modify `run.py` to point to your directory of images.

Run with `python3 run.py`

##### Hotkeys

| Button | Description |
| --- | --- |
| left click | creates a single point (2nd left click creates the rectangle) |
| right click | remove previous rectangle or stand-alone point |
| Escape | Save and continue to next image |

You may also close the window at any point to save and exit.
