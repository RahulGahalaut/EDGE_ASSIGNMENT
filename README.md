steps to run the server:
    1. git clone https://github.com/RahulGahalaut/EDGE_ASSIGNMENT.git
    2. pip install -r requirements.txt
    3. uvicorn main:app --reload

System Specification:
    The system is designed as a Python FastAPI REST service that interacts with a PostgreSQL database. It provides endpoints to store and retrieve data from a table named source_data in the database. The system design follows the client-server architecture, where the FastAPI server acts as the backend that handles HTTP requests and communicates with the PostgreSQL database for data storage and retrieval.

    The system utilises SQLAlchemy as the Object-Relational Mapping (ORM) tool to interact with the database. SQLAlchemy provides an abstraction layer that allows us to define the table schema using Python classes (declarative models) and perform database operations using high-level Python methods.

    The system supports the following endpoints:
        GET /get_data
        Description: Retrieves all the data for a given source from the source_data table.
        Request Field: source_id (integer) - Specifies the source ID to filter the data.
        Response Field: All fields present in the source data row.


        GET /get_data_trigger
        Description: Retrieves the data for a given source from the source_data table, adjusting the from_date and to_date values by adding the frequency.
        Request Field: source_id (integer) - Specifies the source ID to filter the data.
        Response Field: All fields present in the source data row, including adjusted from_date and to_date values.


        PUT /update_data
        Description: Updates the from_date, to_date, and last_update_date values for a given source in the source_data table.
        Request Field: 
        source_id (integer) - Specifies the source ID to update.
        from_date (datetime) - New value for the from_date.
        to_date (datetime) - New value for the to_date.
        last_update_date (datetime) - New value for the last_update_date.
        Response Field: { "status": "success" }


        POST /add_data
        Description: Adds a new record to the source_data table.
        Request Field: Payload containing the following fields:
        source (string) - Name of the source.
        source_type (string) - Type of the source.
        source_tag (string) - Tag for the source.
        last_update_date (datetime) - Last updated timestamp for the source.
        from_date (datetime) - From date.
        to_date (datetime) - To date.
        frequency (string) - Update frequency in minutes.
        Response Field: { "status": "success" }


SQL Script for the Table:

    CREATE TABLE source_data (
        source_id SERIAL PRIMARY KEY,
        source VARCHAR(200),
        source_type VARCHAR(10),
        source_tag VARCHAR(10),
        last_update_date TIMESTAMP,
        from_date TIMESTAMP,
        to_date TIMESTAMP,
        frequency VARCHAR(5)
    );

The source_data table has the following columns:
    source_id (serial, primary key) - ID of the source (automatically generated).
    source (varchar) - Name of the source.
    source_type (varchar) - Type of the source.
    source_tag (varchar) - Tag for the source.
    last_update_date (timestamp) - Last updated timestamp for the source.
    from_date (timestamp) - From date.
    to_date (timestamp) - To date.
    frequency (varchar) - Update frequency in minutes.

Sample Payloads and Specifications:
    GET /get_data
        Sample Request: GET /get_data?source_id=1
        Response Body:
            {
            "source_id": 1,
            "source": "flipkart",
            "source_type": "online",
            "source_tag": "fk",
            "last_update_date": "2023-01-01T00:00:30",
            "from_date": "2023-01-01T00:00:15",
            "to_date": "2023-01-01T00:00:30",
            "frequency": "15M"
            }


    GET /get_data_trigger
        Sample Request: GET /get_data_trigger?source_id=1
        Response Body:
            {
            "source_id": 1,
            "source": "flipkart",
            "source_type": "online",
            "source_tag": "fk",
            "last_update_date": "2023-01-01T00:00:30",
            "from_date": "2023-01-01T00:00:30",
            "to_date": "2023-01-01T00:00:45",
            "frequency": "15M”
            }

    PUT /update_data
        Sample Request:  PUT /update_data/source_id=1
            {
            "from_date": "2023-01-01T00:01:00",
            "to_date": "2023-01-01T00:01:15",
            "last_update_date": "2023-01-01T00:01:30"
            }
        Response Body:
            {
            "status": "success"
            }

    POST /add_data
        Sample Request:  POST /add_data
            {
            "source": "amazon",
            "source_type": "online",
            "source_tag": "amz",
            "last_update_date": "2023-01-02T10:00:00",
            "from_date": "2023-01-02T09:45:00",
            "to_date": "2023-01-02T10:00:00",
            "frequency": "15M"
            }
        Response Body:
            {
            "status": "success"
            }
