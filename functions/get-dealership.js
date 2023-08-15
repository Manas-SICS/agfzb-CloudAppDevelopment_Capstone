const express = require('express');
const app = express();
const port = 3000;
const Cloudant = require('@cloudant/cloudant');
 
// Initialize Cloudant connection
function dbCloudantConnect() {
    return new Promise((resolve, reject) => {
        Cloudant({  // eslint-disable-line
            url: "https://55e78b78-d769-452b-b437-52069b827068-bluemix.cloudantnosqldb.appdomain.cloud", 
            maxAttempt: 5, 
            plugins: [ { iamauth: { iamApiKey: '3tN02_CVbex9EoiUmpbWV5ktsBLCxCzgH77fZtfiQQsn' } }, { retry: { retryDelayMultiplier: 4 } } ]
        }, ((err, cloudant) => {
            if (err) {
                console.error('Connect failure: ' + err.message + ' for Cloudant DB');
                reject(err);
            } else {
                let db = cloudant.use("dealerships");
                console.info('Connect success! Connected to DB');
                resolve(db);
            }
        }));
    });
}
 
let dealershipsDB

dbCloudantConnect("dealerships").then((database) => {
    dealershipsDB = database;
}).catch((err) => {
    throw err;
});

app.use(express.json());
app.set('json spaces', 2);

// Define a route to get all dealerships with optional state and ID filters
app.get('/api/dealership', (req, res) => {
    const { state, id } = req.query;

    // If no params, empty selector will be sent and all docs will be retrieved.
    let selector = {};

    if (id) selector.id = parseInt(id);
    if (state) selector.state = state;

    dealershipsDB.find({ selector: selector }, (err, result) => {
        if (err) {
            return res.status(500).send({ error: "Error while quering the database" });
        }

        res.json(result.docs);
    });
});

app.listen(port, () => {
    console.log("Listening to port " + port)
})