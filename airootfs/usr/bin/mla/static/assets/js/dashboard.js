document.getElementById('form-agents').onsubmit = function () {
    this.reset();
};

selector_one = document.querySelector("#key_type_select");
selector_two = document.querySelector("#key_sec_type_select");
var option, option_text;
const data = JSON.parse(document.getElementById('data-json').textContent);
const skeleton = document.querySelector("#skeleton-box");
const azure = document.querySelectorAll("#azure-input");
const anthropic = document.querySelectorAll("#anthropic-input");
const bedrock = document.querySelectorAll("#bed-rock-input");
var selected;
const input_button = document.querySelector("#input-button");
const name = document.querySelector("#name_key");

selector_one.addEventListener("change", () => {
    var selected = Object.keys(data)[selector_one.selectedIndex - 1];
    selector_two.innerHTML = "";
    option = document.createElement("option");
    option.classList.add("bg-base-100")
    option_text = document.createTextNode("choose llm");
    option.appendChild(option_text);
    selector_two.appendChild(option)
    if (!(skeleton.classList.contains("skeleton"))) {
        name.classList.add("hidden");
        name.removeAttribute("selected");

        document.querySelector("#input-box").classList.remove("hidden");
        azure.forEach(azure => {
            azure.classList.add("hidden");
        })
        bedrock.forEach(bedrock => {
            bedrock.classList.add("hidden");
        })
        anthropic.forEach(anthropic => {
            anthropic.classList.add("hidden");
        })

        input_button.classList.add("hidden");
        skeleton.classList.add("skeleton");

    }


    Object.keys(data).forEach(dataKey => {
        if (selected == dataKey) {

            Object.values(data)[selector_one.selectedIndex - 1].forEach(llm => {
                option = document.createElement("option");
                option.classList.add("bg-base-100")
                option_text = document.createTextNode(llm);
                option.appendChild(option_text);
                selector_two.appendChild(option)
            })
        }
    })
})
selector_two.addEventListener("change", () => {

    if (selector_two.children[selector_two.selectedIndex].value != "choose llm") {
        name.classList.remove("hidden");
        name.setAttribute("selected", "true");

        selected = Object.keys(data)[selector_one.selectedIndex - 1];
        if (selected == "azure") {
            azure.forEach(azure => {

                azure.classList.remove("hidden");
                azure.setAttribute("selected", "true");
            })
            anthropic.forEach(anthropic => {
                anthropic.removeAttribute("selected");
            })
            bedrock.forEach(bedrock => {
                bedrock.removeAttribute("selected");
            })


        } else if (selected == "bedrock") {
            azure.forEach(azure => {
                azure.removeAttribute("selected");
            })
            bedrock.forEach(bedrock => {
                bedrock.classList.remove("hidden");
                bedrock.setAttribute("selected", "true");

            })
            anthropic.forEach(anthropic => {
                anthropic.removeAttribute("selected");
            })

        } else {
            azure.forEach(azure => {
                azure.removeAttribute("selected");
            })
            bedrock.forEach(bedrock => {
                bedrock.removeAttribute("selected");
            })
            anthropic.forEach(anthropic => {
                anthropic.classList.remove("hidden");
                anthropic.setAttribute("selected", "true");
            })
        }
        input_button.classList.remove("hidden");
        skeleton.classList.remove("skeleton");
        document.querySelector("#input-box").classList.add("hidden");

    } else {
        if (!(skeleton.classList.contains("skeleton"))) {
            skeleton.classList.add("skeleton");
            skeleton.innerHTML = `
                                                    <div class="opacity-50 col-start-2 col-span-4 row-start-2" id="input-box">
                                            <p class="text-3xl font-sans text-center"><strong>choose your api key type
                                                first</strong></p>

                                        </div>`

        }
    }
})


window.onload = () => {
    const created = JSON.parse(document.getElementById("created").textContent);

    if (!(created)) {
        alert("no api key to use for this llm.");
    }
};


const key_data_submit = document.querySelector("#key-data-submit");
var active_inputs = document.querySelectorAll("[selected='true']");
var input_datas = {};

key_data_submit.addEventListener("click", () => {
    input_datas = {};

    selected = Object.keys(data)[selector_one.selectedIndex - 1];

    input_datas["company"] = selected;
    active_inputs = document.querySelectorAll("[selected='true']");

    active_inputs.forEach(input => {
        console.log(input.children);
        input_datas[input.children[0].getAttribute("model-data")] = input.children[0].value;
        input.children[0].value = "";

    })

    create_django_api(input_datas);
    create_html_api(input_datas);

})


