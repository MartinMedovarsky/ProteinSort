import './styles/App.css';
import React, { useState } from 'react';
import { useProdSingle, useProdComplex } from './useProdSearch';
import { Dropdown, DropdownButton, FormControl, InputGroup, Container, Jumbotron, Table } from 'react-bootstrap';

export default function App() {
  const [query, setQuery] = useState('')
  const [dropdown, setDropdown] = useState('All Departments')

  function handleSearch(e) {
    setQuery(e.target.value)
  }

  //Handles changing of the dropdown title selected
  function handleDropDown(e){
    setDropdown(e.target.textContent)
  }

  useProdComplex(query, dropdown)

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
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e)}>Diary, Eggs &amp; Fridge</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e)}>Bakery</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e)}>Freezer</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e)}>Pantry</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e)}>Drink</div></Dropdown.Item>
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
              <th>Price / g of Protein</th>
              <th>Total Protein</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td>Mark</td>
              <td>Otto</td>
              <td>@mdo</td>
              <td>Mark</td>
              <td>Otto</td>
              <td>@mdo</td>
            </tr>
            
          </tbody>
        </Table>

      </Container>
      
    </>
  );
}

