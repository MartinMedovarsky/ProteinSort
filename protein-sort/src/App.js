import './styles/App.css';
import React, { useState } from 'react';
import { useProdSingle, useProdComplex } from './useProdSearch';
import { Dropdown, DropdownButton, FormControl, InputGroup, Container, Jumbotron } from 'react-bootstrap';

export default function App() {
  const [query, setQuery] = useState('')
  const [dropdown, setdrop] = useState('All Departments')

  function handleSearch(e) {
    setQuery(e.target.value)
  }

  function handleDropDown(e){
    setdrop(e)
  }

  useProdSingle(query)

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
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e.target.textContent)}>All Departments</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e.target.textContent)}>Meat, Seafood &amp; Deli</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e.target.textContent)}>Fruit &amp; Veg</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e.target.textContent)}>Diary, Eggs &amp; Fridge</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e.target.textContent)}>Bakery</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e.target.textContent)}>Freezer</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e.target.textContent)}>Pantry</div></Dropdown.Item>
            <Dropdown.Item href="#"><div onClick={(e) => handleDropDown(e.target.textContent)}>Drink</div></Dropdown.Item>
          </DropdownButton>
        </InputGroup>

      </Container>
      
    </>
  );
}

