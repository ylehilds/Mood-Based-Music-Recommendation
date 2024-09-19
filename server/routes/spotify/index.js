'use strict'

const Analyzer = require('natural').SentimentAnalyzer;
const stemmer = require('natural').PorterStemmer;
const analyzer = new Analyzer("English", stemmer, "afinn");

module.exports = async function (fastify, opts) {
  fastify.get('/', async function (request, reply) {
    // return 'this is an example'
    const {searchQuery} = request.query
    const token = await getToken()
    const moodScore = getSentimentScore(searchQuery)
    const moodCategory = getPlaylist(moodScore)
    const response = await fetch(`https://api.spotify.com/v1/recommendations?seed_genres=${moodCategory}&min_popularity=50&max_danceability=0.7&limit=20`, {
      headers: {
        'Authorization': 'Bearer ' + token
      }
    })
    let format = await response.json();

    // Filter out explicit tracks
    const cleanTracks = format.tracks.filter(track => !track.explicit);

    return cleanTracks.map(song => ({
      name: song.name,
      artist: song.artists[0].name,
      url: song.external_urls.spotify,
      id: song.id
    }));
  })

  async function getToken() {
    const response = await fetch('https://accounts.spotify.com/api/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + Buffer.from(process.env.SPOTIFY_CLIENT_ID + ':' + process.env.SPOTIFY_CLIENT_SECRET).toString('base64')
      },
      body: 'grant_type=client_credentials'
    })

    const data = await response.json()
    return data.access_token
  }

  function getSentimentScore(mood) {
    return analyzer.getSentiment(mood.split(' '))
  }

  function getPlaylist(score) {
    if (score > 0) {
      return 'happy'
    } else if (score < 0) {
      return 'sad'
    } else {
      // Default seed genres for neutral mood
      return 'pop,chill,acoustic,ambient,classical';
    }
  }
}