function create_django_api(data) {


    console.log(data);

    url = "/agents/apikey/create/";

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Required if using CSRF protection
        },
        body: JSON.stringify(data)
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


function create_html_api(key) {

    const mainDiv = document.createElement('div');
    mainDiv.className = 'stat-shadow rounded-3xl w-full';
    mainDiv.style.border = 'gray 1px solid';
    mainDiv.id = 'API';

    const flexDiv = document.createElement('div');
    flexDiv.className = 'flex flex-row';

    const statDiv = document.createElement('div');
    statDiv.className = 'stat simp-bottom-bord';
    statDiv.style.borderRight = '1px solid rgb(179, 179, 179)';

    const statTitleDiv = document.createElement('div');
    statTitleDiv.className = 'stat-title';

    const statValueDiv = document.createElement('div');
    statValueDiv.className = 'stat-value text-secondary w-24';
    statValueDiv.textContent = `${key.name}`;

    statDiv.appendChild(statTitleDiv);
    statDiv.appendChild(statValueDiv);

    flexDiv.appendChild(statDiv);

    mainDiv.appendChild(flexDiv);


    const inputContainerDiv = document.createElement('div');
    inputContainerDiv.className = 'px-4 py-2';

    const label = document.createElement('label');
    label.className = 'flex items-center gap-2 input input-bordered input-secondary';

    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'grow w-full max-w-xs';
    input.disabled = true;

    if (key.anthropic_api_key) {
        input.value = key.anthropic_api_key;
    } else if (key.aws_secret_key) {
        input.value = key.aws_secret_key;
    } else {
        input.value = key.azure_openai_key;
    }

    label.appendChild(input);

    inputContainerDiv.appendChild(label);

    mainDiv.appendChild(inputContainerDiv);

    document.querySelector("#scroll_key").appendChild(mainDiv);
}

const create_agent_inputs = document.querySelectorAll("#create-agent-input");
const create_agent_checks = document.querySelectorAll("#create-agent-checkboxes");
const select_agent_api_key = document.querySelector("#choose_api_key_agent");
const select_llm_agent = document.querySelector("#choose_llm_agent");
const agent_create_button = document.querySelector("#create-agent");
const form_agent = document.querySelector("#agent-form");
var list_keys;
var agent_creation_data = {};
var option, company, options;
const all_ai_types = JSON.parse(document.querySelector("#data-json").textContent);


select_agent_api_key.addEventListener("change", () => {
        select_llm_agent.innerHTML = "";
        options = [];
        if (select_agent_api_key[select_agent_api_key.selectedIndex].innerText != "choose your key") {
            company = select_agent_api_key[select_agent_api_key.selectedIndex].getAttribute("model-company");

            if (company == "azure") {
                console.log(azure);
                all_ai_types["azure"].forEach(azure => {
                    option = document.createElement("option");
                    option.appendChild(document.createTextNode(`${azure}`));
                    option.setAttribute("select-2-model-company", "azure");
                    options.push("option");
                })


            } else if (company == "bedrock") {
                console.log("bedrock");
                console.log(select_agent_api_key);
                console.log(all_ai_types["bedrock"]);
                all_ai_types["bedrock"].forEach(bedrock => {
                    option = document.createElement("option");
                    option.appendChild(document.createTextNode(`${bedrock}`));
                    option.setAttribute("select-2-model-company", "bedrock");
                    console.log(option);
                    options.push(option);

                })


            } else {
                console.log('anthropic');
                all_ai_types["anthropic"].forEach(anthropic => {
                    option = document.createElement("option");
                    option.appendChild(document.createTextNode(`${anthropic}`));
                    option.setAttribute("select-2-model-company", "anthropic")
                    options.push(option);

                })

            }

            option = document.createElement("option");
            option.appendChild(document.createTextNode(`select llm`));
            select_llm_agent.appendChild(option);
            options.forEach(option => {
                select_llm_agent.appendChild(option);
            })
        } else {
            select_llm_agent.innerHTML = "";
            option = document.createElement("option");
            option.classList.add("bg-base-400", "text-secondary");
            option.appendChild(document.createTextNode(`select llm`));
            select_llm_agent.appendChild(option);
        }

    }
)


