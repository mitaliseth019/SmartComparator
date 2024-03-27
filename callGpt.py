import requests

class GPTModelClient:
    def __init__(self, model='gpt-35-turbo-16k'):
        self.gpt_endpoint = 'https://wmtllmgateway.stage.walmart.com/wmtllmgateway/v1/openai'
        self.gpt_headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': 'eyJzZ252ZXIiOiIxIiwiYWxnIjoiSFMyNTYiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiIzOCIsInN1YiI6IjIxNCIsImlzcyI6IldNVExMTUdBVEVXQVktU1RHIiwiYWN0IjoiYTBiMGl5YiIsInR5cGUiOiJBUFAiLCJpYXQiOjE3MTAyNjI0OTAsImV4cCI6MTcyNTgxNDQ5MH0.WDv2W07AhjF_zvM_SX2OiLXUzf4ORmA7YD723nj_GjI',  # Replace with your API key
        }
        self.gpt_parameters = {
            'model': model,
            'task': 'chat/completions',
            'model-params': {
                'messages': [
                ]
            }
        }

    def _call_llmgateway(self):
        try:
            try:
                response = requests.post(
                    self.gpt_endpoint, headers=self.gpt_headers, json=self.gpt_parameters)
            except requests.exceptions.SSLError:
                response = requests.post(
                        self.gpt_endpoint, headers=self.gpt_headers, json=self.gpt_parameters, verify=False
                    )
        except requests.exceptions.RequestException as e:
            raise ValueError(e)
        if response.status_code != 200:
            raise ValueError(
                f"Server Error: {response.content}"
            )
        return response.json()
    
    def query_gpt(self, user_query: str):
        self.gpt_parameters['model-params']['messages'].append(
            {
                'role': 'user',
                'content': user_query
            }
        )
        response = self._call_llmgateway()
        #print(response)
        return response["choices"][0]["message"]["content"]
