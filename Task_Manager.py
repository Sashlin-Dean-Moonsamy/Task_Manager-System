# Import Modules
import mysql.connector
import datetime

# Initialize global variables
db = mysql.connector.connect(
    host="localhost",
    user="versifire",
    passwd="RiddleMeThis?",
    database="task_manager"
)

admin = False
username = ""

cursor = db.cursor()

cursor.execute("SELECT username FROM users")
users = cursor.fetchall()
all_users = [str(value).strip("(),'") for value in users]


# Define a login function
def login():

    # Call global variables
    global username
    global admin

# Create Try Except for defensive programming
    try:

        # Receive input from user
        username = str(input("\n\t\tLogin\n\nUsername: ")).strip()
        password = str(input("Password: "))

        # Get data from database
        cursor.execute(f"SELECT * FROM users WHERE username='{username}'")
        results = cursor.fetchone()

        # If user is admin change boolean
        if results[0] == "admin":
            admin = True

        # If password entered matches password from database and print welcome message
        if results[-1] == password:

            print("\n\t\tWelcome !")

        # Else print error message to user
        else:
            print("\nIncorrect Password Please Try Again! ")
            login()

    # If a TypeError is found return appropriate error message and call login function again
    except TypeError:
        print("\n This User Does Not Exists!")
        login()


# Create function to get int values from user
def get_num(request):
    while True:

        # Add a try except for defensive programming
        try:
            answer = int(input(request))
            return answer

        except ValueError:
            print("\n\t\tYou Have Not Entered A Number! Please Try Again.")


# Create function to allow the admin to register a new user
def reg_user():

    # Call global variables
    global users

    # Request information from user and save in variable
    print("\n\t\tRegister A User:\n(Fill In The New User's Information Below)")
    new_user = input("\nUsername: ").strip()

    # If the new user that user enters already exists print out appropriate message and call reg_user()
    if new_user in all_users:
        print("This User Already Exists Please Try Again!")
        reg_user()

    # Get new users password from user
    new_password = input("Password: ")

    # Add information to database, save changes and print out message to user
    cursor.execute(f"INSERT INTO users VALUES(%s,%s)", (new_user, new_password))
    db.commit()
    print("\n\t\tUser Successfully Added")


# Create function that prints out tasks given a list
def print_tasks(tasks):

    # Call global variables and assign variables
    global username
    num = 1

    # Create for loop that prints out tasks in a manor that is easy to read
    for item in tasks:
        print(f"\n\t\tTask {num}"
              f"\nUser: {item[0]}"
              f"\nTask Title: {item[1]}"
              f"\nTask: {item[2]}"
              f"\nDate Assigned: {item[3]}"
              f"\nDue Date: {item[4]}"
              f"\nCompletion: {item[-1]}"
              )
        num += 1


# Create function that allows user to see all tasks
def view_all():

    # Read from database and save in variable
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    # Print out tasks using print_tasks
    print_tasks(tasks)


# Create a function that allows user to add tasks to database
def add_task():

    # Request information from user
    task_user = input("\n\t\tFill In The Following Information\n\nUser Assigned To Task: ")

    # If the user enters a person that is not in the database return an appropriate message
    if task_user not in all_users:
        return "User Does Not Exist"

    # Request information from user
    task_title = input("Task Title: ")
    task = input("Task: ")
    due_date = input("Due Date(YYYY-MM-DD): ")

    # if user enters more than 10 values as date print out appropriate error message
    if len(due_date) != 10:
        print("\nYou Have Entered An Incorrect Date!")
        return add_task()

    # Insert values into database, commit changes to database and print out appropriate message
    cursor.execute(f"INSERT INTO tasks VALUES("
                   f"'{task_user}',"
                   f"'{task_title}',"
                   f" '{task}',"
                   f"'{str(datetime.date.today())}',"
                   f"'{due_date}', 'no')")
    db.commit()
    return "Task Successfully Added"


# Define function that allows user to view all tasks only assigned to them
def view_my():

    # Call global variables
    global username
    global users

    # Read from database and save information in variable
    cursor.execute(f"SELECT * FROM tasks WHERE username='{username}'")
    tasks = cursor.fetchall()

    # print values using print_tasks()
    print_tasks(tasks)

    # Use try except for defensive programming
    try:

        # Get information from user
        task_num = get_num(
            "\n\t\tEnter The Number Of A Task You Wish To Edit Or -1 To Return To The Main Menu\n\nSelection: ")

        # If user enters -1 return appropriate message
        if task_num == -1:
            return "\nNo Tasks Were Edited!\n"

        # Assign chosen task to variable
        task_tuple = tasks[task_num - 1]

        # If the last value of the tuple is yes return appropriate error message
        if task_tuple[-1] == "yes":
            return "\n\t\tTask Could Not Be Edited As It Has Already Been Marked As Complete!"

    # If an index error is found return appropriate message
    except IndexError:
        return "\n\t\tThe Project You Have Chosen Does Not Exists!"

    # Request input from user
    vm_select = input("\nMC - Mark Task As Complete"
                      "\nCU - Change User Assigned To Task"
                      "\nCD - Change Due Date"
                      "\nEX - Return To Main Menu"
                      "\n\nSelection: ")

