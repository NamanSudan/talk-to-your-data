Source Code
View the source code on GitHub: https://github.com/vanna-ai/vanna

Basic Usage
Getting an API key
import vanna as vn
api_key = vn.get_api_key('my-email@example.com')
vn.set_api_key(api_key)
Setting the model
vn.set_model('chinook')
Asking a question
vn.ask(question='What are the top 10 artists by sales?')
vn.ask(...) is a convenience wrapper around vn.generate_sql(...), vn.run_sql(...), vn.generate_plotly_code(...), vn.get_plotly_figure(...), and vn.generate_followup_questions(...).

For a runnable notebook where you can ask questions, see here

Training
There are 3 main types of training data that you can add to a model: SQL, DDL, and documentation.

# DDL Statements
vn.train(ddl='CREATE TABLE employees (id INT, name VARCHAR(255), salary INT)')

# Documentation
vn.train(documentation='Our organization\'s definition of sales is the discount price of an item multiplied by the quantity sold.')

# SQL
vn.train(sql='SELECT AVG(salary) FROM employees')
vn.train(...) is a convenience wrapper around vn.add_sql(...), vn.add_ddl(...), and vn.add_documentation(...).

For a runnable notebook where you can train a model, see here

Nomenclature
Prefix	Definition	Examples
vn.set_	Sets the variable for the current session	[vn.set_model(...)][set_model]
[vn.set_api_key(...)][set_api_key]
vn.get_	Performs a read-only operation	[vn.get_model()][get_models]
vn.add_	Adds something to the model	[vn.add_sql(...)][add_sql]
[vn.add_ddl(...)][add_ddl]
vn.generate_	Generates something using AI based on the information in the model	[vn.generate_sql(...)][generate_sql]
[vn.generate_explanation()][generate_explanation]
vn.run_	Runs code (SQL or Plotly)	[vn.run_sql][run_sql]
vn.remove_	Removes something from the model	[vn.remove_training_data][remove_training_data]
vn.update_	Updates something in the model	[vn.update_model_visibility(...)][update_model_visibility]
vn.connect_	Connects to a database	[vn.connect_to_snowflake(...)][connect_to_snowflake]
Permissions
By default when you create a model it is private. You can add members or admins to your model or make it public.

User Role	Public Model	Private Model
Use	Train	Use	Train
Non-Member	✅	❌	❌	❌
Member	✅	❌	✅	❌
Admin	✅	✅	✅	✅
Open-Source and Extending
Vanna.AI is open-source and extensible. If you'd like to use Vanna without the servers, see an example here.

The following is an example of where various functions are implemented in the codebase when using the default "local" version of Vanna. vanna.base.VannaBase is the base class which provides a vanna.base.VannaBase.ask and vanna.base.VannaBase.train function. Those rely on abstract methods which are implemented in the subclasses vanna.openai_chat.OpenAI_Chat and vanna.chromadb_vector.ChromaDB_VectorStore. vanna.openai_chat.OpenAI_Chat uses the OpenAI API to generate SQL and Plotly code. vanna.chromadb_vector.ChromaDB_VectorStore uses ChromaDB to store training data and generate embeddings.

If you want to use Vanna with other LLMs or databases, you can create your own subclass of vanna.base.VannaBase and implement the abstract methods.

ChromaDB_VectorStore
generate_embedding
add_question_sql
add_ddl
add_documentation
get_similar_question_sql
get_related_ddl
get_related_documentation
OpenAI_Chat
get_sql_prompt
submit_prompt
generate_question
generate_plotly_code
VannaBase
ask
train
API Reference
api_key: Optional[str] = None
fig_as_img: bool = False
run_sql: Optional[Callable[[str], pandas.core.frame.DataFrame]] = None
Example

vn.run_sql = lambda sql: pd.read_sql(sql, engine)
Set the SQL to DataFrame function for Vanna.AI. This is used in the [vn.ask(...)][ask] function. Instead of setting this directly you can also use [vn.connect_to_snowflake(...)][connect_to_snowflake] to set this.

def get_api_key(email: str, otp_code: Optional[str] = None) -> str:
Example:

vn.get_api_key(email="my-email@example.com")
Login to the Vanna.AI API.

Arguments:
email (str): The email address to login with.
otp_code (Union[str, None]): The OTP code to login with. If None, an OTP code will be sent to the email address.
Returns:
str: The API key.

def set_api_key(key: str) -> None:
Sets the API key for Vanna.AI.

Example:

api_key = vn.get_api_key(email="my-email@example.com")
vn.set_api_key(api_key)
Arguments:
key (str): The API key.
def get_models() -> List[str]:
Example:

models = vn.get_models()
List the models that the user is a member of.

Returns:
List[str]: A list of model names.

def create_model(model: str, db_type: str) -> bool:
Example:

