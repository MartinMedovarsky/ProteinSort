//const path = require('path')

//const dbPath = path.resolve(__dirname, 'db/itemData.db')


//import database
var knex = require('knex')({
    client: 'sqlite3',
    connection: { filename: 'server/db/itemData.db' }
  })

//Complex product query
exports.complex = async (req, res) => {
    
}


//Single Product query
exports.productSingle = async (req, res) => {
    //Find specific product in ther database and return it
    console.log('ID SENT: ' + req.query.id)
    knex
        .select('*')
        .from('itemData')
        .where('ID', 25) //find the product based on id
        .then(productData => {
            //send the individual product
            res.json(productData)
        })
        .catch(err => {
            res.json({ message: `There was an error retrieving a single product: ${err}`})
        })
}