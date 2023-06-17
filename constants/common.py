class CommonConstants:
    persistance_location = "db"
    input_files_location = 'input_files'
    chroma_db_impl = "duckdb+parquet"
    content_min_length = 5
    openai_llm_model_name = 'gpt-3.5-turbo-0613'
    max_token_for_model = 4096
    max_token_for_completion = 1024
    temperature = 0
    openai_api_key = "OPENAI_API_KEY"
    default_openai_api_key = "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"
    n_results = 50
    proxy_address = 'http://127.0.0.1:10809'