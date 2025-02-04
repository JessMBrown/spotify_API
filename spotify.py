# I will be using spotify api for this project
from dotenv import load_dotenv
import time
import os
import base64
from requests import post, get
import json

# find and read the contents of the .env file
load_dotenv()
# pull the credentials from the .env and assign to local vars
client_id = os.getenv("Client_ID_Spotify")
client_secret = os.getenv("Client_Secret_Spotify")
# display a welcome message
print(
    'Welcome to my spotify API, lets find your favorite artists top tracks and information'
)
time.sleep(2)


def get_artist_name():
    # Ask for artist name to be used in the search
    artist_name_entered = input('\nWhat artist are you searching for?: ')
    time.sleep(2)
    # function return the value entered by the user
    return artist_name_entered


def get_token():
    # start the request builder specified on the spotify documentation
    # add the client id and client secret together joining with a colon
    auth_string = client_id + ":" + client_secret
    # encode it to utf-8
    auth_bytes = auth_string.encode("utf-8")
    # convert it to base64
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    # specify the base url
    url = "https://accounts.spotify.com/api/token"
    # specify the headers and content-type to be sent in the POST request
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    # specify the body of the POST - a request for client credentials
    data = {"grant_type": "client_credentials"}
    # send the POST request and store the response
    result = post(url, headers=headers, data=data)
    # transform the response to json
    json_result = json.loads(result.content)
    # extract the contents of the access_token field and store it
    token = json_result["access_token"]
    # check the token is returned successfully
    # if the token is empty print a generic error message
    # boolean statement and if else statement
    if len(token) == 0:
        print("Error retrieving token")
    # if the token has any content assign it to "token" and return it
    else:
        return token


def get_auth_header(token):
    # construct the auth header using the contents of 'token'
    return {"Authorization": "Bearer " + token}


def search_for_artist(token, artist_name):
    # specify the base url
    url = "https://api.spotify.com/v1/search"
    # get the evaluated header and store it
    headers = get_auth_header(token)
    # specify the query url to be added to the base url in the request
    query = f"?q={artist_name}&type=artist&limit=1"
    # specify the fully qualified url
    query_url = url + query
    # store the GET response
    result = get(query_url, headers=headers)
    # transform the response to json and extract the contents from the "artists" and "items" fields
    json_result = json.loads(result.content)["artists"]["items"]
    # if the response is empty display an error
    if len(json_result) == 0:
        print("No artist found. . . .")
        return None
    # return the first result from the json_results array
    return json_result[0]


def get_songs_by_artist(token, artist_id):
    # specify the url using the passed in value from artist_id variable NOTE: country=UK is not valid
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    # get the evaluated header and store it
    headers = get_auth_header(token)
    # store the GET response
    result = get(url, headers=headers)
    # transform the response to json and extract the contents from the "tracks" field
    json_result = json.loads(result.content)["tracks"]
    # return the contents of "tracks"
    return json_result


# I can't think of anything that would be useful being sliced when it comes to info. on the artist and song
# so created a quiz that gets the first song from songs (songs[0]), slices the first four letters from the song name
# and asks for user input
def quiz():
    # get the first song from the "songs" array
    first_song = songs[0]["name"]
    # define the slice value to the first four characters
    s1 = slice(4)
    # ask a question, the question uses the first song retrieved from the "songs" array and splices using the value
    # from "s1"
    print("Can you guess the top song from the first four letters of the song? : " + first_song[s1])
    # Accept user input and store it
    quiz_answer = input()
    # compare the users input with the answer for a full or partial match
    # set both sets of text to lowercase to avoid any comparison issues
    # if the value entered is not found in the songs name (the answer is incorrect)
    if quiz_answer.lower() not in first_song.lower():
        # print a message saying the answer is incorrect
        print("That's not it")
        # ask the question does the user want to try again
        try_again = input("Try again? y/n ")
        # convert the value entered to lowercase and check if is equal to "y"
        if try_again.lower() == "y":
            # ask a question for the answer for a second time
            second_quiz_answer = input("The answer is: ")
            # if the value entered is found in the songs name (the answer is correct)
            if second_quiz_answer.lower() in first_song.lower():
                # print a message saying it is
                print("Correct!")
                time.sleep(3)
            # the value entered is incorrect
            else:
                # print a message saying it is wrong and what the song actually was
                print("Sorry wrong again, it was " + first_song)
                print("Here's the list!")
                time.sleep(2)
        # convert the value entered to lowercase and check if is equal to "n"
        elif try_again.lower == "n":
            # print a message saying the songs will be displayed
            print("Here's the list")
            time.sleep(2)
    # if the value entered is correct print a message saying it was correct
    elif quiz_answer.lower() in first_song.lower():
        print("Correct!")
        time.sleep(3)

# specify where to get the token
token = get_token()
# specify the artists name
result = search_for_artist(token, get_artist_name())
# extract the arist's id needed to make the request to spotify as outlined in the documentation
artist_id = result["id"]
# make the request for the artists top-10 songs using the artist id
songs = get_songs_by_artist(token, artist_id)
# ask the quiz question
quiz()

print(f"The top 10 songs for the artist are: ")
# loop through the songs returned, get the name and print them out
# Dictionary (enumerate)
for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}")

# save to file
songs_for_file = str(songs)
writeFile = open('songs.txt', 'w')
writeFile.write(songs_for_file)
writeFile.close()
