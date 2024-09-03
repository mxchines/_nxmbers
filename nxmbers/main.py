import config
from config import USER_TICKER, USER_START_DATE, USER_END_DATE, USER_INTERVAL, USER_API_SOURCES, BEAM_API_KEY
from app import update_config_data
from data_ingestion.data_combiner import main as combine_data
from prediction_model.r_model_executor import run_r_models
from results_storage.results_saver import save_results
from data_storage.rds_uploader import upload_to_rds

def main():
    # Fetch data
    update_config_data(
        ticker=config.USER_TICKER,
        start_date=config.USER_START_DATE,
        end_date=config.USER_END_DATE,
        interval=config.USER_INTERVAL,
        api_sources=config.USER_API_SOURCES,
        beam_api_key=config.BEAM_API_KEY
    )

    # Combine data
    combine_data(config.USER_TICKER)

    # Upload cleaned data to RDS
    table_name = upload_to_rds()
    print(f"Data uploaded to RDS table: {table_name}")

    # Run R models
    run_r_models()

    # Save results
    save_results()

if __name__ == "__main__":
    main()