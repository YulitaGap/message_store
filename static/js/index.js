function setCookie(obj, exdays = 10) {
    let d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = "data=" + JSON.stringify(obj) + ";" + expires + ";";
}

function getCookie() {
    let name = "data=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let cookie = decodedCookie.split(';');
    for (let i = 0; i < cookie.length; i++) {
        let elem = cookie[i];
        while (elem.charAt(0) === ' ') {
            elem = elem.substring(1);
        }
        if (elem.indexOf(name) === 0) {
            return JSON.parse(elem.substring(name.length, elem.length));
        }
    }
    return {};
}

function initCookie() {
    document.cookie = "data={}; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
}

function clearCookie() {
    document.cookie = "data=; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
}

///////////////////////// STATISTICS HANDLERS /////////////////////////////
function selector_visibility_handle() {
    document.getElementById("button").hidden = this.selectedIndex === 0;
    fields_ids.map((mod) => {
        document.getElementById(mod + "_d").hidden = !modes[this.selectedIndex][mod];
    });
}

// function that save a query to cookie and redirect to view_template to visualize
// usage example in 'author_statistics.html' and 'user_statistics.html'
// need such defined variables in outer scope:
/*
const fields_ids = ["author", "start", "end"]
const modes = [
    {         query number one #0
        author: false,
        start: false,
        end: false,
    }, {        query number one #1
        author: true,
        start: true,
        end: false,
        // important order as in 'fields' array
        query: (author, start) => {
            return `/api/end_point?user=${cookie.id}&`;
        }
    }, ...
]
 */
function submit_handle(event) {
    event.preventDefault();
    ///////////////////// SEND QUERY THROUGH COOKIE //////////////////
    let tmp_cookie = getCookie();
    if (tmp_cookie.query_index === undefined) {
        tmp_cookie.query_index = 1;
    } else {
        tmp_cookie.query_index += 1;
    }
    /////////////////////// RENDER QUERY ///////////////////////
    const params = fields_ids.map((el) => {
        if (modes[mode_selector.selectedIndex][el]) {
            return document.getElementById(el).value;
        }
    }).filter((el) => {
        return el !== undefined;
    });

    tmp_cookie[`${tmp_cookie.query_index}`] =
        modes[mode_selector.selectedIndex].query(...params);
    /////////////////////// RENDER QUERY END ///////////////////

    setCookie(tmp_cookie);
    ///////////////////// SEND QUERY THROUGH COOKIE  END /////////////
    window.open(`/view_catalogue?index=${tmp_cookie.query_index}`, '_blank').focus();
}

///////////////////////// STATISTICS HANDLERS END /////////////////////////

