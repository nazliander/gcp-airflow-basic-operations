import os

# Do not use the SQLite on testing
os.environ['AIRFLOW__CORE__UNIT_TEST_MODE'] = 'True'
