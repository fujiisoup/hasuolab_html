"""
Find details of papers and export as necessary formats
Need to install crossref library,
>>> pip install crossrefapi
"""
import numpy as np
import pandas as pd
from find_papers import is_same_person, read_people, HTML_TABLE_HEADER, HTML_TABLE_FOOTER


MASTER_COLOR = 'red'
DOCTOR_COLOR = 'blue'
STAFF_COLOR = 'black'


def sort_by_date(details, newest_first=True):
    dates = details['date start']
    idx = dates.argsort()
    # if newest_first:
    #     idx = idx[::-1]

    idx = details['date start'].sort_values().index[::-1]
    return details.iloc[idx]


def save_html(
    details, outname, people
):
    """
    Save as a markdown format
    """
    # author_list = [au.lower() for au in author_list]

    details = sort_by_date(details)
    htmls = []

    year = None
    years = []
    count = 0
    for i in range(len(details['authors'])):
        detail = details.iloc[i]
        if len(str(detail['title'])) < 5:
            continue

        # if new year, we add a tag
        this_year = detail['date start'].year
        if year != this_year:
            year = this_year
            years.append(year)
            count = 0
            if year is not None:
                htmls.append(HTML_TABLE_FOOTER)
            htmls.append(HTML_TABLE_HEADER.format(year, year))
        count += 1
        authors = ''
        for author in detail['authors'].replace(';', ',').replace(', and', ',').replace('and', ',').split(','):
            if len(author.strip()) == 1:
                continue
            given = author[:author.find('.')].strip()
            family = author[author.find('.') + 1 :].strip()
            if is_same_person(family, given, people['master'].get(int(year), [])):
                authors += '<B style="color:{};">{}. {}</B>, '.format(
                    MASTER_COLOR, given.upper(), family)
            elif is_same_person(family, given, people['doctor'].get(int(year), [])):
                authors += '<B style="color:{};">{}. {}</B>, '.format(
                    DOCTOR_COLOR, given.upper(), family)
            elif is_same_person(family, given, people['staff'].get(int(year), [])):
                authors += '<B style="color:{};">{}. {}</B>, '.format(
                    STAFF_COLOR, given.upper(), family)
            else:
                authors += '{}. {}, '.format(given, family)
        authors = authors[:-2]  # remove the last comma

        htmls.append(
"""
<TR align="left" style="text-align : left;" width="704"><FONT size="2" face="Times New Roman">
[{}] {}<br>
{}<br>
<I>{}</I>, {}, {} ({}) <br>
</FONT><BR>
<BR>
""".format(
                count, detail['title'],
                authors, 
                detail['conference'],
                detail['date start'].strftime('%Y-%m-%d'), 
                detail['city'], detail['country'])
        )

    htmls.append(HTML_TABLE_FOOTER)

    # add link
    header = []
    for i, year in enumerate(years):
        year = int(year)
        header.append('<a href="#{}"><img src="img/icon.gif" alt="icon" border="0" />{}</a>'.format(year, year))
        if year % 5 == 0:
            header.append('<br>')
    header.append('<br>')
    header.append(
'''<br>
<br>
<b style="color: {};">
red name: master students
</b><br>
<b style="color: {};">
blue name: doctor students
</b><br>
'''.format(MASTER_COLOR, DOCTOR_COLOR))

    htmls = header + htmls
    with open(outname, 'w') as f:
        for html in htmls:
            f.write(html + '\n')


if __name__ == '__main__':
    # people
    people_config = read_people('staffs_students.ini')

    details = pd.read_csv('conference.csv', parse_dates=['date start', 'date end'])
    save_html(details, '../conference_all.html', people_config)
