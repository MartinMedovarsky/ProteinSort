import React, {useState} from 'react';
import { ArrowUpCircle } from "react-bootstrap-icons"
import './styles/App.css';

//This component is taken from <https://betterprogramming.pub/create-a-scroll-to-top-arrow-using-react-hooks-18586890fedc>

const ScrollArrow = () =>{

  const [showScroll, setShowScroll] = useState(false)

  const checkScrollTop = () => {
    if (!showScroll && window.pageYOffset > 400){
      setShowScroll(true)
    } else if (showScroll && window.pageYOffset <= 400){
      setShowScroll(false)
    }
  };

  const scrollTop = () =>{
    window.scrollTo({top: 0, behavior: 'smooth'});
  };

  window.addEventListener('scroll', checkScrollTop)

  return (
        <ArrowUpCircle className="scrollTop" onClick={scrollTop} style={{height: 60, display: showScroll ? 'flex' : 'none'}}/>
  );
}

export default ScrollArrow;