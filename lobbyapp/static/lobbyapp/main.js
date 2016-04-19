
function comet_func(events, textStatus) {
    if (events.count > 0) {
        events = events.events;
        for (event_id in events) {
            event = events[event_id];
            switch (+event.etype) {
                case 1:
                    //alert('Вошел новый пользователь: ' + event.user);
                    var newLI = document.createElement("li");
                    newLI.innerHTML = event.user;
                    newLI.setAttribute("name", event.user);
                    $("div#gamers_online_list ol").append(newLI);
                    break;
                case 2:
                    $("div#gamers_online_list ol li[name='" + event.user + "']").remove();
                    //alert('Пользователь вышел: ' + event.user);
                    break;
                case 3:
                    // Лобби добавлено
                    var newRow = document.createElement("tr");
                    var cur_lobby_count;
                    newRow.setAttribute('name', event.lobby.name);
                    cur_lobby_count = $("div#lobbys_x2 table tr").length;
                    var numTD = document.createElement("td");
                    numTD.setAttribute('name', 'num');
                    numTD.innerHTML = cur_lobby_count;
                    var linkTD = document.createElement("td");
                    linkTD.setAttribute("name", "link");
                    var linkA = document.createElement("a");
                    linkA.setAttribute("href", "/join_lobby/" + event.lobby.id);
                    linkA.innerHTML = event.lobby.name;
                    linkTD.appendChild(linkA);
                    var ownerTD = document.createElement("td");
                    ownerTD.setAttribute("name", "owner");
                    ownerTD.innerHTML = event.lobby.owner;
                    var statusTD = document.createElement("td");
                    statusTD.setAttribute("name", "status");
                    statusTD.innerHTML = event.lobby.status;
                    var curcountTD = document.createElement("td");
                    curcountTD.setAttribute("name", "curcount");
                    curcountTD.innerHTML = event.lobby.curr_users_count + "/" + event.lobby.max_users_count;

                    newRow.appendChild(numTD);
                    newRow.appendChild(linkTD);
                    newRow.appendChild(ownerTD);
                    newRow.appendChild(statusTD);
                    newRow.appendChild(curcountTD);
                    if (event.lobby.max_users_count == 2) {
                        $("div#lobbys_x2 table").append(newRow);
                    }
                    else {
                        $("div#lobbys_x4 table").append(newRow);
                    }
                    break;
                case 4:
                    // Лобби удалено
                    if (event.lobby.max_users_count == 2) {
                        $("div#lobbys_x2 table tr[name='" + event.lobby.name + "']").remove();
                    }
                    else {
                        $("div#lobbys_x4 table tr[name='" + event.lobby.name + "']").remove();
                    }
                    if ($("input#lobby_id"))
                        var lobbi_id = document.getElementById("lobby_id");
                        lobby_id = lobby_id.getAttribute("value");
                        if (lobby_id == event.lobby.id) {
                            $("div#actions ul li[name=lobby_id]").html('<a href="/create_lobby/">Создать лобби</a>');
                        }
                    break;
                case 5:
                    // Лобби запущено
                    var val = event.lobby.status;
                    var selector
                    if (event.lobby.max_users_count == 2) {
                        selector = "div#lobbys_x2";
                    }
                    else {
                        selector = "div#lobbys_x4";
                    }
                    selector = selector + " table tr[name='" + event.lobby.name + "'] td[name=status]";
                    console.log(selector);
                    console.log(val);
                    $(selector).html(val);
                    break;
                case 6:
                    // Игрок присоединился к лобби
                case 7:
                    // Игрок покинул лобби
                    var val = event.lobby.curr_users_count + "/" + event.lobby.max_users_count
                    var selector;
                    if (event.lobby.max_users_count == 2) {
                        selector = "div#lobbys_x2 table tr[name='" + event.lobby.name + "'] td[name=curcount]";
                    }
                    else {
                        selector = "div#lobbys_x4 table tr[name='" + event.lobby.name + "'] td[name=curcount]";
                    }
                    $(selector).html(val);
                    break;
                default:
                    break;
            }
        }
    }
}


$(document).ready(function() {

    var intervalID = setInterval(function() {
        $.ajax({
            url: '/get_new_messages/',
            dataType: 'json',
            success: comet_func
        })
    }, 3000)

    if ($("div#deserter")) {
        var deserter_left = setInterval(function() {
            var time_left = +$("span#deserter_left").html() - 1;
            if (time_left >= 0) {
                $("span#deserter_left").html(time_left);
            }
            else {
                $("div#deserter").remove();
            }
        }, 1000)
    }
});