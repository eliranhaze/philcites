"""
specific data update functions
"""

def update_austin(refs):
    changed = False
    for r in refs:
        year = int(r['year'])
        if r['author'] == 'austin j' and year > 1900 and 'juris' not in r['title'].lower():
            print 'updating', r['title'], year
            r['author'] = 'austin jl'
            changed = True
    return changed

def update_kripke(refs):
    changed = False
    for r in refs:
        if r['author'] == 'kripke sa':
            title = r['title']
            if 'wittgenst' in title and ('rule' in title or 'private' in title):
                year = '1982'
                title = 'wittgenstein on rules and private language'
            elif 'semantics' in title and 'natural' in title:
                year = '1972'
                title = 'semantics of natural language - naming and necessity'
            elif 'naming' in title and 'necessity' in title:
                year = '1980'
                title = 'naming and necessity'
            if title != r['title']:
                print 'updating %s %s' % (r['title'], r['year'])
                r['year'] = year
                r['title'] = title
                changed = True
    return changed

def update_wittgenstein(refs):
    changed = False
    for r in refs:
        if r['author'] == 'wittgenstein l':
            title = r['title']
            if 'tractatus' in title:
                year = '1922'
                title = 'tractatus'
            elif ('philos' in title and 'invest' in title) or 'philosophical inv' in title:
                year = '1953'
                title = 'philosophical investigations'
            elif ('blue' in title and 'brown' in title) or 'blue book' in title:
                year = '1958'
                title = 'blue and brown books'
            elif 'certainty' in title:
                year = '1969'
                title = 'on certainty'
            elif 'zettel' in title:
                year = '1967'
                title = 'zettel'
            if title != r['title']:
                print 'updating %s %s' % (r['title'], r['year'])
                r['year'] = year
                r['title'] = title
                changed = True
    return changed

