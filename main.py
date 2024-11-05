import json
import datetime

command_list = [
    'task-cli list [...status]',
    'task-cli add [...description]',
    'task-cli update [id] [...description]',
    'task-cli delete [id]',
    'task-cli mark-in-progress [id]',
    'task-cli mark-done [id]',
    'task-cli exit',
]

def main(start):
    if start == True:
        print('Welcome to Task CLI, here is your command:')

    for i in command_list:
        print(i)
    
    print('\n\n')

    inputStr = input('Input your command:\n')
    print('\n\n')

    command = inputStr.split(" ")

    if command[0] != 'task-cli':
        print('ERROR: INVALID COMMAND\n\n')
        main(False)
        return

    match command[1]:
        case 'list':
            get_task_list(command)
        case 'add':
            add_task(command)
        case 'update':
            update_task(command)
        case 'delete':
            delete_task(command)
        case 'mark-in-progress':
            mark_task_in_progress(command[2])
        case 'mark-done':
            mark_task_done(command[2])
        case 'exit':
            return
        case _:
            print('ERROR: INVALID COMMAND')
            main(False)

def openFile():
    try:
        with open('tasks.json') as file:
            return json.load(file)
    except FileNotFoundError:
        with open('tasks.json', 'w+') as f:
            json.dump([], f, indent=4)
        return []

def findIndex(array, id):
    for i in range(len(array)):
        if array[i]['id'] == id:
            return i
    return -1

def saveFile(tasks):
    with open('tasks.json', 'w') as f:
        ordered_list = sorted(tasks, key=lambda task: task['id'])
        json.dump(ordered_list, f, indent=4)

def confirmExit(text):
    confirm = input('\n' + text + '. Exit? (yes/no, y/n) ')
    while confirm.lower() not in ['y', 'yes', 'no', 'n']:
        confirm = input('Exit? (yes/no, y/n) ')
    if confirm.lower() == 'y' or confirm.lower() == 'yes':
        print('\n\n')
        return
    else:
        print('\n\n')
        main(False)
        return

def get_task_list(command):
    status = ''
    if len(command) > 2:
        status = ' '.join(command[2:])
        print('Showing tasks with status "'+ status + '" : ')

    tasks = openFile()
    
    for i in range(len(tasks)):
        if status in tasks[i]['status'].lower():
            print('ID: ' + str(tasks[i]['id']))
            print('Description: ' + tasks[i]['description'])
            print('status: ' + tasks[i]['status'])
            print('created at: ' + tasks[i]['createdAt'])
            print('updated at: ' + tasks[i]['updatedAt'])
            print('\n')
    
    confirmExit('')
    

def add_task(command):
    tasks = openFile()
    id = -1
    for i in range(len(tasks)):
        if tasks[i]['id'] != i:
            id = i
    if id == -1:
        id = len(tasks)
    new_task = {
        'id': id,
        'description': ' '.join(command[2:]),
        'status': 'todo',
        'createdAt': datetime.datetime.now().isoformat(),
        'updatedAt': datetime.datetime.now().isoformat()
    }
    tasks.append(new_task)
    
    saveFile(tasks)

    confirmExit('Success Add Task')
    


def update_task(command):
    if len(command) < 3:
        print('ERROR: INVALID ARGUMENT LENGTH')
        print('RETURNING TO MAIN')
        main(False)
        return
    tasks = openFile()
    if not command[2].isdigit():
        confirmExit('ID is not number')
        
    i = findIndex(tasks, int(command[2]))
    if i == -1:
        confirmExit('Task Not Found')
        return

    task = tasks[i]
    task['description'] = ' '.join(command[3:])
    task['updatedAt'] = datetime.datetime.now().isoformat()
    tasks[i] = task

    saveFile(tasks)

    confirmExit('Success Update Task')


def delete_task(command):
    tasks = openFile()
    if not command[2].isdigit():
        confirmExit('ID is not number')
        
    i = findIndex(tasks, int(command[2]))
    if i == -1:
        confirmExit('Task Not Found')
        return

    tasks.pop(i)

    saveFile(tasks)

    confirmExit('Success Delete Task')




def mark_task_in_progress(id):
    tasks = openFile()
    if not id.isdigit():
        confirmExit('ID is not number')

    i = findIndex(tasks, int(id))
    if i == -1:
        confirmExit('Task Not Found')
        return

    task = tasks[i]
    task['status'] = 'in progress'
    task['updatedAt'] = datetime.datetime.now().isoformat()
    tasks[i] = task

    saveFile(tasks)

    confirmExit('Success Mark Task In Progress')

def mark_task_done(id):
    tasks = openFile()
    if not id.isdigit():
        confirmExit('ID is not number')
        
    i = findIndex(tasks, int(id))
    if i == -1:
        confirmExit('Task Not Found')
        return

    task = tasks[i]
    task['status'] = 'done'
    task['updatedAt'] = datetime.datetime.now().isoformat()
    tasks[i] = task

    saveFile(tasks)

    confirmExit('Success Mark Task Done')
    
if __name__ == "__main__":
    main(True)
    print('Thank you using task-cli!')