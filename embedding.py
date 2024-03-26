import requests

class EmbeddingModelClient:
    def __init__(self):
#         self.count = -1
        self.gpt_endpoint = 'https://wmtllmgateway.stage.walmart.com/wmtllmgateway/v1/openai'
        self.gpt_headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': "eyJzZ252ZXIiOiIxIiwiYWxnIjoiSFMyNTYiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiIzOCIsInN1YiI6IjIxNCIsImlzcyI6IldNVExMTUdBVEVXQVktU1RHIiwiYWN0IjoiYTBiMGl5YiIsInR5cGUiOiJBUFAiLCJpYXQiOjE3MTAyNjI0OTAsImV4cCI6MTcyNTgxNDQ5MH0.WDv2W07AhjF_zvM_SX2OiLXUzf4ORmA7YD723nj_GjI"
        }
        self.gpt_parameters = {
            'model': 'text-embedding-ada-002',
            'task': 'embeddings',
            'model-params': {
                "input": ""
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
 
    def embed_text(self, text_to_embed: str):
#         self.count+=1
#         print("count******************************************. ",count)
        self.gpt_parameters['model-params']['input'] = text_to_embed
        response = self._call_llmgateway()
        return response['data'][0]["embedding"]