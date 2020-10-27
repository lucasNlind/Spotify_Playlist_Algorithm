# Spotify Playlist Algorithm
An algorithm that recommends a Spotify playlist/list of songs based on weather at a specified location.

## The Idea
I set out to explore the relationship between weather and music with this project. Weather has always played a pretty significant role in the kind of music I'm listening to in any given environment and I thought it would be cool to see what kind of connections existed.

## The Project
I started by manually making playlists that I thought would cater to a certain vibe/atmosphere. Ultimately I wanted to see how what I believed to cater to a certain vibe compared to what Spotify believed to cater to a certain vibe. I wanted my recommendation to be somewhere in the middle. 

To do this, I ran a statistical analysis function on each of my playlists to see what kind of statistics came from each one. The Spotify API provides audio features for each track - some of which I used to determine which songs fit where (i.e if a song was more energetic, it most likely belonged in a sunny weather playlist). The two variables I found to be the most influential determinants were energy and valence. 

### These audio features as described by Spotify:
energy - "Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity."

valence - "A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive while tracks with low valence sound more negative."

### Tempo and Key
Tempo and key were two variables that I thought would end up being the most influential indicators. However, after comparing the average tempo from each playlist, there was no indication of a correlation between tempo and musical atmosphere. Likewise with key, I found that minor/major key distinction offered no correlation. After I came to this realization, I stuck to strictly using energy and valence to determine musical positivity and liveliness. 

### Increasing sample size
The firs statistical analysis I ran was on a Sunny Weather playlist I created with 35 songs. 

### Tools / Resources
The Spotipy Python library ended up being the most incredible resource for this project. The API makes the whole Authorization/data pulling process super easy. I recommend playing around with the library to get comfortable pulling data because it can be fickle sometimes. There are also a bunch of great resources on GitHub that walk you through some examples of using the library. It's super easy once you get the hang of it. 
The actual Spotify application is super intuitive as well. You can pull song/artist/playlist URI's super easily.
I coded everything in Visual Studio Code and then ran the program in MobaXTerm.
