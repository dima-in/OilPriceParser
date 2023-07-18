# OilPriceParser

This project is a web scraper that retrieves and stores oil prices from a specific website. It provides an API endpoint to fetch the prices and a web interface to view and filter the saved prices.

### Installation

To run the project locally, follow these steps:

1. Clone the repository:

   ```shell
   git clone https://github.com/dima-in/OilPriceParser.git
   ```

2. Change into the project directory:

   ```shell
   cd OilPriceParser
   ```

3. Install the dependencies:

   ```shell
   pip install -r requirements.txt
   ```

### Usage

To start the application, run the following command:

```shell
python main.py
```

The application will be available at `http://localhost:8000` in your browser.

### API Endpoints

- **GET /natureexpressprices**: Retrieves the current oil prices from the website.

### Web Interface

The web interface provides the following endpoints:

- **GET /entry**: Displays the initial template for the application.

- **POST /viewprices**: Allows filtering and viewing the saved oil prices. The parameters for filtering include:
  - `site`: The website to filter the prices from.
  - `oil_name`: The name of the oil to filter.
  - `price`: The exact price to filter.
  - `max_price`: The maximum price to filter.
  - `start_date`: The start date to filter.
  - `end_date`: The end date to filter.

### Dependencies

The project relies on the following dependencies:

- `asyncio`
- `aiohttp`
- `fastapi`
- `Jinja2`
- `pprint`
- `time`
- `requests`
- `beautifulsoup4`
- `BDalchemy`

These dependencies are listed in the `requirements.txt` file.

### Contributing

If you want to contribute to this project, feel free to submit a pull request. Please make sure to follow the established coding style and conventions.

### Author

This project was developed by [Dima](https://github.com/dima-in).
