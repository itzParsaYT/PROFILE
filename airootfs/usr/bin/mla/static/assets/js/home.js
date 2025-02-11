const remove_buttons = document.querySelectorAll("#remove");
const agent_options = document.querySelectorAll("#option");
const selected_agent_place = document.querySelector("#selected-agents");
const select = document.querySelector("#select");
var p, svg, path, text_p, option, text_option, resp_text;
var selected = select.selectedIndex;
var agents_list = [];
var svg_list = [];
var select_list = [...select.children];
const closeAlertButton = document.getElementById('close-alert');
const alert = document.getElementById('alert');
const blurBackground = document.getElementById('blur-background');
const alertBox = document.getElementById('alert-box');
var div, p, time, base_div, sec_div, time_node, p_node, side_div, side_p;
const right_chat_body = document.querySelector("#right-chat-body");
const create_task_button = document.querySelector("#create-task");
var task_text;
var tasks_django_list;
const answer_ic = document.querySelector("#answers_ic");
const left_chat_body = document.querySelector("#left-chat-body");


const dots = document.createElement("div");
dots.classList.add("mt-6", "justify-center", "flex", "flex-row")
const dot_1 = document.createElement("div");
dot_1.classList.add("dot-1");
const dot_2 = document.createElement("div");
dot_2.classList.add("dot-2");
const dot_3 = document.createElement("div");
dot_3.classList.add("dot-3");
dots.appendChild(dot_1);
dots.appendChild(dot_2);
dots.appendChild(dot_3);


tasks_list()

async function tasks_list() {
    const url = '/agents/task/list/';

    response = await fetch(url);
    resp_text = await response.text();
    tasks_django_list = await JSON.parse(resp_text);
    console.log(response.status);
    console.log(tasks_django_list);


}

function crate_agent_badge() {
    path = document.createElementNS("http://www.w3.org/2000/svg", "path");

    path.setAttribute("d", "M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z");
    svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");

    svg.setAttribute("width", "16");
    svg.setAttribute("height", "16");
    svg.setAttribute("id", "remove");
    svg.setAttribute("viewBox", "0 0 16 16");
    svg.setAttribute("class", "bi bi-x-lg");

    svg_list.push(svg);
    p = document.createElement("p");
    p.classList.add("badge");
    p.classList.add("badge-secondary");
    p.classList.add("text-xs");
    text_p = document.createTextNode(select[select.selectedIndex].innerText)
    p.setAttribute("index", `${select[select.selectedIndex].getAttribute("index")}`);
    p.setAttribute("id", "selected-agent");

    svg.addEventListener("click", () => {
        option = document.createElement("option");
        option.classList.add("bg-secondary");
        text_option = text_p;
        console.log(select[select.selectedIndex].innerText);
        option.appendChild(text_option);
        p.remove();
        console.log(option);
        select[select.selectedIndex].after(option);
        agents_list.splice(agents_list.indexOf(select[select.selectedIndex].innerText), 1)
    });

    p.appendChild(svg);
    p.appendChild(text_p);

    agents_list.push(select[select.selectedIndex].innerText);
    selected_agent_place.appendChild(p);
    select[select.selectedIndex].remove();
    selected = select.selectedIndex;
    select_list = [...select.children];

}

select.addEventListener("mouseout", () => {
    if (select.selectedIndex != selected) {
        crate_agent_badge();
    }
});


closeAlertButton.addEventListener('click', () => {
    blurBackground.classList.remove('open');
    alertBox.classList.remove('open');
    setTimeout(() => {
        alert.classList.add('hidden');
    }, 500);
});


create_task_button.addEventListener("click", () => {
    if ([...document.querySelectorAll("#selected-agent")].length > 0) {
        const task_body = document.querySelector("#task-body");
        if (task_body.value) {
            right_chat_body.appendChild(dots);
            create_task(task_body.value);
        } else {
            document.querySelector("#error-alert").innerText = "please right a task before sending it.";

            alert.classList.remove('hidden');

            document.querySelector("#error-alert").innerText = "please right a task before sending it.";
            setTimeout(() => {
                blurBackground.classList.add('open');
                alertBox.classList.add('open');
            }, 10);
        }

    } else {
        alert.classList.remove('hidden');
        document.querySelector("#error-alert").innerText = "please add some agents before sending task";
        setTimeout(() => {
            blurBackground.classList.add('open');
            alertBox.classList.add('open');
        }, 10);
    }

})


function create_task(task_body) {
    base_div = document.createElement("div");
    base_div.setAttribute("id", "chat-last-task");
    base_div.classList.add("grid", "w-full", "mt-8", "grid-cols-1", "add-task");

    create_django_task(task_body)
    tasks_list();
    first_div();
    task_second_div(task_body);
    console.log(base_div);
    document.querySelector("#left-chat-body").appendChild(base_div);

    create_answer();

}


function task_second_div(task_body) {
    div = document.createElement("div");
    div.classList.add("h-auto", "min-h-12", "w-full", "block", "rounded-3xl", "bg-neutral", "ml-4", "mr-4", "px-7", "py-5", "col-span-1", "justify-self-center");


    p = document.createElement("p");
    p.classList.add("text-justify", "text-lg");
    p_node = document.createTextNode(task_body);
    p.appendChild(p_node);


    div.appendChild(p);

    sec_div = document.createElement("div");
    sec_div.classList.add("justify-self-end", "mt-8")

    agents_list.forEach(agent => {
        p = document.createElement("p");
        p.classList.add("badge", "badge-secondary", "badge-outline", "text-xs", "mx-2");
        p_node = document.createTextNode(`${agent}`);
        p.appendChild(p_node);

        sec_div.appendChild(p);
    })

    div.appendChild(sec_div);
    base_div.appendChild(div);
}


