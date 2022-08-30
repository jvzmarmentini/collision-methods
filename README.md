# Collision methods
Esse trabalho consiste em desenvolver um programa que avalie algoritmos de inclusão de ponto em triângulos, usando OpenGL. O programa exibe um conjunto de pontos na tela e sobre este exibe um triângulo que simula o campo de visão de um observador em um cenário 3D.

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

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)