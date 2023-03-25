"""Defines all the functions related to the database"""
from typing import List, Dict, Any

from app import db
from sqlalchemy import sql


def fetch_todo() -> List[Dict[str, Any]]:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    with db.connect() as conn:
        query_results = conn.execute(sql.text("select * from tasks order by id")).fetchall()

    todo_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "task": result[1],
            "status": result[2]
        }
        todo_list.append(item)

    return todo_list


def update_task_entry(task_id: int, text: str) -> None:
    """Updates task description based on given `task_id`

    Args:
        task_id (int): Targeted task_id
        text (str): Updated description

    Returns:
        None
    """

    with db.connect() as conn:
        stmt = sql.text("update tasks set task = :task where id = :task_id")
        conn.execute(stmt.bindparams(task=text, task_id=task_id))


def update_status_entry(task_id: int, text: str) -> None:
    """Updates task status based on given `task_id`

    Args:
        task_id (int): Targeted task_id
        text (str): Updated status

    Returns:
        None
    """

    with db.connect() as conn:
        stmt = sql.text("update tasks set status = :status where id = :task_id")
        conn.execute(stmt.bindparams(status=text, task_id=task_id))


def insert_new_task(text: str) -> int:
    """Insert new task to todo table.

    Args:
        text (str): Task description

    Returns: The task ID for the inserted entry
    """

    with db.connect() as conn:
        stmt = sql.text("insert into tasks (task, status) values (:task, :status) returning id")
        query_result = conn.execute(stmt.bindparams(task=text, status="Todo"))
        query_result = [row for row in query_result]
        task_id = query_result[0][0]

    return task_id


def remove_task_by_id(task_id: int) -> None:
    """ remove entries based on task ID """
    with db.connect() as conn:
        stmt = sql.text("delete from tasks where id = :task_id")
        conn.execute(stmt.bindparams(task_id=task_id))