vn.create_model(model="my-model", db_type="postgres")
Create a new model.

Arguments:
model (str): The name of the model to create.
db_type (str): The type of database to use for the model. This can be "Snowflake", "BigQuery", "Postgres", or anything else.
Returns:
bool: True if the model was created successfully, False otherwise.

def add_user_to_model(model: str, email: str, is_admin: bool) -> bool:
Example:

vn.add_user_to_model(model="my-model", email="user@example.com")
Add a user to an model.

Arguments:
model (str): The name of the model to add the user to.
email (str): The email address of the user to add.
is_admin (bool): Whether or not the user should be an admin.
Returns:
bool: True if the user was added successfully, False otherwise.

def update_model_visibility(public: bool) -> bool:
Example:

vn.update_model_visibility(public=True)
Set the visibility of the current model. If a model is visible, anyone can see it. If it is not visible, only members of the model can see it.

Arguments:
public (bool): Whether or not the model should be publicly visible.
Returns:
bool: True if the model visibility was set successfully, False otherwise.

def set_model(model: str):
Set the models to use for the Vanna.AI API.

Example:

vn.set_model("my-model")
Arguments:
model (str): The name of the model to use.
def add_sql(question: str, sql: str, tag: Optional[str] = 'Manually Trained') -> bool:
Adds a question and its corresponding SQL query to the model's training data. The preferred way to call this is to use [vn.train(sql=...)][train].

Example:

vn.add_sql(
    question="What is the average salary of employees?",
    sql="SELECT AVG(salary) FROM employees"
)
Arguments:
question (str): The question to store.
sql (str): The SQL query to store.
tag (Union[str, None]): A tag to associate with the question and SQL query.
Returns:
bool: True if the question and SQL query were stored successfully, False otherwise.

def add_ddl(ddl: str) -> bool:
Adds a DDL statement to the model's training data

Example:

vn.add_ddl(
    ddl="CREATE TABLE employees (id INT, name VARCHAR(255), salary INT)"
)
Arguments:
ddl (str): The DDL statement to store.
Returns:
bool: True if the DDL statement was stored successfully, False otherwise.

def add_documentation(documentation: str) -> bool:
Adds documentation to the model's training data

Example:

vn.add_documentation(
    documentation="Our organization's definition of sales is the discount price of an item multiplied by the quantity sold."
)
Arguments:
documentation (str): The documentation string to store.
Returns:
bool: True if the documentation string was stored successfully, False otherwise.

@dataclass
class TrainingPlanItem:
TrainingPlanItem(item_type: str, item_group: str, item_name: str, item_value: str)
item_type: str
item_group: str
item_name: str
item_value: str
ITEM_TYPE_SQL = 'sql'
ITEM_TYPE_DDL = 'ddl'
ITEM_TYPE_IS = 'is'
class TrainingPlan:
A class representing a training plan. You can see what's in it, and remove items from it that you don't want trained.

Example:

plan = vn.get_training_plan()

plan.get_summary()
TrainingPlan(plan: List[TrainingPlanItem])
def get_summary(self) -> List[str]:
Example:

plan = vn.get_training_plan()

plan.get_summary()
Get a summary of the training plan.

Returns:
List[str]: A list of strings describing the training plan.

def remove_item(self, item: str):
Example:

plan = vn.get_training_plan()

plan.remove_item("Train on SQL: What is the average salary of employees?")
Remove an item from the training plan.

Arguments:
item (str): The item to remove.
def get_training_plan_postgres(
	filter_databases: Optional[List[str]] = None,
	filter_schemas: Optional[List[str]] = None,
	include_information_schema: bool = False,
	use_historical_queries: bool = True
) -> TrainingPlan:
def get_training_plan_generic(df) -> TrainingPlan:
def get_training_plan_experimental(
	filter_databases: Optional[List[str]] = None,
	filter_schemas: Optional[List[str]] = None,
	include_information_schema: bool = False,
	use_historical_queries: bool = True
) -> TrainingPlan:
EXPERIMENTAL : This method is experimental and may change in future versions.

Get a training plan based on the metadata in the database. Currently this only works for Snowflake.

Example:

plan = vn.get_training_plan_experimental(filter_databases=["employees"], filter_schemas=["public"])

vn.train(plan=plan)
def train(
	question: str = None,
	sql: str = None,
	ddl: str = None,
	documentation: str = None,
	json_file: str = None,
	sql_file: str = None,
	plan: TrainingPlan = None
) -> bool:
Example:

