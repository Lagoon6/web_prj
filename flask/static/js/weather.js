// city_list =["Seoul,KR"]
// apikey ="1c98556bab77208b58bc7cf6168ff0bb"
// api = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"
// api.openweathermap.org/data/2.5/weather?q=seoul&appid=1c98556bab77208b58bc7cf6168ff0bb&units=metric

const getJSON = function(url, callback){
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function(){
        const status = xhr.status;
        if(status === 200){
            callback(null, xhr.response);
        }else{
            callback(status, xhr.response);
        }
    };
    xhr.send()
};

getJSON('https://api.openweathermap.org/data/2.5/weather?q=seoul&appid=1c98556bab77208b58bc7cf6168ff0bb&units=metric',
    function(err, data){
        if(err !== null){
            alert('죄송합니다. 오류가 발생했습니다.'+ err);
        }else{
            loadWeather(data);
        }
    });

    function loadWeather(data){
        let currentTemp = document.querySelector('.current-temp');
        let minTemp = document.querySelector('.min-temp');
        let maxTemp = document.querySelector('.max-temp');
        let icon = document.querySelector('.icon');
        let weatherIcon = data.weather[0].icon;


        currentTemp.append(`${Math.round(data.main.temp)}˚`);
        maxTemp.append(`${Math.round(data.main.temp_max)}˚`);
        minTemp.append(`${Math.round(data.main.temp_min)}˚`);
        icon.innerHTML = `<img src='http://openweathermap.org/img/wn/${weatherIcon}.png'>`;

    }