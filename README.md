# API Template
This is a template to follow when creating APIs

## Running Locally
### Docker (quick)
1. Navigate to root directory
2. Run with `docker-compose up -d`
### Virtual Environment (better debugging)
_Assumes you're using PyCharm_
1. Navigate to root directory
2. Start database in docker with `docker-compose run -d --service-ports db`
3. Create a new virtual environment at `.venv`
4. Navigate to root directory
5. Activate virtual environment with `source .venv/bin/activate`
6. Install requirements with `pip install -r src/requirements.txt`
7. Create new Python run configuration
   1. `script` -> `[root]/src/app.py`
8. Run
### Validation
In a browser, hit `http://localhost:5000/healthcheck`.
If everything is running properly, this should return `Success`

## Folder Structure
```
src
 + clients       # clients for third party integrations go here
 + daos          # daos go here
 + endpoints     # endpoints go here
 + migrations    # migration scripts go
 + models        # models (ORM, DTO, etc) go here
 + services      # business logic goes here
```

## Folder Structure Rationale
Software inevitably changes - features will need to be added, technology requirements will evolve, and business goals will pivot.
This means that software must be created with flexibility in mind, so new additions can easily be plugged into the existing codebases with minimal changes.
This allows developers to iterate efficiently and easily.
With this in mind, the backbone of software design is modularity;
individual software components (functions, classes, files, folders) should be responsible for one specific functionality, so they can be added, removed, or updated without affecting other areas of the codebase.

Think about this example:

>Suppose we have an API with 50 endpoints that query a database and return some data.
We then write 50 functions, and all of them independently connect to the database.
It works great, but a week later, we find out we need to change the way we're connecting to the database.
Now we need to go into all 50 functions and change them individually - this is time-consuming and wasteful.
Instead, imagine we had an extra class that is _only_ responsible for connecting to the database.
We use this class in all of our 50 functions.
At first, everything is the same, but when we're asked to change the way we connect to the database, we only need to make one change rather than 50.
This is much more efficient.

>_side note, this is the DBController class in the `daos` folder_

This is exactly what our folder structure accomplishes, just on a higher level.
It immediately separates abstract functionality, and within each folder we can (and must) split into more modules.
The most common flow of information we'll use for endpoints is:

`endpoint layer --> services layer --> database (dao) layer`

The endpoint layer parses information from the API request and sends it to the services layer.
- When a service layer function is called, it doesn't know where the parameters came from.
That's beyond the scope of its responsibilities.
In fact, it doesn't even know that the `endpoints` layer exists. 

Then the services layer calls a function in the database layer to fetch some stored information.
- When the database layer returns data, the service layer doesn't know where it came from. That's beyond the scope of its responsibilities.
- On the flip side, when the database layer returns data, it doesn't know or care what's being done with that information. That's beyond the scope of its responsibilities. 

This modularity is powerful when we need to make changes.
If we need to change the way we're getting data from the database, we only need to make updates to the database layer.
None of the other modules know or care what's happening, as long as it gets the data that it expects.


## Folder Explanations
### `clients` folder
This folder contains all the logic for communicating with third party applications.

#### What to do here
- Make API requests to other services
- Parse API responses into native models
#### What not to do here
- Handle business logic
- Access the database

### `daos` folder
This folder contains all of your Database Access Objects (`DAOs`).
Each `DAO` should have its own file, and each model / domain should have its own DAO.

When dealing with objects, a `DAO` should always accept (as parameters) and return `DTOs` (data transfer object).
In other words, only the `DAO's` internal functions should see ORM models.

_if the above section is confusing, see the `models` section_

In addition, each `DAO` should inherit from `BaseDAO`.
This offers a few pre-made functions which should cover most basic database functionality:
- `insert`
- `insertmany`
- `fetchone`
- `fetchall`
- `fetchfirst`
- `delete`
- `update`

#### What to do here
- Make database queries
- Handle conversion from `ORM` to `DTO` types
#### What not to do here
- Declare endpoints
- Interact with other `DAOs`
- Handle business logic


### `endpoints` folder
This folder contains all the Flask Blueprints for your API.
Each blueprint should have its own file.

#### What to do here
- Declare blueprints
- Declare endpoints
- Input parsing / validation
#### What not to do here
- Handle business logic
- Access the database


### `migrations` folder
This folder contains all the migration scripts (in SQL) for your database.
Filenames must start with the current date (YYYYMMDD) to preserve order.

**Important:**
All database updates _must_ be explicitly written here.
This is how we keep track of the database's state.
**Do not ever** make changes to production databases without writing the scripts here first.


### `models` folder
This folder contains all the models used in your API.

There are three types of models:
- `DTO` (Data Transfer Object)
  - Ex: `UserDTO`
  - Contains all information about a certain model
  - Passed around internally
  - Inherits from `BaseDTO`
- `ORM` (Object Relational Mapping)
  - Ex: `UserORM`
  - Maps directly to the columns of a database table
  - Used only in the DAO layer
  - Inherits from `BaseORM`
- And, the normal model
  - Ex: `User`
  - This is the model that is sent out in API responses
  - Contains some or all of the same information that a `DTO` has
    - But may omit some fields because they contain sensitive or irrelevant data (ex: birthday)

`ORM` models also come with a method, `to_dto()`.
This is used by `DAOs` to convert from `ORMs` to `DTOs`.
`BaseORM` provides a built-in method for it which maps fields between `DTO` and `ORM` 1:1.
However, more complex models (ex: models with foreign keys involved) may require override methods.

#### What to do here
- Initialize and make calls to `DAOs`
- Process data
#### What not to do here
- Access the database directly
- Declare endpoints
- Parse HTTP request data


### `services` folder
This folder contains all the business logic for your API.
Each domain should have its own file.

#### What to do here
- Initialize and make calls to `DAOs`
- Initialize and make calls to `clients`
- Initialize and make calls to other `services` **only when truly necessary**
- Process data
#### What not to do here
- Access the database directly
- Declare endpoints
- Parse HTTP request data
