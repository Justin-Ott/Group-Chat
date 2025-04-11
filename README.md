## Overview
# Chat Server Design
The server uses a basic client-server architecture to facilitate communication between connected clients. The primary data structures used on the server are as follows:
Connected Clients (Dictionary):


## Structure: {client_socket: username}


Description: A dictionary that maps each client’s socket object to its corresponding username. This tracks which user is associated with which socket for sending and receiving messages.


Client Queue (List):


## Structure: [client_socket, ...]


Description: A list of client socket objects that are currently connected to the server. This list is used to broadcast messages to all clients.


# Operations
accept_connections: This function accepts incoming client connections. It listens for new connections and assigns each connected client to a new thread for handling communication.


handle_client: Each client has a dedicated thread running this function. This function continuously listens for messages from the client, handles the sending and receiving of messages, and sends the message to all other clients.


broadcast_message: This function sends a message to all connected clients.


handle_disconnection: When a client disconnects, this function handles the cleanup by removing the client from the connected_clients dictionary and the client_queue list.



# Chat Client Design
The client application has the following data structures:

Socket Object: Each client connects to the server via a socket object, which is used to send and receive messages.


Message Queue (Local): Although not explicitly implemented, the message queue is logically represented as the order in which messages are displayed in the chat window. The messages are received from the server and displayed in the order they are received.


Username: The client asks for the username at the beginning of the connection and uses it to identify the sender of the messages.


## Operations
connect_to_server: This function establishes the connection between the client and the server by creating a socket connection to the server's IP address and port.


send_message: When the user sends a message, it is inserted into the chat area and immediately sent to the server.


receive_message: This function listens for incoming messages from the server and displays them in the chat window.


emoji_shortcut_handler: This function interprets and replaces emoji shortcuts (like :thumbsup:) with their corresponding Unicode characters before sending them.


URL_handler: A function to interpret URLs within the text and convert them into clickable links in the chat.


# Responsibilities & Developer Coordination
Team Member Responsibilities
Justin Ott- Solo project so just did everything myself.




