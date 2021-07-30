let TICKETS = {};
let ticketTable = null;

function getTickets() {
    let abortController = new AbortController();
    let id = setTimeout(() => abortController.abort(), 5000);

    fetch("/api/tickets/get", {method: 'GET'})
    .then(response => {
        if (!response.ok) {throw Error(response.status)}
        return response.json();
    })
    .then(processTickets)
    .catch(error => {
        clearTimeout(id);
        console.error("Failed to get tickets: " + error);
    })
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
            created_at: new Date(ticket['created_at']).toString().split(" ").slice(1,5).join(" "),
            type: ticket['type'] ? ticket['type'] : 'ticket',
            priority: ticket['priority'] ? ticket['priority'] : '-',
            description: ticket['description']
        };
    }

    createTicketTable();
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
        
        columns:[
            {title:"Subject", field:"subject", width: "300"},
            {title:"Requester", field:"requester_id"},
            {title:"Requested", field:"created_at"},
            {title:"Type", field:"type"},
            {title:"Priority", field:"priority"},
        ]
    });
}

getTickets();