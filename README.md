
# EasySend Automation Test Suite

This repository contains an end-to-end test suite for the EasySend website demo application. Built with Playwright and Pytest, the suite automates critical user flows, validating website functionality under various scenarios, including boundary and edge cases.

## Project Structure

```plaintext
easysend_test_suite/
├── pages/                    
│   ├── base_page.py
│   ├── booking_page.py
│   ├── home_page.py
│   ├── login_page.py
│   └── website.py
├── test_files/              
├── tests/               
│   ├── test_booking.py
│   ├── test_destination.py
│   ├── test_hero.py
│   └── test_login.py
├── .env                  
├── conftest.py         
├── pytest.ini        
└── web_test_structure.txt    
```

## Setup and Installation

### Prerequisites

- Python 3.8+
- Playwright(https://playwright.dev/python/docs/intro)
- Pytest(https://docs.pytest.org/en/stable/)
- Environment variable file `.env` with `BASE_URL` set to the target application URL

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ElidorCohen/easysend_test_suite.git
   ```

2. Navigate to the project directory:

   ```bash
   cd easysend_test_suite
   ```

3. Set up a virtual environment and install dependencies:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   pip install -r requirements.txt
   ```

## Running the Tests

To run specific test files, use:

```bash
pytest tests/<test_file_name>.py
```

To run specific test function, use:

```bash
pytest -k <test_function_name> -s -rx
```

### Configuration Options

You can customize the base URL and other settings in the `.env` file.

## Writing and Structuring Tests

Each test uses Playwright’s `sync_api` to interact with web elements and relies on the `pytest` framework for assertions and parameterization.

For example:

- **Page Objects**: Each page action is encapsulated in classes under the `pages/` directory.
- **Fixtures**: Defined in `conftest.py`, including browser sessions, page instantiations, and reusable elements.

---

## License

This project is open-source, feel free to explore and contribute.
