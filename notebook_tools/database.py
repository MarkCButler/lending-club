"""Functions for interacting with the project's sqlite database.

The functions in this module understand the details of the database and provide
an API that hides most of those details from other modules.
"""
from pandas import read_sql_query
from sqlalchemy import create_engine, text

from notebook_tools import DATA_DIR

DATABASE_PATH = DATA_DIR / "lending-club.sqlite"
DATABASE_ENGINE = create_engine(url="sqlite:///" + str(DATABASE_PATH))

SQL_STRINGS = {
    "loan_data": """
        SELECT *
        FROM loan_data;""",
    "loan_metadata": """
        SELECT *
        FROM loan_metadata;""",
}


def get_loan_data():
    """Query the database for the full table of accepted loans.

    Returns:
        Dataframe representing the table of accepted loans
    """
    metadata = get_loan_metadata()
    dtypes = metadata["data type"].to_dict()
    loan_data = _perform_query(query=text(SQL_STRINGS["loan_data"]))
    return loan_data.astype(dtypes)


def get_loan_metadata():
    """Query the database for metadata on the table of accepted loans.

    Returns:
        Dataframe of metadata on the table of accepted loans.  Each row gives metadata
        for one column in the table of accepted loans.  The index is 'column name', and
        the two columns are 'description' and 'data type'.
    """
    metadata = _perform_query(query=text(SQL_STRINGS["loan_metadata"]))
    return metadata.set_index("column name")


def _perform_query(query, params=None):
    """Query the database and return the result as a dataframe.

    Args:
        query:  sqlalchemy.sql.expression.TextClause object representing the SQL
            query
        params:  Dictionary of parameters to bind to the query

    Returns:
        Dataframe corresponding to the query result
    """
    if DATABASE_ENGINE is None:
        raise RuntimeError(
            "Unable to perform database query because the engine is not instantiated."
        )
    with DATABASE_ENGINE.connect() as con:
        return read_sql_query(query, con, params=params)


def create_database(tables):
    """Create a SQLite database and add tables to it.

    Args:
        tables:  Dictionary of tables to create.  Keys are table names and values are
            pandas dataframes that are converted to SQLite tables
    """
    if DATABASE_PATH.exists():
        response = input(
            f"The database {DATABASE_PATH} already exists.  "
            "Do you wish to replace it (yes/no)? "
        )
        if response == "yes":
            _delete_database()
        else:
            print("\nReturning.\n")
            return
    _add_tables(tables)


def _delete_database():
    # pylint: disable-next=global-statement
    global DATABASE_ENGINE
    # Dispose of the engine's underlying connection pool
    DATABASE_ENGINE.dispose()
    # Enable garbage collection by removing the global reference to the engine
    DATABASE_ENGINE = None
    # Delete the database
    DATABASE_PATH.unlink()
    # Create a new engine.
    DATABASE_ENGINE = create_engine(url="sqlite:///" + str(DATABASE_PATH))


def _add_tables(tables):
    if DATABASE_ENGINE is None:
        raise RuntimeError(
            "Unable to add database tables because the engine is not instantiated."
        )
    with DATABASE_ENGINE.connect() as con:
        for name, df in tables.items():
            df.to_sql(name, con=con, index=False)
        con.commit()
