import React, { useState } from 'react';
import { Modal, Button } from 'react-bootstrap';

export function ProductModal() {
    const [show, setShow] = useState(false);
  
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
  
    return (
      <>
      </>
    );
  }

