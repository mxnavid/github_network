from git import *
# import matplotlib.pyplot as plt

def get_commit_data(folder):
	repo = Repo('./repos/'+folder)
	return list(repo.iter_commits('master', max_count=1000))

def filter_authors(authors):
	filtered = {}
	limit = 50

	for author_name in authors.keys():
		total = 0

		for hour in authors[author_name].values():
			total += hour

		if total > limit:
			filtered[author_name] = authors[author_name]

	return filtered

def get_authors_dict(commits):
	hours = [0 for _ in range(24)]
	authors = {}

	for commit in commits:
		if 'github.com' in commit.author.email:
			continue

		# print(commit.author.email)
		name = commit.author.name.replace('å', 'a')
		hour = commit.authored_datetime.hour

		if name not in authors:
			authors[name] = {}
			for h in range(24):
				authors[name][h] = 0
		
		authors[name][hour] += 1

	return filter_authors(authors)

def generate_authors_json(authors):
	data = []
	uniques = []

	for author, values in authors.items():
		# print(author)
		if author not in uniques:
			uniques.append(author)

		for hour in sorted(values.keys()):
			data.append({
				'author': author,
				'hour': hour,
				'count': values[hour]
				})

	hours = [str(_) for _ in range(24)]
	return {'data': data, 'authors': uniques, 'hours': hours}

def per_day_commits(commits):
	weekdays = {}
	
	for commit in commits:
		t = commit.committed_datetime
		weekday = t.strftime('%A')
		hour = t.hour

		if weekday not in weekdays:
			weekdays[weekday] = {}
			for h in range(24):
				weekdays[weekday][h] = 0

		weekdays[weekday][hour] += 1

	data = []
	for weekday, hours in weekdays.items():
		for hour in hours.keys():
			count = hours[hour]
			data.append({
				'author': weekday,
				'hour': hour,
				'count': count
				})

	hours = [str(_) for _ in range(24)]
	return {'data': data, 'hours': hours}

def threeD_dict(commits):
	authors = []
	hours = []
	weekdays = []

	for commit in commits:
		author = commit.author.name
		hour = commit.committed_datetime.hour
		weekday = commit.committed_datetime.strftime('%A')

		authors.append(author)
		hours.append(hour)
		weekdays.append(weekday)

	dct = {'authors': authors, 'hours': hours, 'weekdays': weekdays}

	import plotly.express as px
	import pandas as pd

	fig = px.scatter_3d(pd.DataFrame.from_dict(dct), x='authors', y='hours', z='weekdays', color='hours')
	print(fig.show())

def author_weekday_3d(folder):
	commits = get_commit_data(folder)
	threeD_dict(commits)

def weekday_resp(folder):
	commits = get_commit_data(folder)
	return per_day_commits(commits)

def authors_resp(folder):
	commits = get_commit_data(folder)
	authors = get_authors_dict(commits)
	return generate_authors_json(authors)

def main():
	folder = 'react'
	commits = get_commit_data(folder)
	threeD_dict(commits)

if __name__ == '__main__':
	main()