# If user selects ex return appropriate error message
    if vm_select.casefold() == "ex":
        return "\nNo Tasks Were Edited!\n"

    # If user selects mc
    elif vm_select.casefold() == "mc":

        # update database, commit changes and display appropriate message
        cursor.execute(f"UPDATE tasks"
                       f" SET completion = 'yes'"
                       f" WHERE username= '{task_tuple[0]}' and taskTitle = '{task_tuple[1]}'"
                       )
        db.commit()
        return "Task Successfully Updated"

    # If user enters cu
    elif vm_select.casefold() == "cu":

        # Request information from user and save in variable
        new_user = input(f"Old User: {task_tuple[0]}\nNew User: ")

        # If a registered user is entered update database, commit changes and return appropriate error message
        if new_user in all_users:
            cursor.execute(f"UPDATE tasks"
                           f" SET username = '{new_user}'"
                           f" WHERE username = '{task_tuple[0]}' and taskTitle = '{task_tuple[1]}'"
                           )
            db.commit()

            return "\nTask Was Successfully Updated!"

        return "\nThe User You Have Entered Does Not Exist Therefore This Task Could Not Be Edited!"

    # If user selects cd
    elif vm_select.casefold() == "cd":

        # Request information from user, Update database, Commit changes and Return appropriate error message
        new_due_date = input(f"Old Due Date: {task_tuple[-2]}\nNew Due Date: ")
        cursor.execute("UPDATE tasks"
                       f" SET dueDate = '{new_due_date}'"
                       f" WHERE username = '{task_tuple[0]}' and taskTitle = '{task_tuple[1]}'"
                       )
        db.commit()

        return "\nTask Successfully Updated!"

    # Else return an appropriate error message
    else:
        return "\n\t\tIncorrect Option Entered. PLease Try Again"


# Define a function to generate  a report
def gen_report():

    # Create try except as defensive programming
    try:

        # Read from database and save information in variables
        cursor.execute("SELECT * FROM tasks")
        all_tasks = cursor.fetchall()
        cursor.execute("SELECT * FROM tasks WHERE completion = 'yes'")
        completed_tasks = cursor.fetchall()
        cursor.execute("SELECT * FROM tasks WHERE completion = 'no'")
        incomplete_tasks = cursor.fetchall()
        cursor.execute(f"SELECT * FROM tasks WHERE '{datetime.date.today()}' > dueDate and completion = 'no'")
        overdue_tasks = cursor.fetchall()

        # Insert values into database
        cursor.execute(f"INSERT INTO taskoverview VALUES("
                       f"'{datetime.date.today()}',"
                       f"{len(all_tasks)},"
                       f"{len(completed_tasks)},"
                       f"{len(incomplete_tasks)},"
                       f"{len(overdue_tasks)},"
                       f"{(len(incomplete_tasks) / len(all_tasks)) * 100},"
                       f"{len(overdue_tasks) / len(all_tasks) * 100})"
                       )

        # Create for loop to read from useroverview database
        for value in all_users:

            # Read from database and save information in variables
            cursor.execute(f"SELECT * FROM tasks WHERE username = '{value}'")
            user_tasks = cursor.fetchall()
            cursor.execute(f"SELECT * FROM tasks WHERE username = '{value}' and completion = 'yes'")
            user_tasks_complete = cursor.fetchall()
            cursor.execute(f"SELECT * FROM tasks WHERE username = '{value}' and completion = 'no'")
            user_tasks_incomplete = cursor.fetchall()
            cursor.execute(f"SELECT * FROM tasks WHERE username = '{value}' and '{datetime.date.today()}' > dueDate ")
            user_tasks_overdue = cursor.fetchall()

            # Insert variables into database
            cursor.execute("INSERT INTO useroverview VALUES("
                           f"'{datetime.date.today()}',"
                           f"'{value}',"
                           f"{len(user_tasks)},"
                           f"{len(user_tasks) / len(all_tasks) * 100},"
                           f"{len(user_tasks_complete) / len(user_tasks) * 100},"
                           f"{len(user_tasks_incomplete) / len(user_tasks) * 100},"
                           f"{len(user_tasks_overdue) / len(user_tasks) * 100})"
                           )

        # Commit changes to database and print out appropriate message to user
        db.commit()
        print("\n\n\t\tReport Usefully Generated")

    # If a mysql.connector.errors.IntegrityError is found print out appropriate error message
    except mysql.connector.errors.IntegrityError:
        print("\n\t\tThis Would Be A Duplicate Entry And Has Therefore Been Aborted")


