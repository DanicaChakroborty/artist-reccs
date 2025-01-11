'''
Date: December 1st, 2024
Names: Danica Chakroborty, Cade Fabio, Lucas Mauriello
Pledge: I pledge my honor that I have abided by the Stevens Honor System
Group Name: 404 Not Found
Description: Group Project Part 2
'''

from os import path 


def nameReal(name):
    '''
    This function checks to see if a name exists, and takes in name as a parameter
    - Danica Chakroborty
    '''
    database = open('musicrecplus.txt', 'r+')
    for x in database:
        temp = x.split(':')
        if temp[0].lower().strip() == name.lower().strip():
            return temp[1].strip().split(',')
    return []


def menu(name, pref):
    '''
    This function is what displays the menu that was described, and also returns 'invalid value'
    if the user enters something not on the menu
    - Danica Chakroborty
    '''
    if not pref or pref == ['']:
        pref = newList(pref)
    x = 0
    while x == 0:
        print("\nEnter a letter to choose an option:")
        print("e - Enter preferences")
        print("d - Delete preferences")
        print("s - Show preferences")
        print("r - Get recommendations")
        print("p - Show most popular artists")
        print("h - How popular is the most popular")
        print("m - Which user has the most likes")
        print("q - Save and quit")
        selection = input("Your choice: ").lower().strip()
        if selection == "e":
            pref = newList(pref)
        elif selection == "d":
            pref = delPref(pref)
        elif selection == "s":
            showPref(pref)
        elif selection == "r":
            getReccs(pref, name)
        elif selection == "p":
            show_most_popular_artists(pref, name)
        elif selection == "h":
            how_popular_is_most_popular_artist(pref, name)
        elif selection == "m":
            which_user_likes_the_most_artists(name, len(pref))
        elif selection == "q":
            save_and_quit(name, pref)
            x = 1
        else:
            print("Invalid value!!!")

def showPref(pref):
    '''
    This extra credit function will display the user's preferences so far
    - Danica Chakroborty
    '''
    if not pref:
        print("You currently have no preferences!!")
    else:
        print("Your current preferences:")
        for artist in pref:
            print(f"- {artist}")


def newList(pref):
    '''
    This function creates a new list with the artists that the user prefers
    - Danica Chakroborty
    '''
    while True:
        name = input('Enter an artist that you like (Enter to finish): ')
        if name == '':
            break
        if name.title() not in pref:
            pref.append(name.title())
    pref.sort()
    return pref

def delPref(pref):
    '''
    This function is the extra credit addition which allows users to remove artists 
    from their preferences, I used the enumerate function to go thru the items and provide
    them with indexes automatically to make this easier, and since it's extra credit I hope that's 
    okay, I learned it in my software engineering class!
    - Danica Chakroborty
    '''
    if not pref:
        print("Oopsies! You have no preferences to delete!")
        return pref

    print("Your current preferences:")
    for ind, artist in enumerate(pref, start=1):
        print(f"{ind}. {artist}")

    while True:
        choice = input("Enter the number of the artist to delete (Enter to finish): ").strip()
        if choice == '':
            break
        if choice.isdigit() and 1 <= int(choice) <= len(pref):
            ind = int(choice) - 1
            print(f"Removing {pref[ind]}")
            pref.pop(ind)
        else:
            print("Invalid,  please select a valid number look at the menu!!")
    return pref

def real(filepath):
    '''
    This is a helper function I made to make sure that the file path exists because
    I was getting some weird errors at the start - might be redundant now but I didn't 
    want to take it out just in case
    - Danica Chakroborty
    '''
    return path.exists(filepath)

def readD(filepath):
    '''
    This is a helper function that reads the database file and returns all of its contents
    as lines, and uses the real function
    - Danica Chakroborty
    '''
    if not real(filepath):
        print("The database file was not found, so no reccomendations at the moment!!")
        return []
    with open(filepath, 'r') as file:
        return [line.strip() for line in file]
    
def check(databaseLines):
    '''
    This is another helper function for getReccs, which goes through 
    the database lines and put them in dictionaries of users and their preferences
    - Danica Chakroborty
    '''
    userData = {}
    for x in databaseLines:
        parts = x.split(':')
        if len(parts) < 2:
            continue
        user = parts[0].strip()
        prefs = [artist.strip() for artist in parts[1].split(',')]
        userData[user] = prefs
    return userData

def bestReccs(prefs, userData, userName):
    '''
    This is also another helper function for getReccs, which identifies
    the reccomendations based on how frequent an artist is in the other user's
    preferences
    - Danica Chakroborty
    '''
    freq = 0
    ogReccs = []
    for otherUser, likes in userData.items():
        if otherUser.lower() == userName.lower() or '$' in otherUser:
            continue
        overlap = 0
        uniqReccs = []
        for like in likes:
            if like in prefs:
                overlap += 1
            elif like not in uniqReccs:
                uniqReccs.append(like)
        if uniqReccs and overlap > freq:
            freq = overlap
            ogReccs = uniqReccs
    return sorted(ogReccs) if ogReccs else []

