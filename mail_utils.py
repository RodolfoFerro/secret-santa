from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import shuffle
import smtplib
import yaml
import json
import ssl


def email_meta_loader():
	"""Utility function to load email parameters."""

	with open('_config.yml') as config:
		meta = yaml.load(config, Loader=yaml.FullLoader)

	return meta


def load_emails(emails_path : str):
	"""Utility function to load emails list."""

	with open(emails_path) as emails_file:
		emails = json.load(emails_file)

	return emails


def assign_partner(emails : list):
	"""Utility function to match partners from emails list."""

	if len(emails) < 2:
		raise Exception('List must have at least 2 emails.')
	else:
		people = [p['name'] for p in emails]
		for e in emails:
			while True:
				shuffle(people)
				if people[-1] != e['name']:
					pop = people.pop()
					e['assigned'] = pop
					break

	return emails


def send_email(email, user):
	"""Utility function to send email to a specific user."""

	# Setup email configurations:
	message = MIMEMultipart('alternative')
	message['Subject'] = email['subject']
	message['From'] = email['email']
	message['To'] = user['email']

	# Load email body:
	with open(email['body']) as body:
		html = body.read()

	html = html.format(user['name'], user['assigned'])
	body = MIMEText(html, 'html')
	message.attach(body)

	# Create secure connection with server and send email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
		server.login(email['email'], email['password'])
		server.sendmail(
			email['email'], user['email'], message.as_string()
		)


if __name__ == "__main__":
	email = email_meta_loader()
	emails = load_emails(email['list'])
	assign_partner(emails)
	print(emails)