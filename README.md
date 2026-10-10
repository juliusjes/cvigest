# cvingest

Simple CV customizer.

## Requirements

- Python 3.12+
- pydantic
- google-genai
- dotenv
- PyYaml

## Installation

Install Latex dependencies:
```bash
sudo apt install texlive-latex-base texlive-latex-extra
```

Install Python depencies:
```bash
pip install pandas google-genai dotenv PyYaml
```

Clone the repository and install the package:

```bash
pip install .
```
or for editing using the "-e" flag.

Create a .env file with key 'GEMINI_API_KEY'.

## Usage



## Project structure

```text
cvingest/
├── pyproject.toml
├── src/
│   └── cvingest/
└── README.md
```

## Development

The project uses [setuptools](https://setuptools.pypa.io/) as its build backend.

Package discovery is configured to use the `src` directory:

```toml
[tool.setuptools.packages.find]
where = ["src"]
```

## License

License information has not yet been specified.