function create_answer(task_body) {
    base_div = document.createElement("div");
    base_div.setAttribute("id", "chat-last-task")
    base_div.classList.add("grid", "w-full", "mt-8", "grid-cols-1", "add-task");

    first_div();
    answer_second_div(task_body);

    right_chat_body.removeChild(dots);
    right_chat_body.appendChild(base_div);

    get_answer();
}

function create_django_task(task_body) {
    var agents_list_index = [];
    [...document.querySelectorAll("#selected-agent")].forEach(element => {
        agents_list_index.push(parseInt(element.getAttribute("index"), 10));
    })


    const taskData = {
        text: task_body,
        multi_process: agents_list.length > 1 ? true : false,
        task_attachment: null,
        agents: agents_list_index,
        done: false
    };

    const url = '/agents/task/create/';


    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Required if using CSRF protection
        },
        body: JSON.stringify(taskData)
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });


    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}

async function get_answer() {
    const url = '/agents/answer/list/';

    response = await fetch(url);
    resp_text = await response.text();
    tasks_django_list = await JSON.parse(resp_text);
    console.log(response.status);
    console.log(tasks_django_list);
    return tasks_django_list[tasks_django_list.length - 1]
}

function first_div() {
    div = document.createElement("div");
    div.classList.add("flex", "flex-row", "justify-start");

    time = document.createElement("time");
    time.classList.add("text-xs", "opacity-50", "mr-4");
    time.innerText = format_date(tasks_django_list[tasks_django_list.length - 1].timestamp);

    if (agents_list.lenght > 1) {
        p = document.createElement("p");
        p.classList.add("opacity-50", "text-xs");
        p_node = document.createTextNode("multi process");
        p.appendChild(p_node);
        div.appendChild(p);

    }


    div.appendChild(time);

    base_div.appendChild(div);

}


function answer_second_div(task_body) {
    div = document.createElement("div");
    div.classList.add("h-auto", "min-h-12", "w-full", "block", "rounded-3xl", "bg-neutral", "ml-4", "mr-4", "px-7", "py-5", "col-span-1", "justify-self-center");


    p = document.createElement("p");
    p.classList.add("text-justify", "text-lg");
    p_node = document.createTextNode(task_body);
    p.appendChild(p_node);


    div.appendChild(p);

    sec_div = document.createElement("div");
    sec_div.classList.add("jusfify-self-end", "mt-8")

    agents_list.forEach(agent => {
        p = document.createElement("p");
        p.classList.add("badge", "badge-secondary", "badge-outline", "text-xs", "mx-2");
        p_node = document.createTextNode(`${agent}`);
        p.appendChild(p_node);

        sec_div.appendChild(p);
    })

    div.appendChild(sec_div);
    base_div.appendChild(div);
}


function format_date(date) {

    date = new Date(date)

    const monthNames = [
        "Jan.", "Feb.", "Mar.", "Apr.", "May", "June",
        "July", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."
    ];
    const month = monthNames[date.getMonth()];
    const day = date.getDate();
    const year = date.getFullYear();
    let hours = date.getHours();
    const minutes = date.getMinutes();

    const ampm = hours >= 12 ? 'p.m.' : 'a.m.';
    hours = hours % 12 || 12;

    const formattedDate = `${month} ${day}, ${year}, ${hours}:${minutes.toString().padStart(2, '0')} ${ampm}`;

    return formattedDate;
}


answer_ic.addEventListener("click", () => {
    if (answer_ic.children[0].innerText == "Tasks") {
        answer_ic.children[0].innerText = "Answers"
    } else {
        answer_ic.children[0].innerText = "Tasks";

    }
    right = document.querySelector("#right");
    left = document.querySelector("#left");
    right.classList.toggle("-remove");
    left.classList.toggle("-remove");

})









const {ipcRenderer} = require('electron');

document.addEventListener('DOMContentLoaded', () => {
    const minimizeBtn = document.getElementById('minimize-btn');
    const maximizeBtn = document.getElementById('maximize-btn');
    const closeBtn = document.getElementById('close-btn');

    // Minimize Window
    minimizeBtn.addEventListener('click', () => {
        ipcRenderer.send('window-action', 'minimize');
    });

    // Maximize/Restore Window
    maximizeBtn.addEventListener('click', async () => {
        const isMaximized = await ipcRenderer.invoke('window-action', 'is-maximized');
        const path = isMaximized ?
            'M5 3a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2V5a2 2 0 00-2-2H5zm0 2h10v10H5V5z' :
            'M3 3a1 1 0 011-1h12a1 1 0 011 1v12a1 1 0 01-1 1H4a1 1 0 01-1-1V3z';

        maximizeBtn.querySelector('svg').innerHTML = `
      <path fill-rule="evenodd" d="${path}" clip-rule="evenodd"/>
    `;

        ipcRenderer.send('window-action', 'toggle-maximize');
    });

    // Close Window
    closeBtn.addEventListener('click', () => {
        ipcRenderer.send('window-action', 'close');
    });
});




