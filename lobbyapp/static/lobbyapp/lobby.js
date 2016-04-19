
function comet_func(events, textStatus) {
    if (events.count > 0 ) {
        events = events.events;
        for (event_id in events) {
            event = events[event_id];
            switch (+event.etype) {
                case 4:
                    // /Лобби завершено
                    var lobby_owner = document.getElementById("owner").innerHTML;
                    if (event.lobby.owner == lobby_owner) {
                        document.location = "/";
                    }
                    break;
                case 5:
                    // Лобби запущено
                    var lobby_owner = document.getElementById("owner").innerHTML;
                    if (event.lobby.owner == lobby_owner) {
                        $("span#status").html("идет игра");
                        if (!$("span#time_left").length) {
                            var info = $("div#lobby_info");
                            info.html(info.html() + 'До завершения осталось: <span id="time_left">60</span><br/>');
                        }
                    }
                    break;
                case 6:
                    // Игрок присоединился к лобби
                    var lobby_owner = document.getElementById("owner").innerHTML;
                    if (event.lobby.owner == lobby_owner) {
                        var newLI = document.createElement("li");
                        newLI.innerHTML = event.user;
                        newLI.setAttribute("name", event.user);
                        $("div#gamers ol").append(newLI);
                        $("span#count").html("(" + event.lobby.curr_users_count + "/" + event.lobby.max_users_count + ")");
                    }
                    break;
                case 7:
                    // Игрок покинул лобби
                    var lobby_owner = document.getElementById("owner").innerHTML;
                    if (event.lobby.owner == lobby_owner) {
                        $("div#gamers ol li[name='" + event.user + "']").remove();
                        $("span#count").html("(" + event.lobby.curr_users_count + "/" + event.lobby.max_users_count + ")");
                    }
                default:
                    break;
            }
        }
    }

}

function TimeToLeft() {
    if ($("span#time_left")) {
        var lobbyTimeLeft = setInterval(function() {
            var time_left = +$("span#time_left").html() - 1;
            if (time_left >= 0) {
                $("span#time_left").html(time_left);
            }
        }, 1000)
    }
}

$(document).ready(function() {

    TimeToLeft();

    var intervalID = setInterval(function() {
        $.ajax({
            url: '/get_new_messages/',
            dataType: 'json',
            success: comet_func
        })
    }, 3000)
});