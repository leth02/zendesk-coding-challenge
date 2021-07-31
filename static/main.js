let TICKETS = {};
let ticketTable = null;

function getTickets() {
    let abortController = new AbortController();
    let id = setTimeout(() => abortController.abort(), 5000);

    fetch('/api/tickets/get', {method: 'GET'})
    .then(response => {
        if (!response.ok) {throw Error(response.status)}
        return response.json();
    })
    .then(processTickets)
    .catch(error => {
        clearTimeout(id);
        console.error('Failed to get tickets: ' + error);
    })
}


function search(searchString, processFn, params) {
    let abortController = new AbortController();
    let id = setTimeout(() => abortController.abort(), 5000);

    fetch('/api/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'search_string': searchString
        })
    })
    .then(response => {
        if (!response.ok) {throw Error(response.status)}
        return response.json();
    })
    .then(json => {
        processFn(json, params);
    })
    .catch(error => {
        clearTimeout(id);
        console.error('Failed to search: ' + error);
    })
}


function addRequesterName(json, params) {
    try {
        console.log(json);
        result = json['results'][0];
        TICKETS[params['ticket_id']]['requester_name'] = result['name'];
        document.getElementById("requester-name").textContent = result['name'];
        
    } catch (error) {
        console.error(error);
    }
}


function processTickets(data) {
    TICKETS = {};
    const tickets = data['tickets'];
    for (const ticket of tickets) {
        TICKETS[ticket['id']] = {
            id: ticket['id'],
            subject: ticket['subject'],
            status: ticket['status'],
            requester_id: ticket['requester_id'],
            created_at: new Date(ticket['created_at']).toString().split(' ').slice(1,5).join(' '),
            type: ticket['type'] ? ticket['type'] : 'ticket',
            priority: ticket['priority'] ? ticket['priority'] : '-',
            description: ticket['description']
        };
    }

    createTicketTable();
}


function displayTicketDescription(description) {
    let ticketDescriptionEl = document.querySelector("#ticketModal #ticket-description")
    ticketDescriptionEl.textContent = "";

    let paragraphStrings = description.split('\n').filter(p => p != "");
    for (const paragraphString of paragraphStrings) {
        const p = document.createElement('p');
        p.textContent = paragraphString;
        ticketDescriptionEl.append(p);
    }
}


function createTicketTable() {
    ticketTable = new Tabulator(document.getElementById("ticket-table"), {
        data: Object.values(TICKETS),
        layout:"fitColumns",
        responsiveLayout:"hide",
        tooltips:true,
        addRowPos:"top",
        pagination:"local",
        paginationSize:25,
        movableColumns:true,
        resizableRows:true,

        rowClick: function(event, row) {
            // open a modal that contains details of the clicked ticket
            const rowData = row['_row']['data'];

            const ticketId = rowData['id'];
            const ticketSubject = rowData["subject"];
            const requesterId = rowData['requester_id'];
            const createdAt = rowData['created_at'];

            const ticket = TICKETS[ticketId];
            document.querySelector("#ticketModal #ticketModalLabel").textContent = ticketSubject;
            document.querySelector('#ticketModal #created-at-time').textContent = createdAt;

            displayTicketDescription(ticket["description"]);
            
            if (ticket['requester_name']) {
                document.getElementById("requester-name").textContent = ticket['requester_name'];
            } 
            else {
                search(`user:${requesterId}`, addRequesterName, {'ticket_id': ticketId});
            }

            ticketModal.toggle();

        },
        
        columns:[
            {title:"Subject", field:"subject", width: "300"},
            {title:"Requester ID", field:"requester_id"},
            {title:"Requested", field:"created_at"},
            {title:"Type", field:"type"},
            {title:"Priority", field:"priority"},
            {title:"id", field: "id", visible: false},
        ]
    });
}

getTickets();

// Crete the Bootstrap ticket modal object
let ticketModal = new bootstrap.Modal(document.getElementById('ticketModal'), {keyboard: true})
let ticketModalElement = document.getElementById("ticketModal");
ticketModalElement.addEventListener("hidden.bs.modal", function(event){
    document.querySelector("#ticketModal #ticketModalLabel").textContent = "";
    document.querySelector("#ticketModal #ticket-description").textContent = "";
})