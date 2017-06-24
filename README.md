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

---

### Example

![eg](https://gfycat.com/VictoriousIncomparableAfricanjacana)

output in `img_classifications.json`

```bazaar
{
  "/home/j/_Github-Projects/ManualImageClassification/example/pictures/iron ore2.png": {
    "tree": [
      [
        736,
        173,
        833,
        239
      ],
      [
        1900,
        54,
        1996,
        116
      ],
      [
        2436,
        951,
        2530,
        1011
      ]
    ]
  },
  "/home/j/_Github-Projects/ManualImageClassification/example/pictures/iron ore3.png": {
    "tree": [
      [
        857,
        1158,
        973,
        1212
      ],
      [
        1872,
        815,
        1970,
        863
      ],
      [
        2026,
        1039,
        2127,
        1095
      ]
    ]
  },
  "/home/j/_Github-Projects/ManualImageClassification/example/pictures/iron ore1.png": {
    "tree": [
      [
        1473,
        680,
        1573,
        742
      ],
      [
        1553,
        949,
        1669,
        995
      ]
    ]
  }
}
```