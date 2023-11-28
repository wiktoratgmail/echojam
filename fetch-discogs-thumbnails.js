// fetch-discogs-thumbnails.js

const fetch = require('node-fetch');
const fs = require('fs');

// Funkcja do pobierania miniatury z Discogs na podstawie identyfikatora release
async function fetchDiscogsThumbnail(releaseId, apiKey) {
  try {
    const apiUrl = `https://api.discogs.com/releases/${releaseId}?key=${apiKey}&secret=${apiKey}`;
    const response = await fetch(apiUrl);
    const data = await response.json();

    if (data.master_id) {
      const masterUrl = `https://api.discogs.com/masters/${data.master_id}?key=${apiKey}&secret=${apiKey}`;
      const masterResponse = await fetch(masterUrl);
      const masterData = await masterResponse.json();

      if (masterData.images && masterData.images.length > 0) {
        return masterData.images[0].uri;
      }
    }

    return null;
  } catch (error) {
    console.error('Błąd pobierania miniatury z Discogs:', error);
    return null;
  }
}

// Przykładowe użycie
const releaseId = '123456'; // Zastąp identyfikatorem rzeczywistego release
const apiKey = 'your_discogs_api_key'; // Zastąp kluczem API Discogs

fetchDiscogsThumbnail(releaseId, apiKey)
  .then(thumbnailUrl => {
    if (thumbnailUrl) {
      console.log('Pobrano miniaturę:', thumbnailUrl);
    } else {
      console.log('Miniatura niedostępna.');
    }
  });
