# Currency Converter

A modern desktop currency converter built with **Python** and **Tkinter**.

The application uses the **Alpha Vantage API** to retrieve currency exchange rates. It includes a clean responsive interface, multiple currencies, input validation, currency swapping, and both light and dark themes.

## Features

- Currency conversion using the Alpha Vantage API
- More than 40 supported currencies
- Light and dark themes
- Currency swap button
- Responsive Tkinter interface
- Input validation
- Network and API error handling
- Non-blocking API requests using a background thread
- Press `Enter` to start a conversion
- Clear button to reset the form
- Exchange-rate information below the converted amount

## Requirements

- Python 3.9 or newer
- Internet connection
- Alpha Vantage API key

## Project Structure

```text
currency-converter/
├── currency_converter.py
└── README.md
```

## Installation

### 1. Download the project

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/currency-converter.git
cd currency-converter
```

You can also download the project as a ZIP file and extract it.

### 2. Create a virtual environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Linux and macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the required package

```bash
pip install requests
```

## API Key Setup

Create an API key on the Alpha Vantage website.
