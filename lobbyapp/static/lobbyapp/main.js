
$(document).ready(function() {
    $("div#gamers_online").click(function(event){
        //$("div#gamers_online li").fadeToggle(1200);

        var newLI = document.createElement("li");
        newLI.innerHTML = "Пушкин";
        $("div#gamers_online_list ol").append(newLI);
        //event.stopPropagation();
    });
});