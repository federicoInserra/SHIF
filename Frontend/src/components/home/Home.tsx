import "./Home.css";
import { Col, Row } from "react-bootstrap";
import { useEffect, useRef, useState } from "react";
import { H1, H2, H3, Subtitle, Link, Label, Description} from "@leafygreen-ui/typography";
import Layout from "../Layout/Layout";
import { SearchInput, SearchResult } from "@leafygreen-ui/search-input";
import "regenerator-runtime/runtime";
import $ from "jquery";
import ChartsEmbedSDK from "@mongodb-js/charts-embed-dom";
import TextInput from "@leafygreen-ui/text-input";
import Button from "@leafygreen-ui/button"
import TextareaAutosize from 'react-textarea-autosize';
import { Combobox, ComboboxOption } from "@leafygreen-ui/combobox";
import TextArea from "@leafygreen-ui/text-area";
import { Spinner }  from "@leafygreen-ui/loading-indicator";
import * as Realm from "realm-web";
import Modal from "@leafygreen-ui/modal";


export const HomeComponent = () => {
  
  const chartDiv = useRef(null)
  const [userPrompt, setUserPrompt] = useState("")
  const [chart, setChart] = useState(null)
  const [hideChart, setHideChart] = useState(true)
  const [assistantResponse, setAssistantResponse] = useState(null)
  const [selectedCustomer, setSelectedCustomer] = useState("")
  const [customerData, setCustomerData] = useState({})
  const [open, setOpen] = useState(false);

  var isCustomerChoosen = false;

  const sdk = new ChartsEmbedSDK({
    // baseUrl: "https://charts.mongodb.com/charts-john-underwood-udftf"
    baseUrl: process.env.REACT_APP_CHART_BASE_URL
  });

  const filteredChart = sdk.createChart({
    chartId: "65e5a2de-f69b-4c74-877e-f0e3ee1a6e59",
    height: 400,
    width: 700
  });

  useEffect( () => {
  }, [] )


  const loadChart = (user) => {

    const mapCharts = {
      "generalChartID": "65e5a2de-f69b-4c74-877e-f0e3ee1a6e59",
      "100": "65e5ea8e-79a2-4104-8304-bb50e9adf468",
      "101": "73f381d2-3564-416a-877b-2212aa3c8ef7"
    }

    const wordCloudCharts = {
      "generalChartID": "65e5a2de-f69b-4c74-877e-f0e3ee1a6e59",
      "100": "65e7577b-cf4f-49e4-86d4-a3a2a88246cc",
      "101": "ea351a99-3420-4b2a-9f38-83b70145bc25"
    }

    const currentStockValueCharts = {
      "generalChartID": "65e5a2de-f69b-4c74-877e-f0e3ee1a6e59",
      "100": "65e5a82c-fb81-4cea-8531-d253fbe52922",
      "101": "0e677c18-fb34-499d-ba96-0fed0e596de3"
    }

    const chart = sdk.createChart({
      chartId: mapCharts[user],
      height: 400,
      width: 700
    });

    const chartWordCloud = sdk.createChart({
      chartId: wordCloudCharts[user],
      height: 400,
      width: 400
    });

    const chartCurrentStockValue = sdk.createChart({
      chartId: currentStockValueCharts[user],
      height: 400,
      width: 400
    });

    setChart(chart)
    setChart(chartWordCloud)
    setChart(chartCurrentStockValue)
    setHideChart(false)

    chart.render(document.getElementById("chart"))
    .then(() => console.log("chart loaded"))
    .catch(err => console.log(err))

    chartWordCloud.render(document.getElementById("chartWordCloud"))
    .then(() => console.log("chartWordCloud loaded"))
    .catch(err => console.log(err))

    chartCurrentStockValue.render(document.getElementById("chartCurrentStockValue"))
    .then(() => console.log("chartCurrentStockValue loaded"))
    .catch(err => console.log(err))
  }


  const sendPrompt = () => {
    
    setAssistantResponse({...assistantResponse,status:"loading"})

    fetch(`http://localhost:3010/advice?q=${userPrompt}`)
      .then(response => response.json())
      .then(data => {
        setAssistantResponse(data)
        filteredChart.render(document.getElementById("filteredChart"))
        .then(() =>     filteredChart.setFilter({ "symbol": {"$in": data.stocks}})    )
        .catch(err => console.log(err))
      })

  }

  const fetchUserData = (customerId) => {
    
    setSelectedCustomer(customerId)
    isCustomerChoosen = true;

    let body = {"customerId": customerId}
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    }

    fetch(`${process.env.REACT_APP_SERVICES_ENDPOINT}/getCustomerInfo`, requestOptions)
      .then(response => response.json())
      .then(data => {
        console.log(data); 
        const { name, ssn, address, stocks, funds } = data;
        
        const formattedInfo = `
          <h3>Name: ${name}</h3>
          <p>SSN: ${ssn}</p>
          <p>Address: ${address}</p>
          <h4>Stocks:</h4>
          <ul>
            ${stocks.map(stock => `<li>${stock.symbol}: ${stock.quantity}</li>`).join('')}
          </ul>
          <h4>Funds:</h4>
          <ul>
            ${funds.map(fund => `<li>${fund.name}: ${fund.amount}</li>`).join('')}
          </ul>
        `;
        
        document.getElementById('customerData').innerHTML = formattedInfo;
      });

    loadChart(customerId);
}
 

  return (
    <Layout>
      <div>
      <Row className="hero-image">
        <Col>
          <div className="hero-items">
            <H1 className="hero-text">SHIF!</H1>  
            <H2 className="hero-text">Something Happened in Finance</H2>
            <br/>
          </div>
          <Row>
            <TextInput
                  baseFontSize={13}
                  label="Subject *"
                  value={userPrompt}
                  onChange={(event) => setUserPrompt(event.target.value)}
                  optional={false}
                />
          </Row>
          <Col>
            <div className="hero-items">
              <br/>
              <Button variant="baseGreen" onClick={sendPrompt} >Send Prompt</Button>
              <br/>
            </div>
          </Col>
        </Col>
        {
          assistantResponse ?
          assistantResponse.status === "loading" ?
          <div style={{ display: 'flex', flexDirection: 'row' }}>
            <div style={{ flex: 1, backgroundColor:"white", padding:"5px" }}>
              <Spinner description="Loading…"/>
            </div>
          </div>
          :assistantResponse.answer ?
          <>
          <div style={{ display: 'flex', flexDirection: 'row' }}>
            <div style={{ flex: 1, backgroundColor:"white", padding:"5px" }}>
                <div style={{backgroundColor:"white",padding:"5px"}}>
                  {assistantResponse.answer}
                </div>
                <Button onClick={() => setOpen(true)}>Explain search results</Button>
            </div>
            <div style={{ flex: 1, backgroundColor:"white", padding:"5px" }}>
              <div style={{backgroundColor:"white",padding:"5px"}}>
                <Subtitle>Links to relevant market news</Subtitle>
                {
                  assistantResponse.links.slice(0,10).map(link => {
                    return <Link href={link}>{link}</Link>
                  })
                }
              </div>
            </div>
          </div>
          <div style={{ display: 'flex', flexDirection: 'row' }}>
            <div style={{ flex: 1, backgroundColor:"white", padding:"5px" }}>
              <div id="filteredChart"></div>
            </div>
            <div style={{ flex: 1, backgroundColor:"white", padding:"5px" }}>
              <div style={{backgroundColor:"white",padding:"5px"}}>
                <Subtitle>Relevant Stocks</Subtitle>
                {assistantResponse.stocks.join(", ")}
              </div>
            </div>
          </div>
          </>
          :<></>
          :<></>
        }
      </Row>
      <Combobox 
                id="searchOpp"
                className="fieldMargin"
                label={"Select customer"}
                onChange={(value) => fetchUserData(value)}
                value={selectedCustomer}>
                  
                  <ComboboxOption 
                    key="100"
                    value="100"
                  />
                  <ComboboxOption 
                    key="101"
                    value="101"
                  />
                  
              </Combobox>

              <br/>

        
        <div id="container">
          <div id="chart"></div>
          <div id="chartWordCloud"></div>
          <div id="chartCurrentStockValue"></div>
        </div>
        
        <div id="customerData">
          {isCustomerChoosen ?  <p>{JSON.stringify(customerData)} </p> : <p></p>}

          
        </div>
        <Modal open={open} setOpen={setOpen}>
          {assistantResponse && assistantResponse.explanation?<>
          <Subtitle>Search Result Explanations</Subtitle>
          <Label htmlFor="-">Lexical</Label>
          <Description>{assistantResponse.explanation.lexical}</Description>
          <Label htmlFor="-">Semantic</Label>
          <Description>{assistantResponse.explanation.vector}</Description>
          </>
          :<></>
          }
        </Modal>
      </div>
    </Layout>
  );
};