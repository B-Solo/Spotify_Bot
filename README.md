# Spotify Handler 

## Summary

This system currently provides two somewhat distinct pieces of functionality, and a main script that uses these libraries to compare a google sheets copy of a playlist's titles with the actual titles from Spotify.

These are grouped together is that the legacy handling of Spotify playlists
was manual and used Google Sheets, and so this tool integrates with the
existing sheet rather than using a new .csv file.

## Requirements

This module has been developed in Python 3.11.4. Please see the attached requirements.txt file for the Python libraries used and their versions.

## Setup

As well as the necessary requirements, authentication tokens are required for both the Spotify and Google Sheets APIs. 

### Spotify Authentication Tokens

The `spotify_handler.py` module requires an accompanying file `spotify_tokens.py` to contain the relevant authentication information. The file should take the form:

```
CLIENT_ID = <client ID>
CLIENT_SECRET = <client secret>
REDIRECT_URI = <redirect URI>
```

where the client ID, client secret, and redirect URI are all strings that can 
be found on the Spotify developer dashboard, in the app set up to interface 
with this library, on the 
[basic information page](https://developer.spotify.com/dashboard/e287922924f04651a63a8476fdfa59eb/settings).

### Google Authentication Tokens

In order to use the `sheets_handler.py` module, a file named 
`google_base_credentials.json` must be created. We can download this file
(it will need renaming) from 
[the credentials page](https://console.cloud.google.com/apis/credentials?authuser=1&project=spotify-project-395708&supportedpurview=project) of the google project. 


## The Spotify Handler Library

## The Google Sheets Handler Library

As can be seen in detail on
[this helppage](https://developers.google.com/sheets/api/quickstart/python),
the way that Google Authentication works is that the project on Google's
servers has "authentication credentials", and these credentials can be used
to generate a token to allow access. The reasoning here is that the credentials
provide a pathway to the project no matter the user, whereas the token is
account specific, and requires signing in with an email to first be generated.

The module then takes care of generating the tokens,
requesting login details from the user where appropriate.