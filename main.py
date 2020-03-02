import os
import random

import slack
from dotenv import load_dotenv

def get_students(filepath: str = './students.csv') -> list:
	"""Get the list of the students, returns a list
	
	Keyword Arguments:
		filepath {str} -- the path of the csv file (default: {'./students.csv'})
	
	Returns:
		list -- list of students
	"""	
	with open(filepath) as file:
		return file.readlines()

def generate_groups(nstudents: int = 2) -> dict: # change the number of nstudents if we don't want binoms anymore
	"""Generate the groups

	Keyword Arguments:
		nstudents {int} -- the number of students we want per group (default: {2})
	
	Returns:
		dict -- dictionary with key => group, value => list of student for this group
	"""	
	groups = {}
	students = get_students()
	num_groups = len(students) // nstudents
	for group in range(num_groups):
		students_in_group = []
		for _ in range(nstudents):
			student_key = random.choice(range(len(students)))
			students_in_group.append(students[student_key].replace('\n', ''))
			students.pop(student_key)
		groups[f"Group {group + 1}"] = students_in_group # +1 because arrays start at 0
	
	if len(students) != 0: # if they are student(s) left
		groups[f"Group {num_groups + 1}"] = students

	return groups

def generate_message() -> str:
	"""Generate the message to send
	
	Returns:
		str -- returns the message
	"""	
	msg = ''
	for group, students in generate_groups().items():
		students = '\n'.join(students)
		msg += f'\n*{group}:*\n{students}'
	return msg

def main():
	load_dotenv() # load the token in the env variables
	client = slack.WebClient(token=os.environ.get('SLACK_API_TOKEN'))

	client.chat_postMessage(
		channel='CUPM7PLAG',
		text=generate_message()
	)

if __name__ == '__main__':
	main()
