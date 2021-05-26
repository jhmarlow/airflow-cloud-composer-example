import datetime

import pytest
from airflow import DAG

import airflow
#  Use test default test config (can overwrite with airflow/unittests.cfg)
# https://airflow.apache.org/docs/apache-airflow/stable/howto/use-test-config.html
airflow.configuration.load_test_config()


@pytest.fixture
def test_dag():
    return DAG(
        "test_dag",
        default_args={
            "owner": "airflow",
            "start_date": datetime.datetime(2018, 1, 1)},
        schedule_interval=datetime.timedelta(days=1),
    )


pytest_plugins = ["helpers_namespace"]


@pytest.helpers.register
def run_task(task, dag):
    dag.clear()
    task.run(
        start_date=dag.default_args["start_date"],
        end_date=dag.default_args["start_date"],
    )