vn.train()
Train Vanna.AI on a question and its corresponding SQL query. If you call it with no arguments, it will check if you connected to a database and it will attempt to train on the metadata of that database. If you call it with the sql argument, it's equivalent to [add_sql()][add_sql]. If you call it with the ddl argument, it's equivalent to [add_ddl()][add_ddl]. If you call it with the documentation argument, it's equivalent to [add_documentation()][add_documentation]. It can also accept a JSON file path or SQL file path to train on a batch of questions and SQL queries or a list of SQL queries respectively. Additionally, you can pass a [TrainingPlan][TrainingPlan] object. Get a training plan with [vn.get_training_plan_experimental()][get_training_plan_experimental].

Arguments:
question (str): The question to train on.
sql (str): The SQL query to train on.
sql_file (str): The SQL file path.
json_file (str): The JSON file path.
ddl (str): The DDL statement.
documentation (str): The documentation to train on.
plan (TrainingPlan): The training plan to train on.
def flag_sql_for_review(
	question: str,
	sql: Optional[str] = None,
	error_msg: Optional[str] = None
) -> bool:
Example:

vn.flag_sql_for_review(question="What is the average salary of employees?")
Flag a question and its corresponding SQL query for review. You can see the tag show up in [vn.get_all_questions()][get_all_questions]

Arguments:
question (str): The question to flag.
sql (str): The SQL query to flag.
error_msg (str): The error message to flag.
Returns:
bool: True if the question and SQL query were flagged successfully, False otherwise.

def remove_sql(question: str) -> bool:
Remove a question and its corresponding SQL query from the model's training data

Example:

vn.remove_sql(question="What is the average salary of employees?")
Arguments:
question (str): The question to remove.
def remove_training_data(id: str) -> bool:
Remove training data from the model

Example:

vn.remove_training_data(id="1-ddl")
Arguments:
id (str): The ID of the training data to remove.
def generate_sql(question: str) -> str:
Example:

vn.generate_sql(question="What is the average salary of employees?")
# SELECT AVG(salary) FROM employees
Generate an SQL query using the Vanna.AI API.

Arguments:
question (str): The question to generate an SQL query for.
Returns:
str or None: The SQL query, or None if an error occurred.

def get_related_training_data(question: str) -> vanna.types.TrainingData:
Example:

training_data = vn.get_related_training_data(question="What is the average salary of employees?")
Get the training data related to a question.

Arguments:
question (str): The question to get related training data for.
Returns:
TrainingData or None: The related training data, or None if an error occurred.

def generate_meta(question: str) -> str:
Example:

vn.generate_meta(question="What tables are in the database?")
# Information about the tables in the database
Generate answers about the metadata of a database using the Vanna.AI API.

Arguments:
question (str): The question to generate an answer for.
Returns:
str or None: The answer, or None if an error occurred.

def generate_followup_questions(question: str, df: pandas.core.frame.DataFrame) -> List[str]:
Example:

vn.generate_followup_questions(question="What is the average salary of employees?", df=df)
# ['What is the average salary of employees in the Sales department?', 'What is the average salary of employees in the Engineering department?', ...]
Generate follow-up questions using the Vanna.AI API.

Arguments:
question (str): The question to generate follow-up questions for.
df (pd.DataFrame): The DataFrame to generate follow-up questions for.
Returns:
List[str] or None: The follow-up questions, or None if an error occurred.

def generate_questions() -> List[str]:
Example:

vn.generate_questions()
# ['What is the average salary of employees?', 'What is the total salary of employees?', ...]
Generate questions using the Vanna.AI API.

Returns:
List[str] or None: The questions, or None if an error occurred.

def ask(
	question: Optional[str] = None,
	print_results: bool = True,
	auto_train: bool = True,
	generate_followups: bool = True
) -> Optional[Tuple[Optional[str], Optional[pandas.core.frame.DataFrame], Optional[plotly.graph_objs._figure.Figure], Optional[List[str]]]]:
Example:

# RECOMMENDED IN A NOTEBOOK:
sql, df, fig, followup_questions = vn.ask()


sql, df, fig, followup_questions = vn.ask(question="What is the average salary of employees?")
# SELECT AVG(salary) FROM employees
Ask a question using the Vanna.AI API. This generates an SQL query, runs it, and returns the results in a dataframe and a Plotly figure. If you set print_results to True, the sql, dataframe, and figure will be output to the screen instead of returned.

Arguments:
question (str): The question to ask. If None, you will be prompted to enter a question.
print_results (bool): Whether to print the SQL query and results.
auto_train (bool): Whether to automatically train the model if the SQL query is incorrect.
generate_followups (bool): Whether to generate follow-up questions.
Returns:
str or None: The SQL query, or None if an error occurred. pd.DataFrame or None: The results of the SQL query, or None if an error occurred. plotly.graph_objs.Figure or None: The Plotly figure, or None if an error occurred. List[str] or None: The follow-up questions, or None if an error occurred.

def generate_plotly_code(
	question: Optional[str],
	sql: Optional[str],
	df: pandas.core.frame.DataFrame,
	chart_instructions: Optional[str] = None
) -> str:
Example:

