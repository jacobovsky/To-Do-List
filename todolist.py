from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
import sys
import datetime

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.datetime.today())


def display_menu(menu_name='main'):
    if menu_name == 'main':
        print("1) Today's tasks\n"
              "2) Week's tasks\n"
              "3) All tasks\n"
              "4) Missed tasks\n"
              "5) Add task\n"
              "6) Delete task\n"
              "0) Exit")


months = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
          7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
day = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
Base.metadata.create_all(engine)
while 1:
    display_menu()
    menu_key = input()
    print()
    if menu_key == '1':
        rows = session.query(Task).filter(Task.deadline == datetime.datetime.today().date()).order_by(Task.deadline).all()
        if rows:
            number_of_displayed_task = 1
            print(f"Today {rows[0].deadline.day} {months[rows[0].deadline.month]}:")
            for row in rows:
                print(f"{number_of_displayed_task}. {row.task}")
                number_of_displayed_task += 1
        else:
            print("Nothing to do!")
        print()
    elif menu_key == '2':
        week_from_today = [datetime.datetime.today() + datetime.timedelta(days=i) for i in range(7)]
        for day_in_week in week_from_today:
            print()
            rows = session.query(Task).filter(Task.deadline == day_in_week.date()).order_by(
                Task.deadline).all()

            print(f"{day[day_in_week.weekday()]} {day_in_week.day} {months[day_in_week.month]}:")
            if rows:
                number_of_displayed_task = 1
                for row in rows:
                    print(f"{number_of_displayed_task}. {row.task}")
                    number_of_displayed_task += 1
            else:
                print("Nothing to do!")
        print()
    elif menu_key == '3':
        rows = session.query(Task).order_by(Task.deadline).all()
        print("All tasks:")
        if rows:
            number_of_displayed_task = 1
            for row in rows:
                print(f"{number_of_displayed_task}. {row.task}. {row.deadline.day} {months[row.deadline.month]}")
                number_of_displayed_task += 1
        else:
            print("Nothing to do!")
        print()
    elif menu_key == '4':
        print("Missed tasks:")
        rows = session.query(Task).filter(Task.deadline < datetime.datetime.today().date()).order_by(Task.deadline).all()
        if rows:
            number_of_displayed_task = 1
            for row in rows:
                print(f"{number_of_displayed_task}. {row.task}. {row.deadline.day} {months[row.deadline.month]}")
                number_of_displayed_task += 1
        else:
            print("Nothing is missed!")
        print()
    elif menu_key == '5':
        # it adds new task to database
        print("Enter task")
        new_task_name = input()

        # it adds deadline to new task
        print("Enter deadline")
        new_task_deadline = input().split(sep='-')
        deadline_date = datetime.datetime(int(new_task_deadline[0]), int(new_task_deadline[1]), int(new_task_deadline[2]))
        print()

        # commit to database
        new_task = Task(task=new_task_name, deadline=deadline_date)
        session.add(new_task)
        session.commit()
    elif menu_key == '6':
        rows = session.query(Task).order_by(Task.deadline).all()
        print("Choose the number of task you want to delete:")
        if rows:
            number_of_displayed_task = 1
            for row in rows:
                print(f"{number_of_displayed_task}. {row.task}. {row.deadline.day} {months[row.deadline.month]}")
                number_of_displayed_task += 1
            task_to_delete = int(input())
            session.delete(rows[task_to_delete - 1])
            session.commit()
            print("The task has been deleted!\n")
        else:
            print("Nothing can be deleted!\n")
    elif menu_key == '0':
        print("Bye!")
        sys.exit()
    else:
        pass
