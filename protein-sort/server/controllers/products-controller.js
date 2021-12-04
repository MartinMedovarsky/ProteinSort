//const path = require('path')

//const dbPath = path.resolve(__dirname, 'db/itemData.db')

const { attachPaginate } = require('knex-paginate');
attachPaginate();


//import database
var knex = require('knex')({
    client: 'mysql',
    connection: {
      host : '127.0.0.1',
      port : 3306,
      user : 'root',
      password : process.env.proteinSortPass,
      database : 'proteinsort'
    }
  })

//Complex product query
exports.complex = async (req, res) => {

    //Maybe perform query first, consider item category, then sort, then pagination, then return page based set?
    var search = req.query.search
    var department = req.query.dep //Limit results to a particular category
    //var sortType = req.body.sortType //What are we sorting by
    //var sortDir = req.body.sortDir  //Sort ascending / descending
    var page = req.query.page 
    var perPage = 20

    //Make deparment equal nothing if all departments are selected
    if (department == "All Departments") {
        department = ""
    } 

    knex
        .select('*')
        .from('itemdata')
        .where('name', 'like', `%${search}%`) //%% chars search for term in any position
        .andWhere('dep', 'like', `%${department}%`)
        .orderBy('PPGP')
        .paginate({ perPage: perPage, currentPage: page, isLengthAware: true})
        .then(productData => {
            //send the individual product
            res.json(productData)
        })
        .catch(err => {
            res.json({ message: `There was an error retrieving the products: ${err}`})
        })
}


//Single Product query
exports.productSingle = async (req, res) => {
    //Find specific product in ther database and return it
    console.log('ID SENT: ' + req.query.id)
    knex
        .select('*')
        .from('itemdata')
        .where('ID', req.query.id) //find the product based on id
        .then(productData => {
            //send the individual product
            res.json(productData)
        })
        .catch(err => {
            res.json({ message: `There was an error retrieving a single product: ${err}`})
        })
}