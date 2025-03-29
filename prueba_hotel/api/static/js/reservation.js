const hotel = document.getElementById("hotel")
const companions_checkbox = document.getElementById("companions")
const bus_checkbox = document.getElementById("bus_checkbox")
const companion_container = document.getElementById("companions_list");
const add_companion_button = document.getElementById("add_companion")
const buses_list = document.getElementById("buses_list")
const additional_services = document.getElementById("additional_services")
const show_services = document.getElementById("show_services")
const bus_seats = document.getElementById("bus_seats")
const seats = document.getElementsByClassName("seat")

let num = 1

hotel.addEventListener("change", () => {
    if(hotel.value != 0){
        search_rooms(hotel.value)
    }
    if(bus_checkbox.checked){
        bus_checkbox.checked = false
        bus_checkbox.dispatchEvent(new Event("change"));
    }
});

companions_checkbox.addEventListener("change", () => {
    add_companion_button.classList.toggle("hide");
    if (companions_checkbox.checked){
        companion_container.innerHTML = `<label>Ingrese los nombres de los acompañantes:</label><br>`
        addField();
    } else {
        companion_container.innerHTML = "";
        num = 0
    }
});

bus_checkbox.addEventListener("change", () => {
    if (bus_checkbox.checked){
        if(hotel.value == 0){
            buses_list.innerHTML = `<p style="color: red; font-size: 12px">Primero debe seleccionar un hotel</p>`;
        }else{
            console.log(hotel.value)
            search_routes(hotel.value)
        } 
    } else {
        buses_list.innerHTML = "";
        bus_seats.classList.add("hide")
    }
});

show_services.addEventListener("change", () => {
    additional_services.classList.toggle("hide");
    additional_services.scrollIntoView({ behavior: "smooth", block: "start" });
});

function addField() {
    companion_container.innerHTML += `<div class="column">
                                <input type="text" class="companions_fields input" name="companion${num}" id="companion${num}">
                                <button onclick="deleteField('companion${num}', this)" type="button" class="del">Eliminar</button>
                            <div/>`;
    num += 1
}

function deleteField(id, button) {
    let companions = document.getElementsByClassName("companions_fields")
    for(let i = 0; i < companions.length; i++){
        if(companions[i].id == id){
            companions[i].remove()
        }
    }
    button.remove()
}

function available_hotel_rooms(room_num, type){
    return `<option value="${room_num}">${type} ${room_num}</option>`;
}

function companions(){
    return `<label for="">Ingrese el nombre del acompañante:</label><br>
            <input type="text" name="companion" id="companion"><br>`;
}

function search_rooms(num){
    fetch(`/hotel/${num}/rooms`, {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
    }).then(response => response.json()).then(rooms => {
        if (rooms.length > 0){
            let roomsListHTML = "";
            for(let i = 0; i < rooms.length; i++){
                if(rooms[i][3] == "Disponible"){
                    roomsListHTML += available_hotel_rooms(rooms[i][1], rooms[i][0])
                }
            };
            document.getElementById("room").innerHTML = `<option value="0" disabled selected>Seleccione una opción</option>`;
            document.getElementById("room").innerHTML += roomsListHTML;
        }
    });
}

function search_buses(num, ruta, hora){
    fetch(`/bus/${num}`, {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
    }).then(response => response.json()).then(bus => {
        console.log(bus)
        show_bus_seats(bus)
        display_info(num, ruta, hora)
    });
}

function search_routes(num){
    fetch(`/bus/routes/hotel/${num}`, {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
    }).then(response => response.json()).then(routes => {
        for(let i = 0; i < routes.length; i++){
            buses_list.innerHTML += show_routes(routes[i]);
        }
        
    });
}

function show_routes(route){
    return `<div class="routes column">
                <p class="r1 t3 autobus">Autobus #${route[0]}</p>
                <p class="r2 t3">Hora de partida: ${route[3]}</p>
                <button class="reserve" type="button" onclick="search_buses(${route[0]}, ${route[1]}, '${route[3]}')">Más información</button>
            </div>`;
}

function show_bus_seats(bus){
    bus_seats.classList.remove("hide");
    bus_seats.scrollIntoView({ behavior: "smooth", block: "start" });
    const availableSeats = JSON.parse(bus[1]);
    const reservedSeats = JSON.parse(bus[2]);
    for(let i = 0; i < 10; i++){
        seats[i].classList.remove("available", "taken");
        if(availableSeats.includes(Number(seats[i].textContent))){
            console.log(seats[i].textContent)
            seats[i].classList.add("available")
            seats[i].addEventListener("click", () => {
                validate_bus_seat(seats[i])
            });
        }

        if(reservedSeats.includes(Number(seats[i].textContent))){
            console.log(seats[i].textContent)
            seats[i].classList.add("taken")
        }
    }
    
}

function display_info(autobus, ruta, hora){
    document.getElementById("autobus").textContent = `Autobus #${autobus}`
    document.getElementById("ruta").textContent = `Ruta #${ruta}`
    document.getElementById("hora").textContent = `Hora de partida: ${hora}`
    document.getElementById("bus_number_input").value = autobus
}

function validate_bus_seat(seat){
    const selectedSeatsContainer = document.getElementById("selected_seats");
    const input = document.getElementById("selected_seats_input");

    let selectedSeatsInput = JSON.parse(input.value);
    
    seat.classList.toggle("available")
    seat.classList.toggle("choice")
    if (seat.classList.contains("choice")) {
        selectedSeatsContainer.appendChild(seat.cloneNode(true))
        selectedSeatsInput.push(Number(seat.textContent));
    }else{
        const selectedSeats = selectedSeatsContainer.getElementsByClassName("seat");
        for (let i = 0; i < selectedSeats.length; i++) {
            if (selectedSeats[i].textContent === seat.textContent) {
                selectedSeatsContainer.removeChild(selectedSeats[i]);
                selectedSeatsInput = selectedSeatsInput.filter(s => s != seat.textContent);
                break;
            }
        }
    }
    input.value = JSON.stringify(selectedSeatsInput);
}

document.querySelector("form").addEventListener("submit", function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const jsonData = {};

    formData.forEach((value, key) => {
        jsonData[key] = value;
    });

    fetch("/hotel/reservation", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(jsonData)
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error("Error:", error));
});
