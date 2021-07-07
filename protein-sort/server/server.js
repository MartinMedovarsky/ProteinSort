const express = require('express');

//Importing dependencies
//const app = express();
const express = require('express')
const bodyParser = require('body-parser')
const compression = require('compression')
const cors = require('cors')
const helmet = require('helmet')


app.get('/api/products', (req, res) => {
    const products = [
        {id: 1, name: 'apple', price: '123'},
        {id: 2, name: 'Bread', price: '22'},
        {id: 3, name: 'Cabbage', price: '32'}
    ];

    res.json(products);
});

const port = 5000;

app.listen(port, () => console.log(`Server started on port ${port}`));