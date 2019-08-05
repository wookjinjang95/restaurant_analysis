var api_key = "NpCtKXFTfpB-32VXJSvE9uPC__UgOl2P8FE0sOUa6KY06lZ3qCMN6qOzvVscwaNeJIP7_zR0EvBf_W2UuOUqrftm9cGp5cJ-4PXjk6raAM_BH082AIe8-OshBthFXXYx"

const yelp = require('yelp-fusion');
const client = yelp.client(api_key);

client.search({
  term: "Kiraku",
  location: "Berkeley Downtown, CA",
}).then(response =>{
  console.log(response.jsonBody.businesses[0].url);
}).catch(e => {
  console.log(e);
});

client.reviews('Kiraku-berkeley').then(response =>{
  console.log(response.jsonBody.reviews[0].text);
}).catch(e =>{
  console.log(e);
});
