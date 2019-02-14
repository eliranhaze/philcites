import glob
import re

from names import normalize, STDNAMES
from utils import pkl

def download_all():
    from main import Downloader
    ref_files = glob.glob('.papers_*.pkl')
    for rf in ref_files:
        name = re.findall('\.papers_(.*?)\.pkl', rf)[0]
        papers = pkl.load('papers_%s' % name)
        refs = Downloader().download_papers_refs(papers)
        pkl.save(refs, 'refs_%s' % name)

def update_refs_data(update_func, *args, **kw):
    ref_files = glob.glob('.refs_*.pkl')
    for rf in ref_files:
        name = re.findall('\.(.*?)\.pkl', rf)[0]
        print 'loading %s' % name
        refs = pkl.load(name)
        print 'updating %s' % name
        update_func(refs, *args, **kw)
        print 'saving %s' % name
        pkl.save(refs, name)

def renormalize(refs, full = False):
    def _update(refs, full):
        for r in refs:
            author = r['author']
            r['author'] = normalize(author) if full else STDNAMES.get(author, author)
    update_refs_data(_update, full = full)
