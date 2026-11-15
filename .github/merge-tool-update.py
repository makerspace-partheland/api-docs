"""Übernimmt ausschließlich geprüfte Node-/Ruby-Versionsdaten aus dem zentralen Werkzeugupdater."""
import base64
import json
import os
from pathlib import Path
import re
import subprocess


def api(path):
    return json.loads(subprocess.check_output(['gh', 'api', 'repos/' + repository + '/' + path], text=True))


def content(path, sha):
    return base64.b64decode(api('contents/' + path + '?ref=' + sha)['content']).decode().strip()


repository = os.environ['GITHUB_REPOSITORY']
branch = {'makerspace-partheland/makerspace-partheland.github.io': 'main',
          'makerspace-partheland/api-docs': 'master'}[repository]
pr = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())['pull_request']
bot = os.environ['TOOL_UPDATE_BOT']
if (os.environ['GITHUB_ACTOR'] != bot or pr['user']['login'] != bot
        or pr['head']['repo']['full_name'] != repository or pr['base']['ref'] != branch
        or not pr['head']['ref'].startswith('toolchain/')):
    raise ValueError('Fremder Werkzeug-PR')
head, base = pr['head']['sha'], pr['base']['sha']
if not all(re.fullmatch('[a-f0-9]{40}', value) for value in [head, base]):
    raise ValueError('Ungültiger Prüfstand')
files = api(f'pulls/{pr["number"]}/files?per_page=100')
allowed = {'.node-version', '.ruby-version'} if branch == 'main' else {'.node-version'}
if not files or len(files) != pr['changed_files'] or any(f['filename'] not in allowed or f['status'] != 'modified' for f in files):
    raise ValueError('Der PR enthält andere Änderungen als Werkzeugversionen')
for f in files:
    before, after = content(f['filename'], base), content(f['filename'], head)
    if not all(re.fullmatch(r'[0-9]+(?:\.[0-9]+){0,2}', value) for value in [before, after]):
        raise ValueError('Ungültige Runtimeversion')
    left, right = [tuple(map(int, value.split('.'))) for value in [before, after]]
    if right < left:
        raise ValueError('Ein Downgrade ist nicht zulässig')
    if left[0] != right[0]:
        print('Der Majorwechsel bleibt zur Entscheidung offen.')
        raise SystemExit(0)
live = api(f'pulls/{pr["number"]}')
if (live['state'] != 'open' or live['draft'] or live['user']['login'] != bot
        or live['head']['sha'] != head or live['head']['repo']['full_name'] != repository
        or live['head']['ref'] != pr['head']['ref'] or live['base']['ref'] != branch or live['base']['sha'] != base
        or api('git/ref/heads/' + branch)['object']['sha'] != base):
    raise ValueError('Der geprüfte PR oder sein Ziel wurde verändert')
preview = live.get('merge_commit_sha')
if not isinstance(preview, str) or not re.fullmatch('[a-f0-9]{40}', preview):
    raise ValueError('Der erwartete Mergebaum fehlt')
if api('commits/' + preview)['commit']['tree']['sha'] != api('commits/' + head)['commit']['tree']['sha']:
    raise ValueError('Der PR benötigt eine aktuelle Basis und erneute Prüfung')
subprocess.run(['gh', 'pr', 'merge', str(pr['number']), '--repo', repository, '--squash',
                '--match-head-commit', head, '--subject', 'Geprüfte Werkzeugversionen aktualisiert', '--body', ''], check=True)
merged = api(f'pulls/{pr["number"]}')['merge_commit_sha']
commit = api('commits/' + merged)
if (not commit['commit']['verification']['verified'] or [p['sha'] for p in commit['parents']] != [base]
        or commit['commit']['tree']['sha'] != api('commits/' + head)['commit']['tree']['sha']):
    raise ValueError('Die Integration hat den geprüften Stand verändert')
with open(os.environ['GITHUB_OUTPUT'], 'a') as stream:
    stream.write('sha=' + merged + '\n')
