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

def update_williamson(refs):
    changed = False
    for r in refs:
        if r['author'] == 'williamson t':
            title = r['title']
            if 'knowledge' in title and 'limits' in title:
                year = '2000'
                title = 'knowledge and its limits'
            elif 'philosophy of philosophy' in title:
                year = '2007'
                title = 'the philosophy of philosophy'
            elif title.startswith('vagueness'):
                year = '1994'
                title = 'vagueness'
            if title != r['title']:
                print 'updating %s %s' % (r['title'], r['year'])
                r['year'] = year
                r['title'] = title
                changed = True
    return changed

def update_lewis(refs):
    changed = False
    for r in refs:
        if r['author'] == 'lewis dk':
            title = r['title']
            if title.startswith('convention'):
                year = '1969'
                title = 'convention'
            if title.startswith('counterfactuals'):
                year = '1973'
                title = 'counterfactuals'
            elif 'plurality' in title and 'worlds' in title:
                year = '1986'
                title = 'on the plurality of worlds'
            elif 'philos papers' in title:
                title = title.replace('philos papers', 'philosophical papers')
            if title != r['title']:
                print 'updating %s %s' % (r['title'], r['year'])
                r['year'] = year
                r['title'] = title
                changed = True
    return changed

def update_quine(refs):
    changed = False
    for r in refs:
        if r['author'] == 'quine wvo':
            title = r['title']
            if 'two dogmas' in title:
                year = '1951'
                title = 'philosophical review - two dogmas of empiricism'
            if 'methods' in title and 'logic' in title:
                year = '1950'
                title = 'methods of logic'
            if 'logical' in title and 'point' in title and ' v' in title:
                year = '1953'
                title = 'from a logical point of view'
            if 'word' in title and 'object' in title:
                year = '1960'
                title = 'word and object'
            if 'ways' in title and 'paradox' in title:
                year = '1966'
                title = 'ways of paradox'
            elif 'ontological' in title and 'relativ' in title:
                year = '1969'
                title = 'ontological relativity and other essays'
            elif 'roots' in title and 'reference' in title:
                year = '1974'
                title = 'roots of reference'
            elif 'theories' in title and 'things' in title:
                year = '1981'
                title = 'theories and things'
            elif 'philosophy of logic' in title or 'philos logic' in title or 'philosophy logic' in title:
                year = '1970'
                title = 'philosophy of logic'
            if title != r['title']:
                print 'updating %s %s' % (r['title'], r['year'])
                r['year'] = year
                r['title'] = title
                changed = True
    return changed
