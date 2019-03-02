// Import the interface directly from the file
import { OWAPIBlob } from './index';

// When you make the request save assign that OWAPIBlob interface to the response
// Here I'm using request = require('request-promise')
let r: OWAPIBlob = await request({
  uri: `https://owapi.net/api/v3/u/battletag-1234/blob`, // Put the requested URL here
  headers: {
    'User-Agent': 'request'
  },
  json: true
}).catch(console.error);

// If there has been an error with the request, you can find it like this
// Errors ususally are either 404 or "Private" (the profile has been set private)
if (r.error) throw new Error(`Error ${r.error}: ${r.msg}`);

// If it found the profile you can use the autocomplete in your text editor (it may need
// an additional plugin/package)
