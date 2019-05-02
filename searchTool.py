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

        # Keep going through list while it is not empty
        while website_queue:

            # Get the next url to crawl and add it to crawled list
            url = website_queue.pop()
            crawled.append(url)

            # Get the content of this url
            request = requests.get(url)
            # Create Beautiful Soup object from the request
            with open(request) as html_doc:
                soup = BS(html_doc)

            # Store frequency of words
            # Find link tags, if new URL then add to queue (standard or priority)
            for link in soup.find_all('a'):
                link_tags.append(link.get('href'))
            # Store index in a file

            # 5 second politeness window before next request
            time.sleep(5)

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
