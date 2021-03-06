Adaptation and extension of Falicon's AngelList api ( http://angel.co/api )

# DISCLAIMER:

Note: This code is a quick hack for a personal project I'm playing around with. There are obvious holes (for example the delete stuff isn't working yet) and there are most certainly much cleaner/better/faster ways to interact with the AngelList api, but this version basically gave me quick access to the functionality that I needed at the time.

If you have questions, comments, or updates you would like me to include please feel free to post an issue on this fork.

# OAUTH:

The AngelList api requires authentication via OAuth2 ( http://angel.co/api/oauth/faq ). This process is started by sending users to a specific angel.co url to authorize your app. You generate that url like this:

auth_url = "https://angel.co/api/oauth/authorize?client_id=%s&response_type=code" % 'YOUR_CLIENT_ID_ASSIGNED_BY_ANGEL_LIST'

Then you just redirect your user to the generated URL. Once a user validates your app on AngelList, AngelList will send them back to the endpoint your specified when you set up your app along with a URL param of code. It will look something like this:

http://localhost?code=08a6502cb3199adf9f7d50c85254a0f1

The next step is to use this returned code, along with your client_id, and client_secret to obtain a valid access_token. You do that like this:

import angellist
al = angellist.AngelList()
al.client_id = 'YOUR_CLIENT_ID_ASSIGNED_BY_ANGEL_LIST'
al.client_secret = 'YOUR_CLIENT_SECRET_ASSIGNED_BY_ANGEL_LIST'
access_token = al.getAccessToken(code='THE_CODE_YOU_JUST_GOT_IN_THE_AUTH_RESPONSE_URL')

and if all goes well, you should now have a valid access_token that you can store along with this users account details and make valid AngelList api calls for.

# BASICS:

If you have a valid access token, you should be able to something like the following:

import angellist
al = angellist.AngelList()
al.access_token = 'YOUR_VALID_ACCESS_TOKEN_FROM_OAUTH_PROCESS'
my_angel_list_profile = al.getMe()

-- IMPORTANT NOTE -- All requests expect a valid access_token to be set (see the OAuth section for details on obtaining a valid access_token).

# METHODS:

- getFeed()

- deleteFollows(follow_type='', follow_id='') - currently known issues
- addFollows(follow_type='', follow_id='')
- getFollowers(user_id='', page=1)
- getFollowersIds(user_id='', page=1)
- getFollowing(user_id='', page=1)
- getFollowingIds(user_id='', page=1)
- getStartupsFollowers(startup_id='', page=1)
- getStartupsFollowersIds(startup_id='', page=1)

- getReviews(user_id='', page=1)

- getStartups(startup_id='')

- getStartupRoles(user_id='', startup_id='', page=1)

- getStatusUpdates(user_id='', startup_id='', page=1)
- postStatusUpdates(startup_id='', message='')
- deleteStatusUpdates(status_id='') - currently known issues

- getTags(tag_id='', domain='', page=1)

- getUsers(user_id='', page=1)
- getUsersSearch(slug='', email='')
- getMe()

- getSearch(query='', type_option='')

# KNOWN ISSUES:

- DELETE requests (deleteFollows and deleteStatusUpdates) are not currently working (I have not yet been able to debug just how AngelList is expecting DELETE requests to be submitted).

