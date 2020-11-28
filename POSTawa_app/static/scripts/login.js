document.addEventListener('DOMContentLoaded', function (event) {

    const GET = "GET";
    const POST = "POST";
    const URL = "https://localhost:8081/";

    const LOGIN_FIELD_ID = "login";
    const PASSWORD_FIELD_ID = "password";
    const LOGIN_BUTTON_ID = "button-log-form"
    var HTTP_STATUS = {OK: 200, NOT_FOUND: 404};

    let loginForm = document.getElementById("login-form");

    loginForm.addEventListener("submit", function (event) {
        event.preventDefault();

        tryLogIn();
        setTimeout(function(){
            if (document.getElementById("correctLogin") !== null) {
                console.log("Weszłem w ifa")
                window.location = "/";
            }
        }, 2000);
        
            

    });
    
    function tryLogIn() {
        let loginUrl = URL + "login_user";

        let loginParams = {
            method: POST,
            body: new FormData(loginForm),
            redirect: "follow"
        };

        fetchResponse = fetch(loginUrl, loginParams)
            .then(response => displayInConsoleCorrectResponse(response))
            .catch(err => {
                console.log("Caught error: " + err);
            });
    }

    function displayInConsoleCorrectResponse(correctResponse) {
        let status = correctResponse.status;
        console.log("status " + status)
        let correctLoginInfo = "correctLogin";
        let sucessMessage = "Użytkownik został zalogowany pomyślnie. Za chwilę nastąpi przekierowanie.";
        let warningLoginInfo = "unsuccessfulLogin";
        let warningMessage = "Nieprawidłowy login lub hasło.";

        if (status !== HTTP_STATUS.OK) {
            removeWarningMessage(correctLoginInfo);
            showWarningMessage(warningLoginInfo, warningMessage, LOGIN_BUTTON_ID);
            console.log("Errors: " + correctResponse.errors);
        } else {
            removeWarningMessage(warningLoginInfo);
            showSuccesMessage(correctLoginInfo, sucessMessage, LOGIN_BUTTON_ID);
        }
    }

    function showWarningMessage(newElemId, message, textBoxId) {
        let warningElem = prepareWarningElem(newElemId, message);
        appendAfterElem(textBoxId, warningElem);
    }

    function showSuccesMessage(newElemId, message, textBoxId) {
        let warningElem = prepareWarningElem(newElemId, message);
        warningElem.className = "success-field";
        appendAfterElem(textBoxId, warningElem);
    }

    function removeWarningMessage(warningElemId) {
        let warningElem = document.getElementById(warningElemId);

        if (warningElem !== null) {
            warningElem.remove();
        }
    }

    function prepareWarningElem(newElemId, message) {
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

});