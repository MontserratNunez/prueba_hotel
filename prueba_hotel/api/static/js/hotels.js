document.addEventListener("DOMContentLoaded", () => {
    search(hotelId, "rooms");
});

function search(num, endpoint){
    fetch(`/hotel/${num}/${endpoint}`, {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
    }).then(response => response.json()).then(rooms => {
        if (rooms.length > 0){
            let roomsListHTML = "";
            rooms.forEach(room =>{
                if (endpoint == "rooms"){
                    roomsListHTML += layout_room(room);
                }else if (endpoint == "locations"){
                    roomsListHTML += layout_location(room);
                }
            });
            document.getElementById("divElements").innerHTML = roomsListHTML;
        }
    });
}

let options = document.querySelectorAll(".options")
options.forEach(button =>{
    button.addEventListener("click", event =>{
        options.forEach(button => {
            button.setAttribute("aria-pressed", "false");
        })
        button.setAttribute("aria-pressed", "true");
    });
});

function layout_room(r){
    return `<div class="card row" onclick="">
        <img class="Img" src="../static/images/room1.jpg">
        <div class="info column">
            <p class="title">${r[0]}</p>
            <p class="description">Habitación ${r[1]}</p>
            <div class="cardFooter center-content">
                <p class="price title">$${r[2]}</p>
                <button class="button third">Ver detalles</button>
            </div>
        </div>
    </div>`;
}

function layout_location(r){
    return `<div class="card center-content row" onclick= "">
        <img class="Img" src="../static/images/${r[1]}.jpg">
        <div class="info column">
            <p class="title">${r[0]}</p>
            <p class="description">${r[2]}</p>
            <div class="cardFooter center-content">
                <button class="button second">Ver detalles</button>
            </div>
        </div>
    </div>`;
}