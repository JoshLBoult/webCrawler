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
import time


# Initial global variable values
ready_to_continue = True
website = 'http://example.webscraping.com/'

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
        while website_queue:

            # Get the next url to crawl and add it to crawled list
            url = website_queue.pop()
            crawled.append(url)

            # Check for unwanted urls
            if "/trap" in url:
                # Don't send a request to this url
            elif "/sitemap" in url:
                # Don't want to crawl the sitemap
            else:
                # Get the content of this url
                request = requests.get(url)
                # Create Beautiful Soup object from the response
                with open(request) as html_doc:
                    soup = BS(html_doc)

                # Store frequency of words
                word_list = soup.get_text().split()

                for word in word_list:
                    if word in word_index:
                        # Check if it has an entry for this url_id
                    else:
                        word_index[word] = [[url_id, 1]]


                # Find link tags, if it is a new URL, then add to the list
                for link in soup.find_all('a'):
                    link_url = link.get('href')
                    if link_url in website_queue:
                        # Do nothing, url already stored
                    elif link_url in crawled:
                        # Do nothing, url already crawled
                    else:
                        website_queue.append(link_url)

                # Add url to url table and increment url_id
                url_keys[url_id] = url
                url_id = url_id + 1
                # Store index and url table in a file

                # 5 second politeness window before next request
                time.sleep(5)

        print('Index built\n')
        ready_to_continue = False
        continue

    elif (command_list[0]=='load'):
        print('Not yet implemented...\n')
        continue

    elif (command_list[0]=='print'):
        print('Not yet implemented...\n')
        continue

    elif (command_list[0]=='find'):
        print('Not yet implemented...\n')
        continue

    # Option to get out of the infinite program loop
    elif (command_list[0]=='quit'):
        break

    # Enter if command was incorrect
    else:
        print('That is an invalid command, please try again')
        ready_to_continue = False
        continue
