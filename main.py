import config
from data_ingestion.data_fetcher import main as fetch_data
from data_cleaning.data_cleaner import clean_data
from prediction_model.r_model_executor import run_r_models
from results_storage.results_saver import save_results

def main():
    # Fetch data
    fetch_data(
        ticker=config.USER_TICKER,
        start_date=config.USER_START_DATE,
        end_date=config.USER_END_DATE,
        interval=config.USER_INTERVAL,
        api_key=config.USER_API_KEY
    )

    # Clean data
    clean_data()

    # Run R models
    run_r_models()

    # Save results
    save_results()

if __name__ == "__main__":
    main()