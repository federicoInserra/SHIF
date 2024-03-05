import { Container } from 'react-bootstrap'
import Header from './Header/Header'
import React, { useEffect, useState, useContext } from "react";

interface Props {
  children: JSX.Element
}

const Layout = ({ children }: Props) => {

  return (
    <div className="min-vh-100">

      {
        window.location.href.includes("noLogo") ? null : // Hide if they reach the use the special url for specialist form
        (
          <Header />
        )
      }
      
      <Container fluid className="main-content bg-light">
        {children}
      </Container>
    </div>
  )
}

export default Layout