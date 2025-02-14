# Lexicon Agent

A sophisticated natural language processing system that combines risk analysis and intent matching capabilities.

## Project Structure

```
lexicon_agent/
├── analysis_service/
│   ├── agent/
│   │   ├── match_intent.py
│   │   └── risk_detect.py
│   ├── services/
│   │   └── risk_detector.py
│   └── main.py
└── safe_service/
    └── config.py
```

## Setup

1. Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
Create a `.env` file in the project root and add your configuration:
```
OPENAI_API_KEY=your-api-key-here
# Add other required environment variables
```

## Features

- Intent matching system
- Risk detection and analysis
- Natural language processing capabilities
- Configurable safety parameters

## Usage

Run the analysis service:
```bash
python analysis_service/main.py
```

## Development

The project is structured into two main services:
- Analysis Service: Handles intent matching and risk detection
- Safe Service: Manages configuration and safety parameters

## License

[Add your license information here]
