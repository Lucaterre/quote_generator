// series of values to retrieve from the API
const valuesToSetFromQG = ['author', 'quote', 'source', 'category']

/**
 * Populate a table with response items
 * @param {Object} results response from API
 * @param {Array} valuesToSet series of values that must be filled in table
 */
const populateTable = (results, valuesToSet) => {
    let table = "";
    for (let key in results){
                // init new data line
                let line = ""
                valuesToSet.forEach((value) => {
                    line+= `<td>${results[key][value]}</td>`;
                })
                // creating a new entry in table data with a new line
                let rowData = `<tr>${line}</tr>`

                // Store entry in "table" content
                table+=rowData;
            }
    document.getElementById("tableContent").innerHTML = table;
}

/**
 * Set total items founded from response
 * @param {String} value
 */
const setTotalResults = (value) => {
    document.getElementById('num_found').textContent = value;
}

// Fetch Quote generator API when user submit query
document.getElementById('form').addEventListener('submit', (event) => {
        // Prevent default behavior
        event.preventDefault();
        // set params to request
        const params = {
            "q":document.getElementById('query_input').value,
            "exact": Boolean(document.getElementById('query_type').checked)
        }
        get_request("api/search", params)
        .then(responseData => {
            setTotalResults(responseData['results']['TotalQuotes']);
            populateTable(responseData['results']['quotes'], valuesToSetFromQG);
        });
    });