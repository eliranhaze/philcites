"""
specific data update functions
"""

from copy import copy

def update_names(refs, full = False):
    from names import STDNAMES, normalize_author, normalize_title
    def update_func(r):
        author = r['author']
        r['author'] = normalize_author(author) if full else STDNAMES.get(author, author)
        r['title'] = normalize_title(r['title'])
    return _update(refs, lambda r: True, update_func)

def update_austin(refs):
    def enter_condition(r):
        if r['year']:
            year = int(r['year'])
            return r['author'] == 'austin j' and year > 1900
    def update_func(r):
        title = r['title'].lower()
        if 'juris' not in title and ' law' not in title:
            r['author'] = 'austin jl'
    return _update(refs, enter_condition, update_func)

def update_kripke(refs):
    def enter_condition(r):
        return r['author'] == 'kripke sa'
    def update_func(r):
        year = r['year']
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
        r['year'] = year
        r['title'] = title
    return _update(refs, enter_condition, update_func)

def update_wittgenstein(refs):
    def enter_condition(r):
        return r['author'] == 'wittgenstein l'
    def update_func(r):
        year = r['year']
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
        r['year'] = year
        r['title'] = title
    return _update(refs, enter_condition, update_func)

def update_williamson(refs):
    def enter_condition(r):
        return r['author'] == 'williamson t'
    def update_func(r):
        year = r['year']
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
        r['year'] = year
        r['title'] = title
    return _update(refs, enter_condition, update_func)

def update_lewis(refs):
    def enter_condition(r):
        return r['author'] == 'lewis dk'
    def update_func(r):
        year = r['year']
        title = r['title']
        if title.startswith('convention'):
            year = '1969'
            title = 'convention'
        elif title.startswith('counterfactuals'):
            year = '1973'
            title = 'counterfactuals'
        elif 'plurality' in title and 'worlds' in title:
            year = '1986'
            title = 'on the plurality of worlds'
        elif 'philos papers' in title:
            title = title.replace('philos papers', 'philosophical papers')
        r['year'] = year
        r['title'] = title
    return _update(refs, enter_condition, update_func)

def update_rawls(refs):
    def enter_condition(r):
        return r['author'] == 'rawls jb'
    def update_func(r):
        year = r['year']
        title = r['title']
        if 'theory' in title and 'justice' in title:
            year = '1971'
            title = 'a theory of justice'
        elif 'political' in title and 'liberalism' in title:
            year = '1993'
            title = 'political liberalism'
        r['year'] = year
        r['title'] = title
    return _update(refs, enter_condition, update_func)

def update_quine(refs):
    def enter_condition(r):
        return r['author'] == 'quine wvo'
    def update_func(r):
        year = r['year']
        title = r['title']
        if 'two dogmas' in title:
            year = '1951'
            title = 'philosophical review - two dogmas of empiricism'
        elif 'methods' in title and 'logic' in title:
            year = '1950'
            title = 'methods of logic'
        elif 'logical' in title and 'point' in title and ' v' in title:
            year = '1953'
            title = 'from a logical point of view'
        elif 'word' in title and 'object' in title:
            year = '1960'
            title = 'word and object'
        elif 'ways' in title and 'paradox' in title:
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
        r['year'] = year
        r['title'] = title
    return _update(refs, enter_condition, update_func)

def update_journal_names(refs):
    pass

def _update(refs, enter_condition, update_func):
    changed = False
    for r in refs:
        if enter_condition(r):
            orig = copy(r)
            update_func(r)
            if orig != r:
                print 'updating %s/%s/%s' % (orig['author'], orig['title'][:10], orig['year'])
                changed = True
    return changed
