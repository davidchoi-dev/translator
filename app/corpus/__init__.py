import hashlib
import json
from datetime import datetime

from flask import Blueprint, jsonify, request

from app.corpus.models import Corpus, Translation


corpus_module = Blueprint('corpus', __name__, template_folder='templates')


@corpus_module.route('/match')
def corpus_match():

    query = request.args.get('q', '')
    source_lang = request.args.get('sl', None)
    target_lang = request.args.get('tl', None)

    matches = Corpus.match(query, source_lang, target_lang)

    return json.dumps(map(lambda x: x.serialize(), matches))


@corpus_module.route('/raw', methods=['POST'])
def corpus_raw():
    """Collects raw corpus data."""

    raw, source_lang, target_lang = \
        map(lambda x: request.form[x], ('raw', 'sl', 'tl'))

    # Unicode-objects must be encoded before hashing
    hash = hashlib.sha1(raw.encode('utf-8')).hexdigest()

    parsed = json.loads(raw)

    translation = Translation(
        timestamp=datetime.now(),
        hash=hash,
        raw=json.dumps(parsed, ensure_ascii=False),
        source_lang=source_lang,
        target_lang=target_lang)

    return jsonify(translation.save())
