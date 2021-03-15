"""
Find details of papers and export as necessary formats
Need to install crossref library,
>>> pip install crossrefapi
"""
from crossref.restful import Works
import numpy as np


def download_details(doi_list, maxcount=None):
    works = Works()
    details = []
    for j, doi in enumerate(doi_list):
        doi = doi.strip()
        if doi[0] == '#':
            continue
        if ',' in doi:
            doi = [d.strip() for d in doi.split(',')][0]

        work = works.doi(doi)
        if work is None:
            print(doi)
            continue
        work['doi'] = doi
        details.append(standarize(work))
        if maxcount is not None and j > maxcount:
            break
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

    if 'container-title' in detail:
        if len(detail['container-title']) == 0:
            print(detail['doi'])
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


HTML_TABLE_HEADER = """<h2 id="{}"> {} </h2>
<TABLE border="0">
<TBODY>"""

HTML_TABLE_FOOTER = """
<TR>
    <TD align="right" style="text-align : right;" width="704" valign="bottom">
    <a href="#top"><img src="img/up_icon.gif" border="0">top</a>
    </TD>
</TR>
</TBODY>
</TABLE>
"""



def save_html(details, outname, author_list):
    """
    Save as a markdown format
    """
    if isinstance(author_list, str):
        author_list = [author_list]
    author_list = [au.lower() for au in author_list]

    details = sort_by_date(details)
    htmls = []

    year = None
    years = []
    count = 0

    for i, detail in enumerate(details):
        # if new year, we add a tag
        this_year = detail['journal-issue']['published-print']['date-parts'][0][0]
        if year != this_year:
            year = this_year
            years.append(year)
            count = 0
            if year is not None:
                htmls.append(HTML_TABLE_FOOTER)
            htmls.append(HTML_TABLE_HEADER.format(year, year))
        count += 1
        authors = ''
        for author in detail['author']:
            if author['family'].lower().strip() in author_list:
                authors += '<U><B>{} {}</B></U>, '.format(author['given'], author['family'])
            else:
                authors += '{} {}, '.format(author['given'], author['family'])
        authors = authors[:-2]  # remove the last comma
        # journal
        articlenumber = detail.get('article-number', detail.get('page'))
        htmls.append(
"""
<TR align="left" style="text-align : left;" width="704"><FONT size="2" face="Times New Roman">
[{}] {}<br>
{}<br>
<I>{}</I> <B>{}</B>, {} ({}) <br>
doi: <a href="https://doi.org/{}">{}</a>
</FONT><BR>
<BR>
""".format(
                count, detail['title'][0],
                authors, 
                detail['container-title'][0], detail['volume'], articlenumber, 
                year,
                detail['doi'], detail['doi'], )
        )

    htmls.append(HTML_TABLE_FOOTER)

    # add link
    header = []
    for year in years:
        year = int(year)
        header.append('<a href="#{}"><img src="img/icon.gif" alt="icon" border="0" />{}</a>'.format(year, year))
        if year % 5 == 0:
            header.append('<br>')
    header.append('<br>')

    htmls = header + htmls
    with open(outname, 'w') as f:
        for html in htmls:
            f.write(html + '\n')


def remove_duplicates(doi):
    return list(set([d.lower().strip() for d in doi]))

if __name__ == '__main__':
    files = [
        'paperlist_hasuo.txt',
        'paperlist_shikama.txt',
        'paperlist_kuzmin.txt',
        'paperlist_fujii.txt',                 
    ]
    doi_list = []
    for file in files:
        with open(file, 'r') as f:
            doi_list += f.readlines()
    doi_list = remove_duplicates(doi_list)
    details = download_details(doi_list, maxcount=None)
    # save_markdown(details, 'papers.md')
    save_html(details, 'papers_all.html', [
        'fujii', 'hasuo', 'shikama', 'kuzmin'])
