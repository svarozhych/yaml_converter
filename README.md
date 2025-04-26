# CLI YAML Converter
A command-line tool that converts YAML files into human-readable, formatted Word documents using AI-powered analysis.

## 📋 Overview
YAML Converter transforms files with .yml and .yaml extensions into well-formatted documentation. It is designed with the purpose to make Sigma Rules understandable for security professionals. It parses YAML structure, uses Gemma3 AI to convert technical specifications into clear language, and outputs professional Word documents. 

## Features

- Convert single YAML file or process entire directory
- AI-powered transformation of technical YAML into human-readable explanations (useful for SOC analysts and insident response team)
- Properly formatted Microsoft Word output documents
- Comprehensive logging for tracking conversion progress and errors

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Ollama with Gemma3 model installed

### Setup
1. Clone the repository
```
git clone https://github.com/yourusername/yaml-converter.git
```
```
cd yaml-converter
```
2. Install dependencies
```
pip install -r requirements.txt
```
## 💻 Usage

Start ollama with:
```
ollama pull gemma3
```
Run the CLI tool with:
```
./yaml_converter
```

## 📄 Output

The tool generates:
- `final.docx` for batch conversions
- `converted_yaml.docx` for single file conversions
- Log files: `info.log` and `error.log`

## 🔧 Configuration

Logging can be configured in `log_conf.py`.

The output text format can be configered in `text_format.py`.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 💌 Contact

Mariia Kyrychenko - mariia.kyrychenko@outlook.com