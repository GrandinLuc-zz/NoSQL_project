const data = require('./data.json');
const fs = require('fs')

let listData = data
var months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

function getMonthFromString(mon){
    return months.indexOf((mon.substring(0,3)).toLowerCase())+1
 }

for(let i=0; i<listData.length; i++)
{
    // To format "2021-03-07T21:12:12.039020"
    dateData = listData[i].occuredOn.split(',')
    dayDate = dateData[1].split(' ')[2]
    if(dayDate.length === 1){
        dayDate = '0' + dayDate
    }
    timeDate = dateData[2].split(' ')
    monthDate = getMonthFromString(dateData[1].split(' ')[1]).toString()
    if(monthDate.length === 1){
        monthDate = '0' + monthDate
    }
    hoursDate = timeDate[2].split(':')[0]
    if(timeDate[3] === 'PM'){
        hoursDate = (parseInt(hoursDate)+12).toString()
    }
    else if(timeDate[3] === 'AM' && hoursDate === '12'){
        hoursDate = '00'
    }
    else if(hoursDate.length === 1){
        hoursDate = '0' + hoursDate
    }
    minutesDate = timeDate[2].split(':')[1]
    if(minutesDate.length === 1){
        minutesDate = '0' + minutesDate
    }
    full_date = timeDate[1]+'-'+monthDate+'-'+dayDate+'T'+hoursDate+':'+minutesDate
    listData[i].occuredOn = full_date
}

listData = JSON.stringify(listData)

fs.writeFile('./data.json', listData, (err) => {
    if (err) {
        throw err;
    }
    console.log("JSON data is saved.");
  });




