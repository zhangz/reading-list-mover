# Reading List Mover

Folked from [codebox/reading-list-mover][]:

- Updated to latest APIs. 
- Only support copy bookmarks between Instapaper, Readability, Pocket.

Here's a small Python library to [copy bookmarks/favourites between a number of online services][source]. The library supports [Instapaper][], [Readability][], [Pocket][] (formerly ReadItLater), [Pinboard][], [Delicious][], [Diigo][], [GitHub][]*, [StackOverflow][]* and [Twitter][]* ('*' indicates export only).

To use the library you will need to populate your copy of the [config.txt][] file with the details of your accounts on the services that you are going to use. In the case of Readability, Pocket, Instapaper and Diigo you will also need to apply for an API key:

- [Readability API key](http://help.readability.com/customer/portal/articles/267466-i%E2%80%99m-a-developer-how-can-i-get-an-api-key-)
- [Pocket API key](http://getpocket.com/api/signup/)
- [Instapaper API key](http://www.instapaper.com/main/request_oauth_consumer_token)

You will also need to have the [oauth2][] Python library installed on your system.

Here's an example showing how to copy all your bookmarks from one service to another:

# Copy all bookmarks from Pocket to Readability
pocket = buildPocket()
readability = buildReadability()

for b in pocket.getBookmarks():
    readability.addBookmark(b)
```

You can also use the library to export a list of your bookmarks for use as a backup:

# Print out all bookmarks from Pocket
pocket = buildPocket()

for b in pocket.getBookmarks():
    print b['given_title'] + ': ' + b['given_url']
```

[source]: https://github.com/codebox/reading-list-mover
[Instapaper]: http://www.instapaper.com/
[Readability]: https://www.readability.com/
[Pocket]: http://getpocket.com/
[Pinboard]: http://pinboard.in/
[Delicious]: http://delicious.com/
[Diigo]: http://diigo.com/
[GitHub]: http://github.com/
[StackOverflow]: http://stackoverflow.com/
[Twitter]: http://twitter.com/
[config.txt]: https://github.com/codebox/reading-list-mover/blob/master/config.txt
[oauth2]: https://github.com/simplegeo/python-oauth2
[codebox/reading-list-mover]: https://github.com/codebox/reading-list-mover
