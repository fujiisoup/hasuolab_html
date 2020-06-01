"""
Find details of papers and export as necessary formats
Need to install crossref library,
>>> pip install crossref
"""
from crossref.restful import Works
import numpy as np


def download_details(doi_list):
    works = Works()
    details = []
    for j, doi in enumerate(doi_list):
        doi = doi.strip()
        work = works.doi(doi)
        details.append(standarize(work))
    return details


def get_firstauthor(details, author):
    if isinstance(author, str):
        author = [author]
    author = [au.lower() for au in author]
    firstauthors = []
    for detail in details:
        if detail['author'][0].get('family', None).lower() in author:
            firstauthors.append(detail)
    return firstauthors


def standarize(detail):
    if 'journal-issue' not in detail:
        detail['journal-issue'] = {}
    if 'published-print' not in detail['journal-issue']:
        detail['journal-issue']['published-print'] = {}
        detail['journal-issue']['published-print']['date-parts'] = detail['issued']['date-parts']
    if len(detail['journal-issue']['published-print']['date-parts'][0]) < 2:
        if isinstance(detail['journal-issue']['published-print']['date-parts'][0][0], list):
            detail['journal-issue']['published-print']['date-parts'][0] = detail['journal-issue']['published-print']['date-parts'][0][0]
        if len(detail['journal-issue']['published-print']['date-parts'][0]) == 1:
            detail['journal-issue']['published-print']['date-parts'][0].append(0)  # month not available

    if 'volume' not in detail:
        print(detail)

    for author in detail['author']:
        if 'family' not in author:
            author['family'] = author['name']
        if 'given' not in author:
            author['given'] = ''
    return detail


def sort_by_date(details, newest_first=True):
    dates = []
    for detail in details:
        y = detail['journal-issue']['published-print']['date-parts'][0][0]
        m = detail['journal-issue']['published-print']['date-parts'][0][1]
            
        dates.append(int('{0:d}{1:02d}'.format(y, m)))
    idx = np.argsort(dates)
    if newest_first:
        idx = idx[::-1]
    return [details[i] for i in idx]


def save_markdown(details, outname, author):
    """
    Save as a markdown format
    """
    if isinstance(author, str):
        author = [author]
    author = [au.lower() for au in author]

    details = sort_by_date(details)
    lines = [
        "# List of published papers",
    ]
    for i, detail in enumerate(details):
        lines.append('{}. **{}**  '.format(i + 1, detail['title'][0]))
        authors = ''
        for author in detail['author']:
            if author['family'].lower() in author:
                authors += '__**{} {}**__, '.format(author['given'], author['family'])
            else:
                authors += '{} {}, '.format(author['given'], author['family'])
        lines.append(' {}  '.format(authors[:-2]))  # remove the last comma
        # journal
        articlenumber = detail.get('article-number', detail.get('page'))
        lines.append(' *{}* **{},** {} ({})  \n'.format(
            detail['container-title'][0], 
            detail['volume'],
            articlenumber, 
            detail['journal-issue']['published-print']['date-parts'][0][0]
        ))

    with open(outname, 'w') as f:
        for line in lines:
            f.write(line + '\n')


if __name__ == '__main__':
    with open('_papers.csv', 'r') as f:
        doi_list = f.readlines()
    details = download_details(doi_list)
    with open('dois.txt', 'w') as f:
        for detail in details:
            f.write('{}\n'.format(detail))
    # save_markdown(details, 'papers.md')
    save_html(details, 'papers_all.html', 'all')
    