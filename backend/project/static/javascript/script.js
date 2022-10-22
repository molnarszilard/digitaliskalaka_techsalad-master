function toggleBurger() {
    var burger = $('.burger');
    var menu = $('.navbar-menu');
    burger.toggleClass('is-active');
    menu.toggleClass('is-active');
}

// $(".navbar-item.has-dropdown").click(function(e) {
//     if ($(".navbar-burger").is(':visible')) {
//       $(this).toggleClass("is-active");
//     }
// });
// $(".navbar-item > .navbar-link").click(function(e) {
//     if ($(".navbar-burger").is(':visible')) {
//       e.preventDefault();
//     }
// });
// $(window).resize(function(e) {
//   if (!$(".navbar-burger").is(':visible') && $(".navbar-item.has-dropdown.is-active").length) {
//     $(".navbar-item.has-dropdown.is-active").removeClass('is-active');
//   }
// });

function center_map(longitude, latitude) {
    create_marker(parseFloat(latitude), parseFloat(longitude), map, '../static/images/collect.png');
    const center = new google.maps.LatLng(latitude, longitude);
    map.panTo(center);
}

function attend_event(event_id) {
    console.log(event_id);
    data={
        'id': event_id
    }
    $.ajax({
        url: 'https://192.168.100.73:5000/attend_event',
        data: JSON.stringify(data),
        processData: false,
        contentType: 'application/json; charset=utf-8',
        type: 'POST'
    }).done(function (data) {
        alert(data);
    });
}

function show_participants(event_id) {
    console.log(event_id);
    data={
        'id': event_id
    }
    $.ajax({
        url: 'https://192.168.100.73:5000/get_participants',
        data: JSON.stringify(data),
        processData: false,
        contentType: 'application/json; charset=utf-8',
        type: 'POST'
    }).done(function (data) {
        data["emails"].forEach(x => {
            alert(x);
        });
    });
}

$(document).ready(() => {
    const eventForm = document.getElementById("eventform");
    const inputElement = document.getElementById("upload-image");
    const titleElement = document.getElementById("title");
    const descriptionElement = document.getElementById("description");
    const eventdateElement = document.getElementById("eventdate");

    if (inputElement) {
        inputElement.addEventListener("change", handleFiles, false);
    }
    if (eventForm) {
        eventForm.onsubmit = function (event) {
            event.preventDefault();

            const fileList = inputElement.files; /* now you can work with the file list */
            for (let i = 0, numFiles = fileList.length; i < numFiles; i++) {
                new FileUpload(fileList[i]);
            }
            return false;
        };
    }

    function handleFiles() {
        const fileList = inputElement.files; /* now you can work with the file list */
        for (let i = 0, numFiles = fileList.length; i < numFiles; i++) {
            console.log(fileList[i].name);
            console.log(fileList[i].type);
            console.log(fileList[i].size);
        }
    }

    function FileUpload(img) {
        const reader = new FileReader();

        name = img.name;
        type = img.type;
        size = img.size;

        reader.addEventListener("load", function () {
            // convert image file to base64 string

            geolocation.location((position) => {
                data = {
                    'name': name,
                    'type': type,
                    'size': size,
                    'title': titleElement.value,
                    'description': descriptionElement.value,
                    'eventdate': eventdateElement.value,
                    'longitude': position.coords.longitude,
                    'latitude': position.coords.latitude,
                    'bytes': reader.result
                }
                console.log(data);

                $.ajax({
                    url: 'https://192.168.100.73:5000/create_event',
                    data: JSON.stringify(data),
                    processData: false,
                    contentType: 'application/json; charset=utf-8',
                    type: 'POST'
                }).done(function (data) {
                    inputElement.value = "";
                    titleElement.value = "";
                    descriptionElement.value = "";
                    eventdateElement.value = "";
                    alert(data);
                });
            });
        }, false);
        reader.readAsDataURL(img);
    }


    var geolocation = (function () {
        'use strict';

        var geoposition;
        var options = {
            maximumAge: 1000,
            timeout: 15000,
            enableHighAccuracy: false
        };

        function _onSuccess(callback, position) {
            console.log('DEVICE POSITION');
            console.log('LAT: ' + position.coords.latitude + ' - LON: ' + position.coords.longitude);
            geoposition = position
            callback(position);
        };

        function _onError(callback, error) {
            console.log(error)
            callback();
        };

        function _getLocation(callback) {
            navigator.geolocation.getCurrentPosition(
                _onSuccess.bind(this, callback),
                _onError.bind(this, callback),
                options
            );
        }

        return {
            location: _getLocation
        }

    }());

    // geolocation.location(function () {
    //     console.log('finished, loading app.');
    // });
});