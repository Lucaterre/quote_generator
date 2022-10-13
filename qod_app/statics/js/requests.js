/**
 * A generic HTTP requests wrapper
 *
 * @param {string} url endpoint to send a request
 * @param {object} params parameters of the request
 * @param {object} method method of the request
 * @return {Promise<any>} result from request
 */
const request = ( url, params = {}, method = 'GET' ) => {
    let options = {
        method
    };
    if ( 'GET' === method ) {
        if (Object.keys(params).length !== 0){
            url += '?' + ( new URLSearchParams( params ) ).toString();
        }
    } else {
        options.body = JSON.stringify( params );
    }

    return fetch( url, options ).then( response => response.json() );
};

/**
 * Get HTTP request wrapper
 *
 * @param {string} url url to send GET request
 * @param {object} params params associate to the GET request
 * @return {Promise<*>} response from GET request
 */
const get_request = ( url, params ) => request( url, params, 'GET' );

/**
 * Post HTTP request wrapper
 *
 * @param url url to send POST request
 * @param params params associate to the POST request
 * @return {Promise<*>} response from POST request
 */
const post_request = ( url, params ) => request( url, params, 'POST' );
