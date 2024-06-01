import argparse
import getpass
import asyncio
from utils import CLI, SSHConnection
from config import Config


async def main():
    parser = argparse.ArgumentParser(description='CLI with ChatGPT API')
    parser.add_argument('--host', default=Config.SSH_HOST, help='SSH host')
    parser.add_argument('--port', type=int, default=Config.SSH_PORT, help='SSH port')
    parser.add_argument('--username', default=Config.SSH_USERNAME, help='SSH username')
    args = parser.parse_args()

    password = getpass.getpass(prompt='Enter SSH password: ')

    ssh = SSHConnection.establish_connection(args.host, args.port, args.username, password)

    try:
        await CLI.cli_loop(ssh)
    finally:
        ssh.close()


if __name__ == '__main__':
    asyncio.run(main())