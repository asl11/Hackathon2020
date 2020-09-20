import React, {Component} from 'react';
import './App.css';
import {Navbar, Nav, Image, Container, Row, Col} from 'react-bootstrap/'
import ScrollspyNav from "react-scrollspy-nav";
import Main from './components/Main.jsx';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlay} from "@fortawesome/free-solid-svg-icons";






class App extends Component {
  constructor(props){
    super(props);
    this.state={
      tableData:null,

    }
  }

  state = {
    navBackground: "transparent",
    activeLink: "dummy"

  };

  componentDidMount() {
    document.addEventListener("scroll", () => {
      const backgroundcolor = window.scrollY < 100 ? "transparent" : "white";

      this.setState({ navBackground: backgroundcolor});
    });
  }


  render () {


  return (


    <div className="App">

    {/*  ------- NAVBAR  ------- */}
    <ScrollspyNav
    scrollTargetIds={[
      "home",
      "about",
      "results",
    ]}
    activeNavClass="NAVBAR--active" >
      <Navbar fixed="top" style={{backgroundColor : `${this.state.navBackground}`}} variant="light" expand="lg">
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="mr-auto">
            <Nav.Link className="dummy" href="#home">Home</Nav.Link>
            <Nav.Link href="#about">About</Nav.Link>
            <Nav.Link href="#results">Results</Nav.Link>
          </Nav>
        </Navbar.Collapse>
        <Image style={{height:"5%", width:"5%"}} src={require("./assets/img/logo.png")}/>
      </Navbar>
    </ScrollspyNav>

      {/*  ------- FRONTPAGE  ------- */}
      <header className="masthead" id="home">
          <div  className="d-flex h-100 align-items-center">
              <div className="mx-right text-center wide">
                  {/*<Image style={{height:200, width:200, border:"4px solid #45433a"}}src={require("./assets/img/IMG-4454.jpg")} roundedCircle fluid />*/}
                  <h1 className="mx-auto my-0 text-uppercase">MeetSafe</h1>
                  <h2 className="text-white-50 mx-auto mt-2 mb-5">Dynamic meeting assignment to minimize contact during travel</h2>
                  <a style={{fontStyle : "italic", marginRight:10}} className="btn btn-primary js-scroll-trigger" href="#about">Get Started <FontAwesomeIcon size='xl' style={{marginLeft:10}}icon={faPlay}/></a>
                  <a className="btn btn-primary js-scroll-trigger" href="https://github.com/asl11/Hackathon2020">Github</a>
              </div>
          </div>
      </header>

    {/* ------- ABOUT  ------- */}

    <section id="about" className="resume">
    </section>

    <section style={{backgroundColor:"#BFD2D0"}} id="results">

      {/*-----------RESULTS----------------*/}
      <Container style={{alignItems:"center", alignContent:"center"}} className="imgwrap" fluid>
      <div style={{paddingTop:135}} class="section-title">
        <h2 style={{fontWeight:"bold"}} class="section-title">Run Our Model</h2>
      </div>
           <p style={{paddingBottom : 75}}>
               Upload a xlsx file of meeting schedules and press the run button!
             We'll give you a multiplier <br/> of how many more interactions are created by each
                meeting and the optimal room assignment for the meetings.</p>

      </Container>
      <Main/>
    </section>


      <footer style={{backgroundColor:"#BFD2D0"}} className="footer small text-center"><div className="container">Made by Alex, Chris, Matthew, and Anthony with React/Flask</div></footer>

    </div>
  );
}
}
export default App;

