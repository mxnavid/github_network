from flask import Flask, jsonify, request
from gather import *
import local
import files

# pip install Flask
# export FLASK_APP='app.py'
# flask run

app = Flask(__name__)

# @app.route('/')
# def index():
#     return 'hello, world'

# http://localhost:5000/contributors/react
@app.route('/contributors/<repo>')
def users(repo):
    return jsonify(
        getUsers(f'data/{repo}_contributors.json')
    )

@app.route('/repos')
def repos():
    repos = ['flutter', 'react', 'kubernetes']
    data = []
    for repo in repos:
        r = []
        contributors = getUsers(f'data/{repo}_contributors.json')
        companies = {}
        
        for contributor in contributors:
            company = getCompany(contributor)
            if company not in companies:
                companies[company] = [contributor]
            else:
                companies[company].append(contributor)
                 
            # r.append({
            #     'name': contributor,
            #     'value': 1000
            # })
        
        repo_children = []
        for company, contribs in companies.items():
            contributor_children = []
            for c in contribs:
                contributor_children.append({
                    'name': c,
                    'value': 1000
                })
            
            repo_children.append({
                'name': company,
                'children': contributor_children
            })
        
        r = repo_children
        
        data.append({
            'name': repo,
            'children': r
        })
    
    return jsonify({
        'name': 'repos',
        'children': data
    })

@app.route('/authors')
def authors():
    r = local.authors_resp(request.args['repo'])
    return jsonify(r)

@app.route('/extensions')
def extensions():
    e = files.ext_resp(request.args['repo'])
    return jsonify(e)

@app.route('/weekday_commits')
def weekday_commits():
    e = local.weekday_resp(request.args['repo'])
    return jsonify(e)

@app.route('/author_weekday_3d')
def author_weekday_3d():
    local.author_weekday_3d(request.args['repo'])

if __name__ == '__main__':
    app.run()


