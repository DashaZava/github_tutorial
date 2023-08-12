import datetime


def get_birthdays_per_week(users):
    days_of_week = ['Monday', 'Tuesday', 'Wednesday',
                    'Thursday', 'Friday', 'Saturday', 'Sunday']
    today = datetime.datetime.now().date()
    week_start = today - datetime.timedelta(days=today.weekday())

    for day in range(7):
        current_day = week_start + datetime.timedelta(days=day)
        day_name = days_of_week[day]
        birthdays = [user['name']
                     for user in users if user['birthday'].date() == current_day]

        if birthdays:
            print(f"{day_name}: {', '.join(birthdays)}")


# Приклад тестового списку users
test_users = [
    {'name': 'Alice', 'birthday': datetime.datetime(2000, 8, 9)},
    {'name': 'Bob', 'birthday': datetime.datetime(1985, 8, 12)},
    {'name': 'Charlie', 'birthday': datetime.datetime(1995, 8, 14)},
    {'name': 'David', 'birthday': datetime.datetime(1990, 8, 16)},
    {'name': 'Eve', 'birthday': datetime.datetime(1978, 8, 18)}
]

get_birthdays_per_week(test_users)