vn.generate_plotly_code(
    question="What is the average salary of employees?",
    sql="SELECT AVG(salary) FROM employees",
    df=df
)
# fig = px.bar(df, x="name", y="salary")
Generate Plotly code using the Vanna.AI API.

Arguments:
question (str): The question to generate Plotly code for.
sql (str): The SQL query to generate Plotly code for.
df (pd.DataFrame): The dataframe to generate Plotly code for.
chart_instructions (str): Optional instructions for how to plot the chart.
Returns:
str or None: The Plotly code, or None if an error occurred.

def get_plotly_figure(
	plotly_code: str,
	df: pandas.core.frame.DataFrame,
	dark_mode: bool = True
) -> plotly.graph_objs._figure.Figure:
Example:

fig = vn.get_plotly_figure(
    plotly_code="fig = px.bar(df, x='name', y='salary')",
    df=df
)
fig.show()
Get a Plotly figure from a dataframe and Plotly code.

Arguments:
df (pd.DataFrame): The dataframe to use.
plotly_code (str): The Plotly code to use.
Returns:
plotly.graph_objs.Figure: The Plotly figure.

def get_results(cs, default_database: str, sql: str) -> pandas.core.frame.DataFrame:
DEPRECATED. Use vn.run_sql instead. Run the SQL query and return the results as a pandas dataframe. This is just a helper function that does not use the Vanna.AI API.

Arguments:
cs: Snowflake connection cursor.
default_database (str): The default database to use.
sql (str): The SQL query to execute.
Returns:
pd.DataFrame: The results of the SQL query.

def generate_explanation(sql: str) -> str:
Example:

vn.generate_explanation(sql="SELECT * FROM students WHERE name = 'John Doe'")
# 'This query selects all columns from the students table where the name is John Doe.'
Generate an explanation of an SQL query using the Vanna.AI API.

Arguments:
sql (str): The SQL query to generate an explanation for.
Returns:
str or None: The explanation, or None if an error occurred.

def generate_question(sql: str) -> str:
Example:

vn.generate_question(sql="SELECT * FROM students WHERE name = 'John Doe'")
# 'What is the name of the student?'
Generate a question from an SQL query using the Vanna.AI API.

Arguments:
sql (str): The SQL query to generate a question for.
Returns:
str or None: The question, or None if an error occurred.

def get_all_questions() -> pandas.core.frame.DataFrame:
Get a list of questions from the Vanna.AI API.

Example:

questions = vn.get_all_questions()
Returns:
pd.DataFrame or None: The list of questions, or None if an error occurred.

def get_training_data() -> pandas.core.frame.DataFrame:
Get the training data for the current model

Example:

training_data = vn.get_training_data()
Returns:
pd.DataFrame or None: The training data, or None if an error occurred.

def connect_to_sqlite(url: str):
Connect to a SQLite database. This is just a helper function to set [vn.run_sql][run_sql]

Arguments:
url (str): The URL of the database to connect to.
Returns:
None

def connect_to_snowflake(
	account: str,
	username: str,
	password: str,
	database: str,
	schema: Optional[str] = None,
	role: Optional[str] = None
):
Connect to Snowflake using the Snowflake connector. This is just a helper function to set [vn.run_sql][run_sql]

Example:

import snowflake.connector

vn.connect_to_snowflake(
    account="myaccount",
    username="myusername",
    password="mypassword",
    database="mydatabase",
    role="myrole",
)
Arguments:
account (str): The Snowflake account name.
username (str): The Snowflake username.
password (str): The Snowflake password.
database (str): The default database to use.
schema (Union[str, None], optional): The schema to use. Defaults to None.
role (Union[str, None], optional): The role to use. Defaults to None.
def connect_to_postgres(
	host: str = None,
	dbname: str = None,
	user: str = None,
	password: str = None,
	port: int = None
):
Connect to postgres using the psycopg2 connector. This is just a helper function to set [vn.run_sql][run_sql] Example:

import psycopg2.connect
vn.connect_to_bigquery(
    host="myhost",
    dbname="mydatabase",
    user="myuser",
    password="mypassword",
    port=5432
)
Arguments:
host (str): The postgres host.
dbname (str): The postgres database name.
user (str): The postgres user.
password (str): The postgres password.
port (int): The postgres Port.
def connect_to_bigquery(cred_file_path: str = None, project_id: str = None):
Connect to gcs using the bigquery connector. This is just a helper function to set [vn.run_sql][run_sql] Example:

import bigquery.Client
vn.connect_to_bigquery(
    project_id="myprojectid",
    cred_file_path="path/to/credentials.json",
)
Arguments:
project_id (str): The gcs project id.
cred_file_path (str): The gcs credential file path