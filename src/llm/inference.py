# src/llm/inference.py

class Inference:
    def __init__(self, mistral_client):
        self.mistral_client = mistral_client

    def perform_inference(self, input_data):
        """
        Perform inference using the Mistral LLM.

        Args:
            input_data (str): The input data for the LLM.

        Returns:
            str: The output from the LLM.
        """
        response = self.mistral_client.query(input_data)
        return response.get('output', '')

    def batch_inference(self, input_data_list):
        """
        Perform batch inference using the Mistral LLM.

        Args:
            input_data_list (list): A list of input data for the LLM.

        Returns:
            list: A list of outputs from the LLM.
        """
        outputs = []
        for input_data in input_data_list:
            output = self.perform_inference(input_data)
            outputs.append(output)
        return outputs