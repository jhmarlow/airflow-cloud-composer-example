import logging
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

dag = DAG(
    'excom_xample',
    schedule_interval="@once",
    start_date=days_ago(2),
    default_args={'owner': 'airflow'},
    tags=['example'],
    catchup=False
)

value_1 = [1, 2, 3]
value_2 = {'a': 'b'}


def push(**kwargs):
    """Pushes an XCom without a specific target"""
    logging.info("log before PUSH")  # <<<<<<<<<<< Before landing on breakpoint
    kwargs['ti'].xcom_push(key='value from pusher 1', value=value_1)


def push_by_returning(**kwargs):
    """Pushes an XCom without a specific target, just by returning it"""
    return value_2


def puller(**kwargs):
    """Pull all previously pushed XComs and
        check if the pushed values match the pulled values."""
    ti = kwargs['ti']

    # get value_1
    pulled_value_1 = ti.xcom_pull(key=None, task_ids='push')
    

    print("PRINT Line after breakpoint ")  # <<<< After landing on breakpoint
    if pulled_value_1 != value_1:
        raise ValueError("The two values differ"
                         f"{pulled_value_1} and {value_1}")
    import pdb
    pdb.set_trace()
    # get value_2
    pulled_value_2 = ti.xcom_pull(task_ids='push_by_returning')
    if pulled_value_2 != value_2:
        raise ValueError(
            f'The two values differ {pulled_value_2} and {value_2}')

    # get both value_1 and value_2
    pulled_value_1, pulled_value_2 = ti.xcom_pull(
        key=None, task_ids=['push', 'push_by_returning'])
    if pulled_value_1 != value_1:
        raise ValueError(
            f'The two values differ {pulled_value_1} and {value_1}')
    if pulled_value_2 != value_2:
        raise ValueError(
            f'The two values differ {pulled_value_2} and {value_2}')


push1 = PythonOperator(
    task_id='push',
    dag=dag,
    python_callable=push,
)

push2 = PythonOperator(
    task_id='push_by_returning',
    dag=dag,
    python_callable=push_by_returning,
)

pull = PythonOperator(
    task_id='puller',
    dag=dag,
    python_callable=puller,
)

pull << [push1, push2]

if __name__ == '__main__':
    from airflow.utils.state import State
    dag.clear(dag_run_state=State.NONE)
    dag.run()
