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

    # open the dataset
    with open(source, mode='r', encoding='UTF-8') as fp:
        data = json.loads(fp.read())
        print(f"Total initial data: {len(data)}")

        # remove not used keys for this project
        for d in data:
            del d['Tags']
            del d['Popularity']

        # lowercase all keys and convert to unicode/replace specific set of char in value that observed
        data = [
            {
                k.lower(): v.encode('utf-8').decode('utf-8').replace("‎", "").replace("′", "'").replace("…", "...") for k, v in obj.items()
             } for obj in data]

        # remove duplicates quotes entries in json file and
        # remove quotes and authors with non-Latin characters
        non_latin = re.compile(r'^.*[^\x00-\x7f].*$')
        # create a set to remove duplicate
        seen = set()
        new = []
        # iterate over data
        for record in data:
            quote = record['quote']
            author = record['author']
            # concatenate author and quote and test if contains non latin characters
            if not non_latin.match(quote+author):
                # if quote not seen, store it in set
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
                    # if author has length > 2 that means author and book
                    # are concatenated.
                    # This can be updated because sometimes we have eg. ['Martin Luther King', 'Jr.']
                    if len(is_author_title) == 2:
                        new_obj['author'] = is_author_title[0]
                        # create a new entry in dict that called source
                        new_obj['source'] = is_author_title[1].strip()
                    # To simplify we decided to removed not formatted data in dataset
                    # eg. Jules, Verne, 1865, De la Terre à la lune by set a flag to True
                    elif len(is_author_title) > 2:
                        bad_form = True
                    # if author length is equals to 1, we affect a default 'unknown' value
                    # to source
                    else:
                        new_obj['author'] = v
                        new_obj['source'] = "unknown"
                else:
                    new_obj[k] = v
            if not bad_form:
                new.append(new_obj)

        data = new

    # write the clean data to an output in json
    with open(target, 'w', encoding='utf-8') as fw:
        json.dump(data, fw, indent=4, ensure_ascii=False)

    print(f"Total final data: {len(data)}")
    print(f"TOTAL TIME: {time.time() - start}")


if __name__ == '__main__':
    preprocess_dataset(source='data/quotes.json',
                       target='data/quotes_preprocess.json')
