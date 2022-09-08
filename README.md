# Collision methods
This application is a study of collision detection algorithms between a set of points and a polygon, using OpenGL. The main program displays the set of points into the screen as well as a triangule to simulate the field of vision of a observer in a 3D scenario

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install PyOpenGL.

```bash
pip install -r requirements.txt
```

Obs 1: We strongly recommend to use a [virtual env](https://docs.python.org/3/library/venv.html) to isolate the packages.

### macOS 

Go to `OpenGL/platform/ctypesloader.py` and set

```python
fullName = "/System/Library/Frameworks/{}.framework/{}".format(name,name)
```

This path location depends on your python installation. If you're using a virtual env as venv, this is under `venv/lib/python3.x/site-packages`

## Usage

```bash
python main.py
```

### File

To read the set of points from a file, use:

```bash
python main.py --file {filepath}
``` 

You must use the following pattern in your file:

```txt
x_cord_1 y_cord_2
x_cord_2 y_cord_2
...
x_cord_n y_cord_n
```

## Docker

```diff
This is NOT working in red
```

### Install and Setup

[Install Docker on your machine](https://docs.docker.com/get-docker/).
Then, build the .dockerfile 
    
```bash
docker build -t collision-method .
```

### Usage

```bash
docker run collision-method
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
