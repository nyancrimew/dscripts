import requests
import json
from datetime import datetime
from flask import Flask, jsonify, request, render_template, Response
from collections import namedtuple, OrderedDict

DATEFORMAT = '%Y-%m-%d'

app = Flask(__name__)

@app.route('/dynchangelog')
def getChangelog():
    if 'gerrit_url' in request.args:
        gerrit_url = request.args.get('gerrit_url')
    else:
        return 'ERROR: <code>gerrit_url</code> parameter has to be specified', 400
    if 'from' in request.args:
        try:
            from_date = datetime.utcfromtimestamp(int(request.args.get('from'))).strftime(DATEFORMAT)
        except Exception:
            return 'ERROR: <code>from</code> parameter expected to be a unix timestamp', 400
    else:
        return 'ERROR: <code>from</code> parameter has to be specified', 400
    if 'to' in request.args:
        try:
            to_date = datetime.utcfromtimestamp(int(request.args.get('to'))).strftime(DATEFORMAT)
        except Exception:
            return 'ERROR: <code>to</code> parameter expected to be a unix timestamp', 400
    else:
        to_date = datetime.utcnow().strftime(DATEFORMAT)

    if 'filter' in request.args:
        projects_filter = request.args.get('filter')
        url = f'{gerrit_url}/changes/?q=is:merged+projects:{projects_filter}+since:{from_date}+until:{to_date}'
    else:
        url = f'{gerrit_url}/changes/?q=is:merged+since:{from_date}+until:{to_date}'

    r = requests.get(url)
    data = r.text[5:-1] # fuck gerrit xss protection
    commits = json.loads(data)
    changelog = []
    for commit in commits:
        changelog.append(commit['subject'])
    
    # Remove duplicate entries
    changelog = list(OrderedDict.fromkeys(changelog))
    return Response('\n'.join(changelog), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='6988')