agent_create_button.addEventListener("click", () => {

    agent_creation_data = {};
    create_agent_inputs.forEach(input => {
        agent_creation_data[input.name] = input.value;
    })

    create_agent_checks.forEach(check_box => {
        agent_creation_data[check_box.name] = check_box.checked;
    })


    if (select_agent_api_key[select_agent_api_key.selectedIndex].value != "choose your key") {
        agent_creation_data["api_key"] = select_agent_api_key[select_agent_api_key.selectedIndex].value;

    }
    if (select_llm_agent[select_llm_agent.selectedIndex - 1] != "select llm") {
        agent_creation_data["LLM"] = select_llm_agent[select_llm_agent.selectedIndex].value;

    }
    console.log(agent_creation_data["company_url"]);
    if (isURLStrict(agent_creation_data["company_url"])) {
        create_django_agents(agent_creation_data);

    } else {
        create_agent_errors({"company_url": "please enter a url"});

    }
    card = createAgentCard(agent_creation_data);
    inner_place = document.querySelector("#agents_place").innerHTML;
    document.querySelector("#agents_place").innerHTML = inner_place+card;

})
function createAgentCard(agent) {
  return `
    <div class="w-full h-18 rounded-3xl my-4 bg-base-200 px-3 py-3" style="border: #1db88e 1px solid" id="agent">
      <div class="flex content-center w-full">
        <div class="avatar">
          <div class="w-12 h-12 rounded-3xl">
            <img src="https://img.daisyui.com/images/stock/photo-1635805737707-575885ab0820.webp"/>
          </div>
        </div>
        <div class="ml-3 w-full">
          <p>${agent.name}</p>
          <hr>
          <div>
            ${agent.LLM ? `<p class="badge badge-neutral">${agent.LLM}</p>` : ''}
            ${agent.job ? `<p class="badge badge-secondary">${agent.job}</p>` : ''}
          </div>
        </div>
      </div>
    </div>
  `;
}

function create_django_agents(data) {

    url = '/agents/create/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Required if using CSRF protection
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            if (Object.keys(data).length < 9) {
                create_agent_errors(data)
            }
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

function create_agent_errors(errors) {
    const alertContainer = document.getElementById('alert-container');

    // Create the alert box
    const alertBox = document.createElement('div');
    alertBox.className = 'bg-red-50 mt-18 border-l-4 border-secondary p-4 rounded-2xl bg-base-400 shadow-lg flex flex-col gap-2 relative';

    // Add a title
    const title = document.createElement('strong');
    title.className = 'text-secondary font-semibold';
    title.textContent = 'Please fix the following errors:';
    alertBox.appendChild(title);

    // Add each error as a list item
    for (const [field, messages] of Object.entries(errors)) {
        const errorItem = document.createElement('div');
        errorItem.className = 'text-secondary';
        errorItem.textContent = `${field}: ${messages.join(', ')}`;
        alertBox.appendChild(errorItem);
    }

    // Add a close button
    const closeButton = document.createElement('button');
    closeButton.className = 'absolute top-2 right-2 text-secondary hover:text-neutral';
    closeButton.innerHTML = '&times;';
    closeButton.addEventListener('click', () => {
        alertContainer.removeChild(alertBox);
    });
    alertBox.appendChild(closeButton);

    // Append the alert box to the container
    alertContainer.appendChild(alertBox);

    // Automatically remove the alert after 10 seconds
    setTimeout(() => {
        if (alertContainer.contains(alertBox)) {
            alertContainer.removeChild(alertBox);
        }
    }, 10000);

}

function isURLStrict(str) {
    try {
        // Prepend "http://" if missing protocol
        new URL(str.startsWith('http') ? str : `http://${str}`);
        return true;
    } catch {
        return false;
    }
}

const { ipcRenderer } = require('electron');

// Back Button
document.getElementById('back-btn').addEventListener('click', () => {
    const mainWindow = require('electron').remote.getCurrentWindow();
    mainWindow.webContents.goBack(); // Navigate back in the browser history
});

// Refresh Button
document.getElementById('refresh-btn').addEventListener('click', () => {
    const mainWindow = require('electron').remote.getCurrentWindow();
    mainWindow.webContents.reload(); // Reload the current page
});


