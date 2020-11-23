from git import *

# Use PythonGit to retreive commit history data
def get_commit_data(folder, count=10000):
	repo = Repo('./repos/'+folder)
	return list(repo.iter_commits('master', max_count=count))

# Filter all authors to only most active
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

# Generate commit-level author dara
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

# Prepare authors data JSON response
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

# Aggregate commit level data over days of the week
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

# Prepare weekday commit-level data JSON response
def author_weekday_dict(commits):
	authors = []
	hours = []
	weekdays = []
	count = []

	for commit in commits:
		author = commit.author.name
		hour = commit.committed_datetime.hour
		weekday = commit.committed_datetime.strftime('%A')

		authors.append(author)
		hours.append(hour)
		weekdays.append(weekday)
		count.append(abs(hour - 15))

	return {'authors': authors, 'hours': hours, 'weekdays': weekdays, 'count': count}

# Generate plotly 3D scatter plot
def threeD_dict(commits):
	dct = author_weekday_dict(commits)
	import plotly.express as px
	import pandas as pd
	fig = px.scatter_3d(pd.DataFrame.from_dict(dct), x='authors', y='hours', z='weekdays', color='count')
	fig.show()

# Run 3d scatter plot
def author_weekday_3d(folder):
	commits = get_commit_data(folder, 1000)
	threeD_dict(commits)

# Return weekday commit-level data
def weekday_resp(folder):
	commits = get_commit_data(folder)
	return per_day_commits(commits)

# Return author commit-level data
def authors_resp(folder):
	commits = get_commit_data(folder)
	authors = get_authors_dict(commits)
	return generate_authors_json(authors)

def main():
	folder = 'react'
	commits = get_commit_data(folder, 1000)
	threeD_dict(commits)

if __name__ == '__main__':
	main()
