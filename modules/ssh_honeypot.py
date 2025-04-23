import socket
import paramiko  # type: ignore
import logging
from typing import Dict, Any


class SSHHoneypot:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger('ssh_honeypot')

    def check_auth_password(self, username: str, password: str) -> int:
        """Authenticate and log SSH attempts (always rejects)"""
        self.logger.info(f"Login attempt: {username}/{password}")
        return paramiko.AUTH_FAILED

    def handle_connection(self, client: socket.socket, addr: tuple) -> None:
        """Handle incoming SSH connections"""
        transport = None
        try:
            transport = paramiko.Transport(client)
            transport.add_server_key(paramiko.RSAKey.generate(2048))
            transport.start_server(server=self)

            self.logger.info(f"SSH connection from {addr[0]}:{addr[1]}")

            chan = transport.accept()
            while chan.active:
                chan.send("$ ")
                command = chan.recv(1024).decode().strip()
                if not command:
                    break
                self._handle_command(chan, command, addr)

        except paramiko.SSHException as e:
            self.logger.error(f"SSH protocol error: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
        finally:
            if transport:
                try:
                    transport.close()
                except paramiko.SSHException as e:
                    self.logger.debug(f"Cleanup error: {e}")

    def _handle_command(self, channel, command: str, addr: tuple) -> None:
        """Process and log commands"""
        self.logger.info(f"Command from {addr[0]}: {command}")

        try:
            if command.startswith("cat "):
                filename = command[4:].strip()
                content = self.config.get('fake_fs', {}).get(filename, "")
                channel.send(f"{content}\r\n")
            else:
                channel.send("command not found\r\n")
        except paramiko.SSHException as e:
            self.logger.error(f"Command handling failed: {e}")
