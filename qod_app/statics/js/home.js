const selectNewRandomQuoteBtn = document.getElementById('changeQuoteBtn');
const boxQuoteSelector = document.querySelector("#box-quote-container");
const elementToSet = {
    "author":document.getElementById('author'),
    "source":document.getElementById('source'),
    "quote":document.getElementById('message')
};

/**
 * Set text values from response object for
 * associate elements.
 *
 * @param {Object} values
 */
const populateElementWithValues = (values) => {
    for (let key in values){
        if (elementToSet.hasOwnProperty(key)){
            elementToSet[key].textContent = values[key];
        }
    }
}

/**
 * Fetch a new quote from Quote Generator API
 */
const fetchNewQuote = () => {
    let valueToSet = {
    "author":"",
    "source":"",
    "quote":""
    }
    get_request("api/random", {})
        .then((responseData) => {
            valueToSet.quote = responseData['results']['quote'];
            valueToSet.author = " - " + responseData['results']['author'];
            if (responseData['results']['source'] !== "unknown") {
                valueToSet.source = ", " + responseData['results']['source'];
            }else{
                valueToSet.source = "";
            }
            populateElementWithValues(valueToSet);
        })
        .catch(error => console.log(error));
}

// Initialise page with new quote
fetchNewQuote();

// Add event listener when user click on button
selectNewRandomQuoteBtn.addEventListener('click', () => { fetchNewQuote()});
