# Installation Guide

This guide provides detailed instructions for installing pt_hv_parse in different environments.

## System Requirements

- Python 3.9 or higher
- pip or Poetry package manager

## Standard Installation

The simplest way to install pt_hv_parse is using pip:

```bash
pip install pt_hv_parse
```

This will install the latest stable version from PyPI.

## Installation with Poetry

If you're using Poetry for dependency management (recommended), you can add pt_hv_parse to your project:

```bash
poetry add pt_hv_parse
```

## Development Installation

If you want to contribute to pt_hv_parse or install the latest development version, you can install directly from GitHub:

```bash
pip install git+https://github.com/iceNo9/pt_hv_parse.git
```

Or with Poetry:

```bash
poetry add git+https://github.com/iceNo9/pt_hv_parse.git
```

## Installing from Source

You can also install pt_hv_parse from source:

```bash
git clone https://github.com/iceNo9/pt_hv_parse.git
cd pt_hv_parse
pip install .
```

Or with Poetry:

```bash
git clone https://github.com/iceNo9/pt_hv_parse.git
cd pt_hv_parse
poetry install
```

## Verifying Installation

To verify that pt_hv_parse is installed correctly, you can run:

```python
import pt_hv_parse
print(pt_hv_parse.version)
```


Or check the CLI version:

```bash
pt_hv_parse --version
```



## Troubleshooting

If you encounter any issues during installation, try the following:

1. Make sure you have the latest version of pip:

   ```bash
   pip install --upgrade pip
   ```

2. If you're behind a proxy, configure pip to use it:

   ```bash
   pip install --proxy http://user:password@proxyserver:port pt_hv_parse
   ```

3. If you're having dependency conflicts, consider using a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install pt_hv_parse
   ```

If you still have issues, please [open an issue](<https://github.com/iceNo9/pt_hv_parse/issues>) on our GitHub repository.