def getReccs(prefs, userName):
    '''
    This function returns reccomendations that are based upon users with similar responses,
    if none are similar the function returns as such. We did the extra credit in this so it says
    no reccomendations and reprints the list when appropriate instead of crashing out on us! I used the above helper
    functions to make this code easier to write!
    - Danica Chakroborty
    '''
    if isinstance(prefs, str):
        prefs = prefs.split(',')
    prefs = [artist.strip() for artist in prefs]
    dbLines = readD('musicrecplus.txt')
    if not dbLines:
        return
    userData = check(dbLines)
    reccs = bestReccs(prefs, userData, userName)
    if reccs:
        print("Your reccomendations:")
        for artist in reccs:
            print(artist)
    else:
        print("Sorry, no recommendations can be made right now!!")


def show_most_popular_artists(pref, name):
    '''
    This function will print the top 3 artists that are most popular among users
    We used the enumerate function to go thru the items and provide them with indexes 
    automatically to make this easier, we hope that's okay!
    We also added an extra bit - I know this wasn't in the example 2 file but it was in the directions
    to print the top THREE artists not just the top one, so that's what we did!
    - Cade Fabio
    '''
    database = open('musicrecplus.txt', 'r')
    artists = {}
    for artist in pref:
        artist = artist.strip()
        artists[artist] = artists.get(artist, 0) + 1
    for x in database:
        user_data = x.strip().split(':')
        if len(user_data) < 2:
            continue
        user = user_data[0].strip()
        user_artists = user_data[1].split(',')
        if '$' in user:
            continue
        for artist in user_artists:
            artist = artist.strip()
            artists[artist] = artists.get(artist, 0) + 1
    database.close()
    if not artists:
        print("Sorry, no artists found.")
        return
    sorted_artists = sorted(artists.items(), key=lambda x: x[1], reverse=True)
    for i, (artist, _) in enumerate(sorted_artists[:3]):
        print(artist)

def how_popular_is_most_popular_artist(database, name):
    '''
    This function will return the frequency of the most popular artist
    - Cade Fabio
    '''
    database = open('musicrecplus.txt', 'r')
    artists = {}
    for artist in pref:
        artist = artist.strip()
        artists[artist] = 1  
    for line in database:
        user_data = line.strip().split(':')
        if len(user_data) < 2:
            continue
        user = user_data[0].strip()
        user_artists = user_data[1].split(',')
        if '$' in user or user.lower() == name.lower():
            continue
        for artist in user_artists:
            artist = artist.strip()
            artists[artist] = artists.get(artist, 0) + 1
    database.close()
    if not artists:
        print("Sorry, no artists found!!")
        return
    max_likes = max(artists.values())
    print(max_likes)

def which_user_likes_the_most_artists(name, num):
    '''
    This function will return the user with the most likes
    - Cade Fabio
    '''
    database = open('musicrecplus.txt', 'r')
    user_likes = {}
    user_likes[name] = len(pref)
    for line in database:
        user_data = line.strip().split(':')
        if len(user_data) < 2:
            continue
        user = user_data[0].strip()
        user_artists = user_data[1].split(',')
        if '$' in user:
            continue
        user_likes[user] = len(user_artists)
    database.close()
    if not user_likes:
        print("Sorry, no user found!!")
        return
    max_likes = max(user_likes.values())
    users_with_max_likes = [user for user, likes in user_likes.items() if likes == max_likes]
    for user in sorted(users_with_max_likes):
        print(user)


       
def save_and_quit(name, prefList):
    '''
    This function will save the input and changes made by the user and end the program
    - Cade Fabio
    '''
    form = ''
    hold = []
    for i in range(len(prefList)):
        if i != len(prefList) - 1:
            form += str(prefList[i]) + ','
        else:
            form += prefList[i]
    form = str(name) + ':' + form
    database = open('musicrecplus.txt', 'r+')
    for line in database:
        if line.split(':')[0] != name:
            hold += [line]
    hold += [form]
    hold.sort()
    database = open('musicrecplus.txt', 'w')
    database.write('')
    database = open('musicrecplus.txt', 'a')
    for i in hold:
        if '\n' not in i:
            i += '\n'
        database.write(i)

'''
This makes sure that the path exists and will call the menu function!
- Danica Chakroborty
'''
if path.exists('musicrecplus.txt'):
    database = open('musicrecplus.txt', 'r+')
else:
    database = open('musicrecplus.txt', 'w+')
name = input('Enter your name (put a $ symbol after your name if you wish your preferences to remain private): ')
pref = nameReal(name)
menu(name, pref)