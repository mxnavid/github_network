from flask import Flask, jsonify, request
from gather import *
import local
import files

app = Flask(__name__)

# Github API contributor data
@app.route('/contributors/<repo>')
def users(repo):
    return jsonify(
        getUsers(f'data/{repo}_contributors.json')
    )

# Aggregate Github repository data
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

# Get commit-level author data
@app.route('/authors')
def authors():
    r = local.authors_resp(request.args['repo'])
    return jsonify(r)

# Repository file extension statistics
@app.route('/extensions')
def extensions():
    e = files.ext_resp(request.args['repo'])
    return jsonify(e)

# Commit-level data over days of the week
@app.route('/weekday_commits')
def weekday_commits():
    e = local.weekday_resp(request.args['repo'])
    return jsonify(e)

# 3d scatter plot of weekday and author commit-level data
@app.route('/author_weekday_3d')
def author_weekday_3d():
    local.author_weekday_3d(request.args['repo'])

    return jsonify({'success': True})

if __name__ == '__main__':
    app.run()
