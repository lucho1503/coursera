from requests import requests_with_caching
import json

def get_movies_from_tastedive(movie):
    """ this function takes a input parameter, a string. 
    and return the 5 Tastedive results associated with that string, from the API https://tastedive.com/read/api."""
    baseurl = 'https://tastedive.com/api/similar'
    params_dict = {}
    params_dict['q'] = movie
    params_dict['type'] = 'movies'
    params_dict['limit'] = 5
    resp = requests_with_caching.get(baseurl, params=params_dict)
    print(resp.url)
    return resp.json()

def extract_movie_titles(mo):
    """ this function extracts just the list ofo movies titles
    from a dictionary returned by get_movies_from_tastedive"""
    #lst = []
    #for d in mo['Similar']['Results']:
     #   lst.append(d['Name'])
    return [d['Name'] for d in mo['Similar']['Results']]

def get_related_titles(lst):
    """ This function takes a list of movies titles as a input. it gets five related movies 
    for each from tastedrive, extracts the titles for all of them, and combines them all into a single list,
    dont include the same movio twice """
    #lst2 = []
    #lst3 = []
    #for title in lst:
     #   lst2.append(get_movies_from_tastedive(title))
    lst2 = [get_movies_from_tastedive(title) for title in lst]
    
    #for d in lst2:
     #   lst3.append(extract_movie_titles(d))
    lst3 = [extract_movie_titles(d) for d in lst2]
    
    #lst4 = []
    #for li in lst3:
    #    for l in li:
    #        lst5.append(l)
    lst4 = [l for li in lst3 for l in li]
    #print(lst4)
    return list(set(lst4))
    

def get_movie_data(movie):
    """ this function takes a input which is a string that should represent 
    the title of a movie you want to search, Return a dictionary. from the API https://www.omdbapi.com/ """
    baseurl = 'http://www.omdbapi.com/'
    params_dict = {'t': movie, 'r': 'json'}
    resp = requests_with_caching.get(baseurl, params=params_dict)
    #print(resp.json())
    #print(resp.url)
    return resp.json()

def get_movie_rating(dic):
    """ this function takes an OMBD dictionary result for one movie and extract 
    the Rotten tomatoes rating as an integer """
    value = 0
    for d in dic['Ratings']:
        if d['Source'] == 'Rotten Tomatoes':
            print(d['Value'])
            value = d['Value']
            value = int(value[:-1])
            return value
    return value

#test = extract_movie_titles(get_movies_from_tastedive("Bridesmaids"))
#lst = []
#teste = get_related_titles(["Bridesmaids", "Sherlock Holmes"])
#for title in teste:
  #  get_movie_rating(get_movie_data(title))
 #   lst.append(title)
#print(sorted(lst, reverse=True))
#print(v)
#print(test)
#print(teste)

def get_sorted_recommendations(lst_movies):
    """ It takes a list of movie titles as an input. It returns a sorted list of related movie titles as output,
    up to five related movies for each input movie title. The movies should be sorted in descending order by 
    their Rotten Tomatoes rating, as returned by the get_movie_rating function. Break ties in reverse alphabetic
    order, so that ‘Yahşi Batı’ comes before ‘Eyyvah Eyvah’. """
    
    lst_titles = get_related_titles(lst_movies)
    lst_sort_titles = sorted(lst_titles, key=lambda title: (get_movie_rating(get_movie_data(title)), title), reverse=True)

    return lst_sort_titles
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])

