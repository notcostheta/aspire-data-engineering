# aspire-data-engineering

## Setup Instructions
1. Clone the repository:
    ```sh
    git clone https://github.com/notcostheta/aspire-data-engineering
    ```
2. Navigate to the project directory:
    ```sh
    cd aspire-data-engineering
    ```
3. Create a virtual environment:
    ```sh
    python -m venv .venv
    ```
4. Activate the virtual environment:
    - On Windows:
        ```sh
        .venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source .venv/bin/activate
        ```
5. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Data Extraction
The data extraction script is located in [`extract.py`](extract.py). It reads data from CSV files in the `data/` directory and processes it.

## SQL Queries
The SQL queries for data transformation are located in the `sql/` directory:
- [`elt_adoption_query.sql`](sql/elt_adoption_query.sql)
- [`elt_usage_query.sql`](sql/elt_usage_query.sql)
- [`etl_adoption_query.sql`](sql/etl_adoption_query.sql)
- [`etl_usage_query.sql`](sql/etl_usage_query.sql)

## Data Analysis
The data analysis is performed using Jupyter notebooks located in the `testing/` directory:
- [`main.ipynb`](testing/main.ipynb)
- [`sql_testing.ipynb`](sql_testing.ipynb)

## Outputs
The results of the data analysis are saved in the `outputs/` directory:
- [`monthly_avg_market_cap.csv`](outputs/monthly_avg_market_cap.csv)
- [`stock_analysis_results.csv`](outputs/stock_analysis_results.csv)

## Plots
Generated plots are saved in the `plots/` directory.

## Contributing
Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.