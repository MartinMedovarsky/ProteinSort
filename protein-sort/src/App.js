import './styles/App.css';
import React, { useState, useRef, useCallback } from 'react';
import { useProdSingle, useProdComplex } from './useProdSearch';
import { Dropdown, DropdownButton, FormControl, InputGroup, Container, Jumbotron, Table } from 'react-bootstrap';

export default function App() {
  const [query, setQuery] = useState('')
  const [dropdown, setDropdown] = useState('All Departments')

  const [pageNumber, setPageNumber] = useState(1)

  const {
    products,
    hasMore,
    loading,
    error
  } = useProdComplex(query, dropdown, pageNumber)

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
    setQuery(e.target.value)
    setPageNumber(1)
  }

  //Handles changing of the dropdown title selected
  function handleDropDown(e){
    setDropdown(e.target.textContent)
  }

  //Categories are actually departments, because there are too many categories


  return (
    <>
      <Container fluid='lg'>
        <Jumbotron>
          <h1>Protein Sort</h1>
          <p>Query and sort Woolworths' products based on specific protein and cost information.</p>
        </Jumbotron>

        <InputGroup className="mb-3">
          <FormControl aria-label="Text input with dropdown button" onChange={handleSearch} />

          <DropdownButton
            variant="outline-secondary"
            title={dropdown}
            id="input-group-dropdown-2"
            align="end"
          >
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e)}>All Departments</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e)}>Meat, Seafood &amp; Deli</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e)}>Fruit &amp; Veg</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e)}>Dairy, Eggs &amp; Fridge</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e)}>Bakery</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e)}>Freezer</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e)}>Pantry</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e)}>Drinks</div></Dropdown.Item>
          </DropdownButton>
        </InputGroup>


        <Table striped bordered hover>
          <thead>
            <tr>
              <th>#</th>
              <th>Name</th>
              <th>Department</th>
              <th>Price</th>
              <th>Size</th>
              <th>$ per g of Protein</th>
              <th>Protein per 100g</th>
            </tr>
          </thead>
          <tbody>
            
            {products.map((product, index) => {

              var lastProduct = false
              /* If statement in conjunction with ternary operator below determines if final row*/

              if (products.length === index + 1){ lastProduct = true }

              return (
                <tr ref={lastProduct ? lastProdElementRef : null} key={product.ID}>
                  <td>{index + 1}</td>
                  <td>{product.name}</td>
                  <td>{product.dep}</td>
                  <td>${product.price}</td>
                  <td>{product.packSize}</td>
                  <td>${product.PPGP.toFixed(3)}</td>
                  <td>{product.pContent}g</td>
                </tr>
              );
            })}
            
          </tbody>
        </Table>

        <div>{loading && 'Loading...'}</div>
        <div>{error && 'Error'}</div>

      </Container>
      
    </>
  );
}

