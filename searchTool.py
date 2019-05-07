# The structure of the inverted index and url index:
#
# url index(url_keys) as a dict: {1:root_url, 2:second url crawled, 3:third...}
#
# inverted index(word_index) as a dict with values as arrays:
# {
# torch : [[1,2],[2,7],[5,1]...]
# where the 1st index is the url_id and the 2nd is the number of occurences in that url
# }

import requests
from bs4 import BeautifulSoup as BS
from bs4 import Comment
import time
import json


# Initial global variable values
ready_to_continue = True
website = 'http://example.webscraping.com'

# Global variables for loading the inverted index
page_key = dict()
inverted_index = dict()

while True:

    # Allow the user to pause before continuing with command options in some cases
    if(ready_to_continue == False):
        input('Press enter to continue...')

    # Initial selection options
    print('\nPlease enter a command from the following:\n')
    print('build                             :- crawls website, builds index')
    print('load                              :- loads the index')
    print('print [word]                      :- prints inverted index of a word')
    print('find [word1] [word2]...[wordk]    :- returns all pages containing given words')
    print('quit                              :- quit this client\n')

    # Take command
    command = input('>>> ')
    command_list = command.split()

    if (command_list[0]=='build'):
        # Create queue initialised with the root URL and crawled list to store
        # already crawled URLs
        website_queue = [website]
        crawled = []

        # Create a dict to associate a url to a unique id
        url_id = 1
        url_keys = dict()

        # Create a dict to store inverted index of keywords
        word_index = dict()

        # Keep going through list while it is not empty
        
        # for i in range(100): # This can be used instead of the while loop,
        # which often takes a long time
        while website_queue:
            # Get the next url to crawl and add it to crawled list
            url = website_queue.pop()
            crawled.append(url)
            print(str(url_id) + ' : ' + url)

            # Check for unwanted urls
            if "/trap" in url:
                # Don't send a request to this url
                pass
            elif "/sitemap" in url:
                # Don't want to crawl the sitemap
                pass
            else:
                # Get the content of this url
                request = requests.get(url)
                # Create Beautiful Soup object from the response
                html_doc = request.content
                soup = BS(html_doc, features="html.parser")

                # Remove the comments and script tags from the soup
                comments = soup.find_all(text=lambda text:isinstance(text, Comment))
                for comment in comments:
                    comment.extract()
                for script in soup.find_all('script'):
                    script.extract()

                # Store frequency of words
                word_list = soup.get_text().split()

                # Count occurences of each word into a temporary dict
                word_count_dict = dict()
                for word in word_list:
                    if word not in word_count_dict:
                        word_count_dict[word] = 1
                    else:
                        word_count_dict[word] += 1

                # Add word counts into full index
                for key in word_count_dict:
                    if key not in word_index:
                        word_index[key] = [[url_id, word_count_dict[key]]]
                    else:
                        # Append the count from this url to a word's index
                        word_index[key].append([url_id, word_count_dict[key]])


                # Find link tags, if it is a new URL, then add to the list
                for link in soup.find_all('a'):
                    link_url = link.get('href')
                    link_url = website + link_url
                    if link_url in website_queue:
                        # Do nothing, url already stored
                        pass
                    elif link_url in crawled:
                        # Do nothing, url already crawled
                        pass
                    else:
                        website_queue.append(link_url)

                # Add url to url table and increment url_id
                url_keys[url_id] = url
                url_id = url_id + 1

                # 5 second politeness window before next request
                time.sleep(5)

                # END WHILE

        # Store index and url table in a file
        print(url_keys)
        with open("dicts.txt", 'w') as file:
            file.write(json.dumps([url_keys, word_index]))

        print('Index built\n')
        ready_to_continue = False
        continue

    # Load command
    elif (command_list[0]=='load'):

        # Read in the file as a list of the two dicts
        with open("dicts.txt", 'r') as file:
            dict_list = json.load(file)

        # Split the list to the two dicts
        page_key = dict_list[0]
        inverted_index = dict_list[1]

        print('Loaded inverted index\n')
        ready_to_continue = False
        continue

    # Print command
    elif (command_list[0]=='print'):

        # Check if inverted index has been loaded
        if not bool(inverted_index):
            print('No inverted index has been loaded\n')
        # Check for correct command structure
        elif len(command_list) != 2:
            print('Incorrect number of arguments\n')
            print('Input should be of the form:  print [word]\n')
        # Print the inverted index for the given keyword
        else:
            keyword = command_list[1]
            try:
                keyword_inverted_index = inverted_index[keyword]
                print("Inverted index for " + keyword)
                print(keyword_inverted_index)
            except KeyError as err:
                print('This word does not exist')

        ready_to_continue = False
        continue

    # Find command
    elif (command_list[0]=='find'):
        keyword_inverted_index = dict()
        # Check if inverted index has been loaded
        if not bool(inverted_index):
            print('No inverted index has been loaded\n')
        # Check for correct command structure
        elif len(command_list) < 2:
            print('Incorrect number of arguments\n')
            print('Input should be of the form:  find [word1] [word2]...[wordk]\n')
        # Find the relevant pages for the search term
        else:
            # Skip the first entry which is the 'find' command
            command_iterable = iter(command_list)
            next(command_iterable)
            # Create an index based on the first keyword
            first_keyword = next(command_iterable)
            try:
                keyword_inverted_index = inverted_index[first_keyword]
            except KeyError as err:
                print('The word %s does not exist' % first_keyword)
                continue

            # If there are remaining keywords, iterate over them and compare
            # to the inverted index of the first keyword. Increment the score and
            # removing pages that don't contain all keywords
            for keyword in command_iterable:
                i = 0
                while i < len(keyword_inverted_index):
                    try:
                        temp_index = inverted_index[keyword]
                    except KeyError as err:
                        print('The word %s does not exist' % keyword)
                        i += 1
                        continue
                    for temp_id in temp_index:
                        # The page of this keyword doesn't appear in the current
                        # filtered list from previous keywords, so we ignore it
                        if temp_id[0] < keyword_inverted_index[i][0]:
                            continue
                        # The page matches a page in the current filtered list
                        # so increment the stored score
                        elif temp_id[0] == keyword_inverted_index[i][0]:
                            keyword_inverted_index[i][1] = keyword_inverted_index[i][1] + temp_id[1]
                            i += 1
                            break
                        # Remove this entry from the filtered list
                        else:
                            keyword_inverted_index[i].remove()
                            i += 1
                            break

            print("Search has found the following pages: ")
            # Sort the list before printing based on the second value of each element (the score)
            # First a function to use as the key in sorting, to get the second element
            def scoreSort(element):
                return element[1]
            keyword_inverted_index.sort(key = scoreSort, reverse = True)
            # Print the list
            for i in keyword_inverted_index:
                print(page_key[str(i[0])])

        ready_to_continue = False
        continue

    # Quit option to get out of the infinite program loop
    elif (command_list[0]=='quit'):
        break

    # Enter if command was incorrect
    else:
        print('That is an invalid command, please try again')
        ready_to_continue = False
        continue