# Create a function that displays statistics to the user
def stats():

    # Read from database and save information in variables
    cursor.execute("SELECT date FROM taskoverview")
    date = str(cursor.fetchone()).strip("(),'")
    cursor.execute("SELECT amountOfTasks FROM taskoverview")
    amount_of_tasks = str(cursor.fetchone()).strip("(),'")
    cursor.execute("SELECT completedTasks FROM taskoverview")
    completed_tasks = str(cursor.fetchone()).strip("(),'")
    cursor.execute("SELECT incompleteTasks from taskoverview")
    incomplete_tasks = str(cursor.fetchone()).strip("(),'")
    cursor.execute("SELECT overdueTasks FROM taskoverview")
    overdue_tasks = str(cursor.fetchone()).strip("(),'")
    cursor.execute("SELECT percentageIncomplete FROM taskoverview")
    percentage_incomplete = str(cursor.fetchone()).strip("(),'")
    cursor.execute("SELECT percentageOverdue FROM taskoverview")
    percentage_overdue = str(cursor.fetchone()).strip("(),'")

    # Print out information to user in an easy to read manor
    print(f"\n\t\tStatistics {date}"
          "\n\nTask Statistics:"
          f"\n\nAmount Of Tasks: {amount_of_tasks}"
          f"\nAmount Of Completed Tasks: {completed_tasks}"
          f"\nAmount Of Incomplete Tasks: {incomplete_tasks}"
          f"\nAmount Of Overdue Tasks: {overdue_tasks}"
          f"\nPercentage Of Incomplete Tasks: {percentage_incomplete}%"
          f"\nPercentage Of Overdue Tasks: {percentage_overdue}%"
          f"\n\nUser Statistics:"
          )

    # Read from database and save information in variable
    cursor.execute(f"SELECT * from useroverview WHERE date= '{date}'")
    user_ov_users = cursor.fetchall()

    # Loop through variable that contains information from database
    for value in user_ov_users:

        # Print out information in an easy to read manor
        print(f"\n\nUser: {value[1]}"
              f"\nAmount Of Tasks Assigned: {value[2]}"
              f"\nPercentage Of All Tasks Assigned To User: {value[3]}%"
              f"\nPercentage Of Users Tasks That Have Been Completed: {value[4]}%"
              f"\nPercentage Of Users Tasks That Are Incomplete: {value[5]}%"
              f"\nPercentage Of Users Tasks That Are Overdue: {value[-1]}%")


# Start main with login function
login()

# Create while loop
while True:

    # If the user logged in is an admin display admin options
    if admin:

        selection = input("\nPlease Select One Of The Following Options:"
                          "\n\nVT - View All Tasks"
                          "\nVM - View My Tasks"
                          "\nRU - Register User"
                          "\nAT - Add A Task"
                          "\nGR - Generate Report"
                          "\nDS - Display Statistics"
                          "\nEX - Exit"
                          "\n\nSelection: "
                          )
    # Else print out base options
    else:

        selection = input("\nPlease Select One Of The Following Options:"
                          "\n\nVT - View All Tasks"
                          "\nVM - View My Tasks"
                          "\nEX - Exit"
                          "\n\nSelection: ")

    # If user selects ex break program
    if selection.casefold() == "ex":
        break

    # Elif admin selects ru call reg_user()
    elif selection.casefold() == "ru" and username == "admin":
        reg_user()

    # Elif user selects vt call view_all() function
    elif selection.casefold() == "vt":
        view_all()

    # if user selects vm print view_my() function
    elif selection.casefold() == "vm":
        print(view_my())

    # If admin selects at call add_task()
    elif selection.casefold() == "at" and username == "admin":
        print(add_task())

    # If admin selects gr call gen_report()
    elif selection.casefold() == "gr" and username == "admin":
        gen_report()

    # If user selects ds call stats()
    elif selection.casefold() == "ds" and username == "admin":
        stats()

    # else print appropriate error message
    else:
        print("\n\n\t\tYou have entered an incorrect option! Please try again!")
