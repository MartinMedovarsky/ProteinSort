const express = require('express');

//Importing dependencies
//const app = express();
//Body parser depricated was using bodyparser.urlencoded and bodypaser.json underneath
const bodyParser = require('body-parser')
const compression = require('compression')
const cors = require('cors')
const helmet = require('helmet')

//Importing routes
const productRouter = require('./routes/products-route')

//Default port for express app
const PORT = 5000;

//Create express app
const app = express()

//Applying middleware
app.use(cors())
app.use(helmet())
app.use(compression())
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())

//Implementing products route
app.use('/products', productRouter)

// Implement 500 error route
app.use(function (err, req, res, next) {
    console.error(err.stack)
    res.status(500).send('Something is broken.')
  })
  
  // Implement 404 error route
  app.use(function (req, res, next) {
    res.status(404).send('Sorry we could not find that.')
  })
  
  // Start express app
  app.listen(PORT, function() {
    console.log(`Server is running on: ${PORT}`)
  })