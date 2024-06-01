import requests
import json
from ssh_client import SSHCommandExecutor

class HttpClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def post(self, url, data):
        try:
            response = requests.post(url, headers=self.headers, json=data)
            return response.json()
        except Exception as e:
            print(f"Error occurred during API call: {str(e)}")
            return None


class ChatAPIService:
    def __init__(self, api_key, model_name="openai/gpt-4-turbo", temperature=1.0):
        self.api_key = api_key
        self.model_name = model_name
        self.temperature = temperature
        self.http_client = HttpClient(api_key)

    def execute_api_call(self, messages, tools):
        url = "https://openrouter.ai/api/v1/chat/completions"
        data = {
            "messages": [
                {"role": msg["role"], "content": msg["content"]} for msg in messages
            ],
            "model": self.model_name,
            "temperature": self.temperature,
            "tools": tools,
        }
        response = self.http_client.post(url, data)
        return response

    async def process(self, api_response, ssh):
        tool_calls = self._extract_tool_calls(api_response)

        if tool_calls:
            return await self._handle_tool_calls(tool_calls, ssh)
        else:
            return await self._process_basic_response(api_response)

    def _extract_tool_calls(self, response):
        if response and "choices" in response and response["choices"]:
            choice = response["choices"][0]
            message = choice["message"]
            if "tool_calls" in message:
                return message["tool_calls"]
        return None

    async def _handle_tool_calls(self, tool_calls, ssh):
        outputs = []
        for tool_call in tool_calls:
            if "function" in tool_call:
                function = tool_call["function"]
                if "name" in function and function["name"] == "execute_command":
                    if "arguments" in function:
                        try:
                            arguments = json.loads(function["arguments"])
                            if "command" in arguments:
                                command = arguments["command"]
                                output = SSHCommandExecutor.execute_ssh_command(command, ssh)
                                outputs.append(output)
                            else:
                                outputs.append("Error: Missing 'command' in tool arguments")
                        except json.JSONDecodeError:
                            outputs.append("Error: Invalid JSON format in tool arguments")
                    else:
                        outputs.append("Error: Missing 'arguments' in tool function")
                else:
                    outputs.append("Error: Unsupported tool function")
            else:
                outputs.append("Error: Missing 'function' in tool call")
        return "\n".join(outputs)

    async def _process_basic_response(self, api_response):
        if api_response and "choices" in api_response and api_response["choices"]:
            choice = api_response["choices"][0]
            message = choice["message"]
            if "content" in message:
                return message["content"].strip()
        return "Error: Unable to retrieve response from the API."