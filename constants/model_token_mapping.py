class ModelTokenMapping:
    OFFSET = 15
    MAPPING = {
        'gpt-3.5-turbo': 4096 ,
        'gpt-3.5-turbo-16k': 16384,
        'gpt-3.5-turbo-0613': 4096,
        'gpt-3.5-turbo-16k-0613': 16384
    }

    @staticmethod
    def get_token(model_name):
        return ModelTokenMapping.MAPPING[model_name] - ModelTokenMapping.OFFSET