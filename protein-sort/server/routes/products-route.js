//import express
const express = require('express')

//import products-controller
const productRoutes = require('./../controllers/products-controller.js')

//create router
const router = express.Router()

router.get('/single', productRoutes.productSingle)

router.get('/complex', productRoutes.complex)

module.exports = router