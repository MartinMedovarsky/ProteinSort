
//import database
const knex = require('./../db')

//Complex product query
exports.complex = async (req, res) => {
    
}


//Single Product query
exports.productSingle = async (req, res) => {
    //Find specific product in ther database and return it
    knex('itemDATA')
        .where('ID', req.body.id) //find the product based on id
        .then(productData => {
            //send the individual product
            res.json(productData)
        })
        .catch(err => {
            res.json({ message: `There was an error retrieving a single product: ${err}`})
        })
}