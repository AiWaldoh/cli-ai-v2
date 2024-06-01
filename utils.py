
import os
import paramiko
from config import Config
from http_client import ChatAPIService
from ssh_client import SSHCommandExecutor
import yaml
class CommandExecutor:
    @staticmethod
    async def execute_command(command, ssh):
        if command.split()[0] in Config.WHITELISTED_COMMANDS:
            return SSHCommandExecutor.execute_ssh_command(command, ssh)
        else:
            chat_api = ChatAPIService(Config.OPENAI_API_KEY)
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{command}?"}
            ]
            
            # Read the tools from the YAML file
            with open('tools.yaml', 'r') as file:
                tools_data = yaml.safe_load(file)
                tools = tools_data['tools']
            
            api_response = chat_api.execute_api_call(messages, tools)
            return await chat_api.process(api_response, ssh)
         
class CLI:
    @staticmethod
    async def cli_loop(ssh):
        while True:
            # Get the current working directory
            cwd = os.getcwd()
            # Format the prompt with colored username, host, and path
            prompt = f"{Config.ANSI_COLOR_BLUE}{Config.SSH_USERNAME}{Config.ANSI_COLOR_CYAN}@{Config.SSH_HOST}:{Config.ANSI_COLOR_GREEN}{cwd}{Config.RESET_COLOR}~$ "
            command = input(prompt)
            if command.lower() == 'exit':
                break
            output = await CommandExecutor.execute_command(command, ssh)
            print(output)


class SSHConnection:
    @staticmethod
    def establish_connection(host, port, username, password):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=username, password=password)
        return ssh
