# TaskTrackerAPI
RESTful API for a simple task management system using FastAPI.

## Project Overview
**Problem statement**: Create a RESTful API for a simple task management system.

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

## Setup and local execution:
- Clone the repo: `git clone https://github.com/ajrvs/TaskTrackerAPI.git`
- Go to the project directory: `cd TaskTrackerAPI`
- Run the FastAPI application using the Uvicorn ASGI server with automatic reloading enabled for development purposes: `uvicorn main:app --reload`
- Uvicorn will be running on Port 8000: ([http://127.0.0.1:8000](http://127.0.0.1:8000)) / ([http://localhost:8000](http://localhost:8000))

## Documentation:

`virtualenv env`: create the virtual environment

`env\Scripts\activate`: activate the virtual environment

`pip install fastapi uvicorn`: install fastapi, uvicorn

Later install "pydnatic" for data/input validation and serialization, and "sqlalchemy" for database management (to store tasks in database).

"main.py" is not using any Database, which means tasks are stored in memory (when server runs) and they will be lost when the server restarts. We are back to square one.

"tasks_tracker.py" file is using SQLite to store tasks in a Database.

To include API documentation using FastAPI's built-in OpenAPI and Swagger UI, you simply need to access the generated documentation at the appropriate URL. FastAPI automatically generates an interactive API documentation page using Swagger UI based on the endpoint definitions and input/output models.

http://localhost:8000/docs: Replace localhost:8000 with the appropriate host and port where your FastAPI application is running (if you're using a different host/port configuration).

---

## Documentation for `tasks_tracker.py`

`app = FastAPI()`:
Set up FastAPI app. Instantiate FastAPI class and assigns it to the variable app.

---

[ done ] Improvement: Consider adding more detailed documentation to your API endpoints using FastAPI's description parameter in the route decorators. This can provide additional context for each endpoint.

---

`filtered_tasks = [task for task in tasks if task.status == status]`:
In the filter_tasks endpoint, you're comparing the status attribute of each task directly with the status parameter, which is an enum member — `class TaskStatus(Enum)`. This will result in a type error since the status attribute is an enum member, but the status parameter is a string. You need to convert the string parameter to the corresponding enum member before comparison — `class TaskStatus(str, Enum)`.

Inheriting from str in the TaskStatus class is a way to ensure that the values assigned to the enum members are of type str. This means that when you access TaskStatus.todo, TaskStatus.in_progress, or TaskStatus.done, you get strings "to do", "in progress", and "done", respectively.

By inheriting from str, you're essentially telling Python that instances of TaskStatus can be treated like strings in many contexts, which can be convenient for operations like string comparison, formatting, and manipulation.

---

[done] Improvement: Since data/tasks is only stored in memory, consider using a Database for Data persistence.

---

### Stepwise:
Integrate SQLAlchemy with SQLite.
###### Install SQLAlchemy and SQLite Driver:
`pip install sqlalchemy`

###### Configure Database Connection:
In your FastAPI application, create a SQLAlchemy Engine object by specifying the connection URL for SQLite. For SQLite, the URL format is sqlite:///path_to_database_file, where path_to_database_file is the path to your SQLite database file.

`SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"`

`engine = create_engine(SQLALCHEMY_DATABASE_URL)`

In SQLAlchemy, the create_engine() function is used to create a new database engine instance. This engine serves as a gateway to the database and manages the connections to it.

- create_engine(): This function is provided by SQLAlchemy and is used to create a new database engine instance.

- SQLALCHEMY_DATABASE_URL: This is a string representing the connection URL to the database. For SQLite, the URL format is sqlite:///path_to_database_file, where path_to_database_file is the path to your SQLite database file. SQLAlchemy will create this SQLite database file if it does not already exist.

- engine: This variable holds the database engine instance created by create_engine(). It will be used to interact with the database throughout your application.

When you call create_engine() with the SQLALCHEMY_DATABASE_URL, SQLAlchemy initializes the database engine with the specified connection settings. The engine manages connections to the SQLite database and handles tasks such as connection pooling, transaction management, and executing SQL commands.

You can then use this engine object to create database sessions, execute SQL queries, and perform various database operations using SQLAlchemy's ORM or core functionality.

###### Define Database Models:
Define your database models using SQLAlchemy's ORM. Each model represents a table in your database, and each attribute represents a column.

`from sqlalchemy.ext.declarative import declarative_base`

`Base = declarative_base()`

In SQLAlchemy, declarative_base() is a function provided by the sqlalchemy.ext.declarative module that creates a base class for declarative class definitions.

- declarative_base(): This function creates a new base class for declarative class definitions. Declarative base classes are used to define database models (i.e., tables) using SQLAlchemy's ORM (Object-Relational Mapping) approach.

- Base: The variable Base holds the base class created by declarative_base(). This base class serves as the parent class for all your database model classes.

When you define your database models (i.e., tables), you'll typically inherit from this Base class. SQLAlchemy will use the attributes and methods of the Base class to track and manage your model classes, including mapping them to database tables, managing database sessions, and performing operations such as creating, querying, updating, and deleting records.

A database model class (Task) is defined using the Base class.

To incorporate the previously defined TaskStatus enumeration into the SQLAlchemy Task model, you can use the Enum type provided by SQLAlchemy.

- import the Enum type from SQLAlchemy
- let it be defined the TaskStatus enumeration as before
- In the Task class, we use `Column(SQLAlchemyEnum(TaskStatus), default=TaskStatus.todo)` to define the status column. By passing SQLAlchemyEnum(TaskStatus) as the type argument, we tell SQLAlchemy to use the TaskStatus enumeration for the column's data type; and a default value of corresponding to TaskStatus.todo.

###### Create Database Session
Create a sessionmaker object to manage sessions with the database. This sessionmaker is bound to your SQLAlchemy Engine.

`SessionLocal = sessionmaker(autocommit=True, autoflush=False, bind=engine)`

In SQLAlchemy, sessionmaker() is a function used to create a factory for database session objects.

- sessionmaker(): This function creates a new session factory. When called, it returns a class that can be used to create database session objects.
- autocommit=False: This parameter specifies that transactions should not be automatically committed after each database operation. By setting autocommit to False, transactions will be managed manually, allowing you to control when changes are committed to the database.
- autoflush=False: This parameter specifies that the session should not automatically flush changes to the database before executing queries. When autoflush is False, you have more control over when changes are flushed to the database, which can improve performance in some scenarios.
- bind=engine: This parameter specifies the database engine to which the session will be bound. The engine object created earlier using create_engine() is passed as an argument to bind, indicating that the session will be associated with this database engine.
- SessionLocal: The variable SessionLocal holds the session factory created by sessionmaker(). This factory can be used to create individual database session objects as needed.

With the SessionLocal session factory, you can create database sessions in your FastAPI application to perform database operations such as querying, inserting, updating, and deleting records. Sessions managed by SessionLocal will use the specified database engine (engine) and adhere to the configured autocommit and autoflush settings.

###### Implement CRUD Operations:
Modify your existing CRUD operations to use SQLAlchemy's ORM to interact with the database. Use the SessionLocal object to create, query, update, and delete database records.

---

This documentation is contributed by ChatGPT.