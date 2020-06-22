const Nightmare = require('nightmare'),
  nightmare = Nightmare({ 
    show: true 
  });
const cheerio = require('cheerio');
const url = 'https://www.tripmasters.com/';
let tripTitles;

// Request making using nightmare
nightmare
  .goto(url)
  .wait('body')
  .evaluate(() => document.querySelector('body').innerHTML)
.then(response => {
    tripTitles = getTripTitles(response);
    $(".dvEachPopItinTitle").each((i,elem) => {
      console.log()
    });
}).catch(err => {
  console.log(err);
});

// parse titles from main page
let getTripTitles = (html) => {
  const data=[];
  const $ = cheerio.load(html);


  $('.dvEachPopItinTitle').each((i, elem) => {
    data.push({
      tripTitle : $('h4', elem).text()
    });
  });

  return data;
}

// parse trips from individual trip page
let getTripLocations = (html) => {
    const data = [];
    const $ = cheerio.load(html);

    const title = $('h1 .Blue-Arial16').text()

    $('.itemsR').find('.itemR').each((i, elem) => {
        data.push({
            title : title,
            location : $('div', elem).text()
        });
      });
}