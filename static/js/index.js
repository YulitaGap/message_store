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
