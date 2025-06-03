# Routr-ai

## Overview

Routr-ai is a Django-based trip management system designed to automate mileage tracking, store trip records, and generate route summaries using the ChatGPT API. By replacing tedious manual logs with an intelligent system, Routr-ai streamlines trip data entry and enhances efficiency for truck drivers and logistics professionals.

## Inspiration

The idea for Routr-ai came from firsthand experience with the inefficiencies of paper-based trip logging. After receiving a physical log sheet at work that became a burden by the end of the day, the need for a digital, automated solution became clear. Routr-ai is the result — a smarter way to handle trip records with minimal manual input.

## Features

- **Automated Mileage Tracking**: Dynamically calculates estimated mileage between locations.
- **Trip Record Management**: Stores all trip data in a structured, searchable format.
- **AI-Powered Route Summaries**: Uses the ChatGPT API to generate structured trip reports.
- **Stop Management**: Organizes multiple stops with detailed customer information.
- **Fuel Purchase Integration**: Links fuel purchase records with trip data.

## Technologies Used

- **Backend**: Django 5.0.7 (Python)
- **Database**: SQLite (default), configurable for PostgreSQL/MySQL
- **AI Integration**: OpenAI GPT API
- **Data Models**: Django ORM for structured data storage
- **Frontend**: Django templates (with potential for React or Vue.js integration)

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.10+
- Django 5.0.7
- Virtualenv (optional but recommended)

### Setup Instructions

1. Clone the repository:
   ```sh
   git clone https://github.com/brendanprogrammer/routr-ai.git
   cd routr-ai
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```sh
   python manage.py migrate
   ```
5. Create a superuser (optional for admin access):
   ```sh
   python manage.py createsuperuser
   ```
6. Run the server:
   ```sh
   python manage.py runserver
   ```
7. Access the application at `http://127.0.0.1:8000/`

## Configuration

- Update **OpenAI API key** in `gpt_utils.py`:
  ```python
  self.client = OpenAI(api_key="your_openai_api_key")
  ```
- Customize Django settings in `settings.py`.

## Project Structure

```
routr-ai/
│── trip_records/        # Django app for trip records
│   ├── models.py       # Database models (DriverTripRecord, Stop, FuelPurchaseRecord)
│   ├── views.py        # Django views for handling requests
│   ├── urls.py         # URL routing
│── gpt_utils.py        # AI integration for route summarization
│── manage.py           # Django management script
│── db.sqlite3          # SQLite database (default, configurable)
│── .gitignore          # Ignored files (cache, logs, environment variables)
│── README.md           # Project documentation
```

## Usage

1. **Record a Trip**: Enter trip details (start location, stops, fuel purchases).
2. **Generate AI Route Summary**: Use OpenAI GPT to analyze and format trip data.
3. **Retrieve Reports**: View, search, and export trip records.

## AI API Integration

Routr-ai includes an OpenAI-powered journey parser that generates structured trip logs. Example request structure:

```python
openai_client.send_request(data=trip_data, start_location="San Francisco", ending_location="Los Angeles")
```

## Roadmap

- ✅ Basic Django implementation with AI route summarization
- 🚧 REST API for third-party integrations
- 🎨 Improved UI for seamless trip entry
- 📊 Advanced analytics and reporting

## Contributing

Pull requests are welcome! Follow the [contribution guidelines](CONTRIBUTING.md) and ensure code follows PEP8 standards.

## License

MIT License. See `LICENSE` for details.

## Contact

For questions or collaborations, reach out at brendanprogrammer@gmail.com.