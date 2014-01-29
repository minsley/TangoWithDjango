import json
import urllib, urllib2
import sys
from lib2to3.fixer_util import String

def run_query(search_terms):
    # Build URL base
    root_url = 'https://api.datamarket.azure.com/Bing/Search/v1/'
    source = 'Web'
    
    results_per_page = 10
    offset = 0      # Display the 0th result and on
    
    # Bing API requires the query to be wrapped in quotes
    query = "'{0}'".format(search_terms)
    query = urllib.quote(query)
    
    # Build the URL suffix and format response in json
    search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
       root_url,
       source,
       results_per_page,
       offset,
       query)
    
    # Set up Bing server authentication
    username = ''   # Must be blank String
    bing_api_key = 'CaYOYJwcsaJDfdMrIM3/KHBVUq6Jb3URMjml5mOoc2Q'
    
    # Create a 'password manager' to handle authentication
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, search_url, username, bing_api_key)
    
    results = []
    
    try:
        # Prepare to connect to Bing servers
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        
        # Connect to the server and read the response
        response = urllib2.urlopen(search_url).read()
        
        # Convert the string response to a Python dict
        json_response = json.loads(response)
        
        # Loop through each page returned, populate the results list
        for result in json_response['d']['results']:
            results.append({
                'title': result['Title'],
                'link': result['Url'],
                'summary': result['Description']})
            
    # Catch URLError exceptions
    except urllib2.URLError, e:
        print "Error when querying the Bing API: ", e
        
    # Return the list of results to the calling function
    return results

def main():
    search_terms = str(raw_input("Enter search terms: "))

    results = run_query(search_terms)
    for result in results:
        print(str(results.index(result) + 1) + "    " +
              str(result['title']) + "    " +
              str(result['link']))

if __name__ == '__main__':main()