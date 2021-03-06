import glob
import re

from difflib import SequenceMatcher

from downloader import Downloader
from names import normalize_author, normalize_title, STDNAMES
from utils import pkl

DATA_FOLDER = pkl.DATA_FOLDER
TOP_JOURNALS = ['phil_review', 'mind', 'nous', 'jphil', 'ajp', 'phil_stud', 'ppr']

def download_all(save_every = 100):
    journal_files = glob.glob('%s/.papers_*.pkl' % DATA_FOLDER)
    # init downloader here to avoid reconnecting too often
    downloader = Downloader()
    for jf in journal_files:
        name = re.findall('\.papers_(.*?)\.pkl', jf)[0]
        download_refs(name, save_every = save_every, downloader = downloader)

def download_refs(jname, save_every = 100, downloader = None):
    papers = pkl.load('papers_%s' % jname)
    refs = pkl.load('refs_%s' % jname, [])
    existing_uids = {r['by_uid'] for r in refs}
    papers_to_download = [p for p in papers if p['uid'] not in existing_uids]
    print 'downloading %s: %d out of %d papers' % (jname, len(papers_to_download), len(papers))
    d = downloader if downloader else Downloader()
    for i, chunk in enumerate(chunks(papers_to_download, save_every)):
        print ' -- chunk #%d -- ' % (i + 1)
        chunk_refs = d.download_papers_refs(chunk)
        if chunk_refs: # avoid writing to file unnecessarily
            refs.extend(chunk_refs)
            pkl.save(refs, 'refs_%s' % jname)

def update_refs_data(update_func, *args, **kw):
    ref_files = glob.glob('%s/.refs_*.pkl' % DATA_FOLDER)
    for rf in ref_files:
        name = re.findall('\.(.*?)\.pkl', rf)[0]
        print 'loading %s' % name
        refs = pkl.load(name)
        print 'updating %s' % name
        changed = update_func(refs, *args, **kw)
        if changed:
            print 'saving %s' % name
            pkl.save(refs, name)

def update_refs_data_all():
    import updates
    for func in dir(updates):
        if func.startswith('update_'):
            print ' -- running %s -- ' % func
            update_refs_data(getattr(updates, func))

def load_refs(journals = TOP_JOURNALS):
    refs = []
    for j in journals:
        refs.extend(pkl.load('refs_%s' % j))
    return refs

def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in xrange(0, len(l), n))

def similarity(a, b):
    """" return degree (0-1) of similarity between two strings """
    return SequenceMatcher(None, a, b).ratio()
