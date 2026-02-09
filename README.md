# README

## Introduction
A simple chat-like server written with Spring Boot. This project is intended as a learning exercise and should not be used in production.

### Closer Description
Encryption for messages is handled by clients using their private keys. The server provides public keys to users.
Each user has a mailbox, where they can send and receive messages without the server keeping track of who sent them.
To authenticate users, the server sends a nonce to clients, which must be signed with the client's private key before a JWT token is issued.

Currently, the python client only exists for debugging/testing purposes.

## Getting Started
To run this application, you need a postgres server running. You can find the configuration file at src/main/resources/application.properties. 
Follow these steps:

```
cd Docker
docker compose up
cd ..
mvn clean package
java -jar target/chat-0.0.1-SNAPSHOT.jar
```

You will need to have Maven installed on your machine.
## Features
The following features are implemented:

* User registration
* User authentication
    * Challenge-Response to obtain a JWT
* Sending and receiving messages


## API
### /auth/nonce/{id}

Generate a unique nonce for a specific user ID. The nonce is used to authenticate the user's requests and ensure that only authorized users can access certain features or data.

### /auth/token

Verify the authenticity of a request by checking the signature provided with the request. If the signature is valid, an access token is generated and returned in response, allowing the requesting user to access restricted resources or services.

### /user
Retrieve a list of users whose names match the given query parameter. This endpoint returns all matching users found by name.

### /user/create
Register a new user. Provide the necessary details about the user (name, public key, etc.) in the request body.

### /user/all
Retrieve a list of all registered users. This endpoint returns information for all users available in the database.

### /msg

**POST**:
Send a message to another user. The client must sign the request with their private key to ensure authenticity.

**GET**:
Retrieve a list of messages sent to the authenticated user.

### /msg/{id}
**DELETE**:
Delete a message from the mailbox.

## Limitations
Please keep in mind that this is a simple proof-of-concept and should not be considered a fully-featured chat server.

