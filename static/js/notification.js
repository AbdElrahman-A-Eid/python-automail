const root = document.getElementsByTagName('body')[0]
    
function generateAlert(response, title) {
    const div = document.createElement("div");
    var message = '';
    var details = '';
    if (response.status == 200) {
        const ul = document.createElement("ul");
        ul.classList.add("list-disc")
        if ('emails' in response) {
            response.emails.forEach((email)=>{
                li = document.createElement("li");
                li.innerHTML = email;
                li.classList.add("ml-6")
                li.classList.add("text-sm")
                ul.appendChild(li)
            });
            message = `Here are the ${response.count} mail address(es):`
            details = ul.outerHTML
        } else if ('metadata' in response) {
            Object.entries(response.metadata).forEach(([key, value], index)=>{
                li = document.createElement("li");
                li.innerHTML = `<strong>${key}:</strong> ${value}`;
                li.classList.add("ml-6")
                li.classList.add("text-sm")
                ul.appendChild(li)
            });
            message = `Here are the token usage details for the request:`
            details = ul.outerHTML
        }
        type = {
            color : 'green',
            title : title,
            message: message,
            details: details,
            icon : `<path fill="currentColor" d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10s10-4.5 10-10S17.5 2 12 2m-2 15l-5-5l1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9Z"/>`   
        }
    } else {
        type = {
            color : `red`,
            title : title,
            message: `Here is the error message:`,
            details: response.message,
            icon : `<g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"><path d="m10.25 5.75l-4.5 4.5m0-4.5l4.5 4.5"/><circle cx="8" cy="8" r="6.25"/></g>`
        }
    }
    div.innerHTML = `
        <div class="bg-${type.color}-100 border-t-4 border-${type.color}-500 rounded-b text-${type.color}-900 px-4 py-3 shadow-md opacity-100" role="alert" style="position: absolute; top:10px; right: 10px; z-index: 100;">
            <button id="close-notification" class="absolute top-2 right-3 text-gray-700 text-lg">
                &times;
            </button>    
            <div class="flex pr-5">
                <div class="text-${type.color} text-2xl mt-1">${type.icon}</div>
                <div class="py-1"><svg class="fill-current h-6 w-6 text-${type.color}-500 mr-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 30">${type.icon}</svg></div>
                <div>
                    <p class="font-bold">${type.title}</p>
                    <p class="text-sm">${type.message}</p>
                    <p class="text-sm">${type.details}</p>
                </div>
            </div>
        </div>
    `;
    $("html, body").animate({ scrollTop: 0 }, "slow");
    root.insertBefore(div, root.firstChild);
    document.getElementById('close-notification').addEventListener('click', ()=>{
        setTimeout(() => {
            div.classList.remove("opacity-100");
            div.classList.add("opacity-0")
            setTimeout(()=>{
                div.remove()
            }, 1000)
        }, 2000);
    });
}