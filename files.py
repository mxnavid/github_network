import os

# Get all files and files within subfolders in directory
def get_files(folder):
	files = []

	for (dirpath, dirnames, filenames) in os.walk(folder):
		files += [os.path.join(dirpath, file) for file in filenames]

	return files

# Get the file extension for a full path filename string
def file_extension(filename):
	path_list = filename.split('/')
	file = path_list[-1]
	return file.split('.')[-1]

# Aggregate counts of file extensions in files list
def get_extension_count_dict(files):
	extensions = {}

	for file in files:
		ext = file_extension(file)

		if ext not in extensions:
			extensions[ext] = 1
		else:
			extensions[ext] += 1

	return extensions

# Prepare JSON response
def json_resp(extensions):
	data = []
	m = 0

	for ext, count in extensions.items():
		if count > 3:
			data.append({
				'Country': ext,
				'Value': count
				})

			m = max(m, count)

	return {'data': data, 'max': m}

def ext_resp(folder):
	# folder = 'react'
	repo = './repos/'+folder
	files = get_files(repo)
	extensions = get_extension_count_dict(files)
	return json_resp(extensions)

def main():
	folder = 'vscode'
	repo = './repos/'+folder
	files = get_files(repo)

	extensions = get_extension_count_dict(files)

if __name__ == '__main__':
	main()


