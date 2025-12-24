def main():
    tasks = []  # List to store tasks as dictionaries: {'task': 'description', 'status': 'Pending'}

    while True:
        print("\nTo-Do List Manager")
        print("==================\n")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Remove Task")
        print("5. Exit\n")

        choice = input("Choose an option (1-5): ").strip()

        if choice == '1':
            task_description = input("\nEnter task description: ").strip()
            if task_description:
                tasks.append({'task': task_description, 'status': 'Pending'})
                print("Task added successfully!")
            else:
                print("Task description cannot be empty.")

        elif choice == '2':
            if not tasks:
                print("\nNo tasks yet. Add some!")
            else:
                print("\nYour Tasks:")
                print("-----------")
                for i, item in enumerate(tasks, start=1):
                    status = item['status']
                    print(f"{i}. {item['task']} [{status}]")

        elif choice == '3':
            if not tasks:
                print("\nNo tasks to mark as completed.")
            else:
                try:
                    print("\nCurrent Tasks:")
                    for i, item in enumerate(tasks, start=1):
                        print(f"{i}. {item['task']} [{item['status']}]")
                    index = int(input("\nEnter task number to mark as completed: ")) - 1
                    if 0 <= index < len(tasks):
                        tasks[index]['status'] = 'Completed'
                        print("Task marked as completed!")
                    else:
                        print("Invalid task number.")
                except ValueError:
                    print("Please enter a valid number.")

        elif choice == '4':
            if not tasks:
                print("\nNo tasks to remove.")
            else:
                try:
                    print("\nCurrent Tasks:")
                    for i, item in enumerate(tasks, start=1):
                        print(f"{i}. {item['task']} [{item['status']}]")
                    index = int(input("\nEnter task number to remove: ")) - 1
                    if 0 <= index < len(tasks):
                        removed = tasks.pop(index)
                        print(f"Removed: {removed['task']}")
                    else:
                        print("Invalid task number.")
                except ValueError:
                    print("Please enter a valid number.")

        elif choice == '5':
            print("\nGoodbye! Stay productive.")
            break

        else:
            print("\nInvalid option. Please choose 1-5.")

if __name__ == "__main__":
    main()