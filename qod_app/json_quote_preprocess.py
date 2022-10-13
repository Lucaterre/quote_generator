#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
A little script to preprocess
source dataset before insert
in database
"""

import json
import time
import re


def preprocess_dataset(source: str, target: str) -> None:
    start = time.time()

    with open(source, mode='r', encoding='UTF-8') as fp:
        data = json.loads(fp.read())
        print(f"Total initial data: {len(data)}")

        # remove not used keys
        for d in data:
            del d['Tags']
            del d['Popularity']

        # lowercase all keys and convert to unicode/replace specific set of char in value
        data = [
            {
                k.lower(): v.encode('utf-8').decode('utf-8').replace("‎", "").replace("′", "'").replace("…", "...") for k, v in obj.items()
             } for obj in data]

        # remove duplicates quotes entries in json file and
        # remove quotes and authors with non-Latin characters
        non_latin = re.compile(r'^.*[^\x00-\x7f].*$')
        seen = set()
        new = []
        for record in data:
            quote = record['quote']
            author = record['author']
            if not non_latin.match(quote+author):
                if quote not in seen:
                    seen.add(quote)
                    new.append(record)

        data = new
        del seen

        # remove quotes with unknown category
        data = [obj for obj in data if obj['category'] != ""]

        # split author and book (if exists)
        new = []
        for obj in data:
            new_obj = {}
            bad_form = False
            for k, v in obj.items():
                if k == "author":
                    is_author_title = v.split(',')
                    if len(is_author_title) == 2:
                        new_obj['author'] = is_author_title[0]
                        new_obj['source'] = is_author_title[1].strip()
                    elif len(is_author_title) > 2:
                        bad_form = True
                    else:
                        new_obj['author'] = v
                        new_obj['source'] = "unknown"
                else:
                    new_obj[k] = v
            if not bad_form:
                new.append(new_obj)

        data = new

    with open(target, 'w', encoding='utf-8') as fw:
        json.dump(data, fw, indent=4, ensure_ascii=False)

    print(f"Total final data: {len(data)}")
    print(f"TOTAL TIME: {time.time() - start}")


if __name__ == '__main__':
    preprocess_dataset(source='data/quotes.json',
                       target='data/quotes_preprocess.json')
