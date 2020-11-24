document.addEventListener('DOMContentLoaded', function (event) {

    const GET = "GET";
    const POST = "POST";
    const URL = "https://pamiw2020registration.herokuapp.com/";

    const LOGIN_FIELD_ID = "login";

    var HTTP_STATUS = {OK: 200, NOT_FOUND: 404};

    prepareEventOnLoginChange();

    let registrationForm = document.getElementById("registration-form");

    registrationForm.addEventListener("submit", function (event) {
        event.preventDefault();

        console.log("Form submission stopped.");

        var n = event.srcElement.length;
        for (var i = 0; i < n; i++) {
            console.log(event.srcElement[i].value);
        }
    });

    function prepareEventOnLoginChange() {
        let loginInput = document.getElementById(LOGIN_FIELD_ID);
        loginInput.addEventListener("change", updateLoginAvailabilityMessage);
    }

    function updateLoginAvailabilityMessage() {
        let warningElemId = "loginWarning";
        let warningMessage = "Ten login jest już zajęty";

        isLoginAvailable().then(function (isAvailable) {
            if (isAvailable) {
                console.log("Available login!");
                removeLoginWarningMessage(warningElemId);
            } else {
                console.log("NOT available login");
                showLoginWarningMessage(warningElemId, warningMessage);
            }
        }).catch(function (error) {
            console.error("Something went wrong while checking login.");
            console.error(error);
        });
    }

    function showLoginWarningMessage(newElemId, message) {
        let warningElem = prepareLoginWarningElem(newElemId, message);
        appendAfterElem(LOGIN_FIELD_ID, warningElem);
    }

    function removeLoginWarningMessage(warningElemId) {
        let warningElem = document.getElementById(warningElemId);

        if (warningElem !== null) {
            warningElem.remove();
        }
    }

    function prepareLoginWarningElem(newElemId, message) {
        let warningField = document.getElementById(newElemId);

        if (warningField === null) {
            let textMessage = document.createTextNode(message);
            warningField = document.createElement('span');

            warningField.setAttribute("id", newElemId);
            warningField.className = "warning-field";
            warningField.appendChild(textMessage);
        }
        return warningField;
    }

    function appendAfterElem(currentElemId, newElem) {
        let currentElem = document.getElementById(currentElemId);
        currentElem.insertAdjacentElement('afterend', newElem);
    }

    function isLoginAvailable() {
        return Promise.resolve(checkLoginAvailability().then(function (statusCode) {
            if (statusCode === HTTP_STATUS.OK) {
                return false;

            } else if (statusCode === HTTP_STATUS.NOT_FOUND) {
                return true;

            } else {
                throw "Unknown login availability status: " + statusCode;
            }
        }));
    }



    function checkLoginAvailability() {
        let loginInput = document.getElementById(LOGIN_FIELD_ID);
        let baseUrl = URL + "user/";
        let userUrl = baseUrl + loginInput.value;

        return Promise.resolve(fetch(userUrl, {method: GET}).then(function (resp) {
            return resp.status;
        }).catch(function (err) {
            return err.status;
        }));
    }

});