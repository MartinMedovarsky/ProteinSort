import './styles/App.css';
import React, { useState, useRef, useCallback } from 'react';
import { useProdComplex } from './useProdSearch';
import { Dropdown, DropdownButton, FormControl, InputGroup, Container, Table, Button, Modal, Col, Row, Image} from 'react-bootstrap';
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/js/src/collapse.js";
import ScrollArrow from './scrollArrow'

//Notes for doing modals:
//Have const that represent all data in modal
//onclick of table row call method to get data by item id
//set data in modal const, launch modal

export default function App() {
  const [query, setQuery] = useState('')
  const [dropdown, setDropdown] = useState('All Departments')

  const headers = {"Name":"name","Department":"department","Price":"price","Size":"packSize","$ per g of Protein":"PPGP","Protein per 100g":"pContent"}
  
  const [order, setOrder] = useState("asc")
  const [sortAttribute, setSortAttribute] = useState("PPGP")

  const [pageNumber, setPageNumber] = useState(1)

  const {
    products,
    hasMore,
    loading,
    error
  } = useProdComplex(query, dropdown, pageNumber, order, sortAttribute)

  //Used to load more items when scrolling
  //Whenever an element containing lastProdElementRef
  //Is created the Callback below is called
  const observer = useRef()
  const lastProdElementRef = useCallback(node => {
    //Do nothing if loading
    if (loading) return

    if(observer.current) observer.current.disconnect()
    observer.current = new IntersectionObserver(entries => {
      //Paginate if last element is reached on page and there are more
      if (entries[0].isIntersecting && hasMore){
        console.log("visible")
        setPageNumber(prevPageNumber => prevPageNumber + 1)
      }
    })
    if (node) observer.current.observe(node)
  }, [loading, hasMore])

  function handleSearch(e) {
    //Set single to 0 so page doesnt try to render non-existent item when searching
    setSingle(-1)

    setQuery(e.target.value)
    setPageNumber(1)
  }

  //Handles changing of the dropdown title selected
  function handleDropDown(e){
    //Set single to 0 so page doesn't try to render non-existent item when searching
    setSingle(-1)

    setDropdown(e.target.textContent)
  }

  //Categories are actually departments, because there are too many categories

  //Constants for handling modal 
  const [show, setShow] = useState(false);
  //Product ID for search
  const [single, setSingle] = useState(-1)

  function handleSingle(e) {
    setSingle(e);
    console.log("e: " + e)
    //Display modal
    handleShow()
  }

  //Closing and opening modal
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  function handleHeaderClick(value) {
    if (value == "department"){
      return
    } else if (sortAttribute == value && order == "asc"){
      setOrder("desc")
    } else { setOrder("asc") }
    setSortAttribute(value)
    
    setSingle(-1)

    console.log(sortAttribute, order)
  }


  return (
    <>
      <Container fluid='lg'>
        <Container style={{marginTop:"50px"}}>
          <h1 style={{color:"#178841"}}>Protein Sort</h1>
          <p style={{fontWeight:500}}>Query and sort Woolworths' products based on specific protein and cost information.</p>
        </Container>

        <InputGroup className="mb-3">
          <FormControl aria-label="Text input with dropdown button" onChange={handleSearch} />

          <DropdownButton
            variant="outline-secondary"
            title={dropdown}
            id="input-group-dropdown-2"
            align="end"
          >
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e)}>All Departments</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e)}>Poultry, Meat &amp; Seafood</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e)}>Deli &amp; Chilled Meals</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e)}>Fruit &amp; Veg</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e)}>Dairy, Eggs &amp; Fridge</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e)}>Bakery</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e)}>Freezer</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e)}>Pantry</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e)}>Drinks</div></Dropdown.Item>
          </DropdownButton>
        </InputGroup>

        {/* Conditional to make sure modal doesnt render before api call is made */}
        {single > -1 && 

          <Modal show={show} onHide={handleClose} size="lg">
            <Modal.Header>
              <Modal.Title>{products[single].name}</Modal.Title>
            </Modal.Header>

            <Modal.Body className="show-grid">
              <Container>
                <Row>
                  <Col md={4}>
                    <div></div>
                    <Image src={products[single].imgURLMed} fluid
                    onClick={()=> window.open("https://www.woolworths.com.au/shop/productdetails/" + products[single].ID, "_blank")}></Image>
                  </Col>
                  <Col md={8}>
                    <div class="prodDesc">
                      {products[single].description}
                    </div>
                  </Col>
                </Row>
                <Row></Row>
            </Container>

            </Modal.Body>
            <Modal.Footer>
              <Button variant="secondary" onClick={()=> window.open("https://www.woolworths.com.au/shop/productdetails/" + products[single].ID, "_blank")}>
                Take me to Woolies
              </Button>
              <Button variant="secondary" onClick={handleClose}>
                Close
              </Button>
            </Modal.Footer>
          </Modal>
        }
      

        <Table striped bordered hover>
          <thead>
            <tr>
              <th style={{color:"#178841"}}>#</th>
              {Object.entries(headers).map(([header,value])  => (
                <>
                  {value == sortAttribute && order == "asc" ? <th key={value} style={{color:"#178841"}} onClick={() => handleHeaderClick(value)}>{header} {'\u21E7'}</th> : <></>} 
                  {value == sortAttribute && order == "desc" ? <th key={value} style={{color:"#178841"}} onClick={() => handleHeaderClick(value)}>{header} {'\u21E9'}</th> : <></>}
                  {value != sortAttribute ? <th key={value} onClick={() => handleHeaderClick(value)}>{header} {'\u21E7'}</th> : <></>}
                </>
              ))}
            </tr>
          </thead>
          <tbody>
            
            {products.map((product, index) => {

              var lastProduct = false
              /* If statement in conjunction with ternary operator below determines if final row*/

              if (products.length === index + 1){ lastProduct = true }

              return (
                <>
                <tr ref={lastProduct ? lastProdElementRef : null} key={product.ID} 
                onClick={() => handleSingle(index)} >
                  <td>{index + 1}</td>
                  <td>{product.name}</td>
                  <td>{product.dep}</td>
                  <td>${product.price}</td>
                  <td>{product.packSize}</td>
                  <td>${product.PPGP.toFixed(3)}</td>
                  <td>{product.pContent}g</td>
                </tr>
                </>
              );
            })}
            
          </tbody>
        </Table>  
        <div>{loading && 'Loading...'}</div>
        <div>{error && 'Error'}</div>

        <ScrollArrow></ScrollArrow>

      </Container>
      
    </>
  );
}

