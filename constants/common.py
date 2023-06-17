

from constants.model_token_mapping import ModelTokenMapping


class CommonConstants:
    persistance_location = "db"
    input_files_location = 'input_files'
    chroma_db_impl = "duckdb+parquet"
    content_min_length = 20
    openai_llm_model_name = 'gpt-3.5-turbo-0613'
    max_token_for_model = ModelTokenMapping.get_token(openai_llm_model_name)
    max_token_for_completion = 512
    temperature = 0.2
    openai_api_key = "OPENAI_API_KEY"
    default_openai_api_key = "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"
    n_results = 50
    proxy_address = 'http://127.0.0.1:10809'
