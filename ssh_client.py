

class SSHCommandExecutor:
    @staticmethod
    def execute_ssh_command(command, ssh):
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        return output
