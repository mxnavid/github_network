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

def authors_resp():
	folder = 'vscode'
	commits = get_commit_data(folder)
	authors = get_authors_dict(commits)
	return generate_authors_json(authors)

def main():
	folder = 'react'
	commits = get_commit_data(folder)
	authors = get_authors_dict(commits)
	d =generate_authors_json(authors)
	print(d)

if __name__ == '__main__':
	main()
