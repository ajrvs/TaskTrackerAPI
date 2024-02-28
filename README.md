# TaskTrackerAPI
## Project Overview
#### Problem statement:
**Problem**: Create a RESTful API for a simple task management system.

**Requirements**:

1. The API should allow users to create, read, update, and delete tasks.
2. Each task should have a title, description, status (e.g., "to do", "in progress", "done"), and a due date.
3. Users should be able to retrieve a list of all tasks, retrieve a specific task by its ID, update a task's details, and delete a task.
4. Implement appropriate error handling for cases such as trying to retrieve a non-existent task or providing invalid data for task creation or updates.
5. Use appropriate HTTP methods (GET, POST, PUT, DELETE) and status codes.
6. Ensure data persistence, either using an in-memory database like SQLite or by connecting to an external database.
7. Include API documentation using FastAPI's built-in OpenAPI and Swagger UI.
8. Implement input validation to ensure that required fields are provided and that data types are correct (e.g., due date should be a valid date).

This problem provides a good exercise for building a basic CRUD (Create, Read, Update, Delete) API using FastAPI.

## Work

`virtualenv env`: create the virtual environment

`env\Scripts\activate`: activate the virtual environment

`pip install fastapi uvicorn`: install fastapi, uvicorn and pydnatic (later install sqlalchemy to store tasks in database)

main.py file is without using any Database. So, each time the server is restarted. We are back to square one.

tasks_tracker.py file is using SQLite to store tasks in a Database.

To include API documentation using FastAPI's built-in OpenAPI and Swagger UI, you simply need to access the generated documentation at the appropriate URL. FastAPI automatically generates an interactive API documentation page using Swagger UI based on the endpoint definitions and input/output models.

http://localhost:8000/docs: Replace localhost:8000 with the appropriate host and port where your FastAPI application is running if you're using a different host/port configuration.