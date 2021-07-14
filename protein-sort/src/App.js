import './styles/App.css';
import React, { useState } from 'react';
import useProdSearch from './useProdSearch';

export default function App() {
  const [query, setQuery] = useState('')

  function handleSearch(e) {
    setQuery(e.target.value)
  }

  useProdSearch(query)
  return (
    <>
      <input type="text" onChange={handleSearch}></input>
      <input type="button"></input>
    </>
  );
}

