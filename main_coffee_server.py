import socket
import threading
from main_coffee_bot import JavaAssistant  # Updated import

host = '0.0.0.0'
port = 8888

class CoffeeService:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = None
        self.client = None
        self.assistant = JavaAssistant()  # Updated reference

    def launch_service(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(1)
        print(f"Service active at {self.host}:{self.port}")

        while True:
            self.client, addr = self.server.accept()
            print(f"Connected to {addr}")
            threading.Thread(target=self.manage_client).start()

    def manage_client(self):
        try:
            while True:
                data = self.client.recv(1024).decode()
                if not data:
                    break

                print(f"Client: {data}")
                response = self.assistant.generate_response(data)
                print(f"Response: {response}")
                self.client.sendall(response.encode())

        except (ConnectionResetError, BrokenPipeError):
            print("Client disconnected")
        finally:
            self.client.close()

if __name__ == "__main__":
    service = CoffeeService(host, port)
    service.launch_service()