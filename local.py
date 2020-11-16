from git import *

# def main():
repo = Repo('./repos/react')

commits = list(repo.iter_commits('master', max_count=100))
c = None

for commit in commits:
	print(commit.author.email)
	c = commit

# if __name__ == '__main__':
# 	main()
