import './styles/App.css';
import React, { useState } from 'react';
import { useProdSingle, useProdComplex } from './useProdSearch';
import { Dropdown, DropdownButton, FormControl, InputGroup, Container, Jumbotron } from 'react-bootstrap';

export default function App() {
  const [query, setQuery] = useState('')

  function handleSearch(e) {
    setQuery(e.target.value)
  }

  useProdSingle(query)
  return (
    <>
      <Container fluid='lg'>
        <Jumbotron>
          <h1>Protein Sort</h1>
          <p>Query and sort Woolworths' products based on specific protein and cost information.</p>
        </Jumbotron>

        <InputGroup className="mb-3">
          <FormControl aria-label="Text input with dropdown button" />

          <DropdownButton
            variant="outline-secondary"
            title="Dropdown"
            id="input-group-dropdown-2"
            align="end"
          >
            <Dropdown.Item href="#">Action</Dropdown.Item>
            <Dropdown.Item href="#">Another action</Dropdown.Item>
            <Dropdown.Item href="#">Something else here</Dropdown.Item>
            <Dropdown.Divider />
            <Dropdown.Item href="#">Separated link</Dropdown.Item>
          </DropdownButton>
        </InputGroup>

      </Container>


      <input type="text" onChange={handleSearch}></input>
      <button class="btn btn-primary" type="submit">Button</button>
      
    </>
  );
}

