
import React from 'react';
import DTable from './DTable.jsx';
import ReactLoading from "react-loading";


function DisplayTable(props) {
    if (props.data !== null && props.data !== undefined) {
        console.log("here2");
        return <DTable className={"test"} data={props.data}/>;
    } else if (props.started){
        console.log("here3");
        return <ReactLoading className={"test"} type={"bubbles"}/>
    } else {
        return null;
    }

}
class Main extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            data: null,
            started: false,
        };

        this.handleUploadImage = this.handleUploadImage.bind(this);
    }

    handleUploadImage(ev) {
        ev.preventDefault();
        console.log("here")
        this.setState({started:true});
        const data = new FormData();
        data.append('file', this.uploadInput.files[0]);


        fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: data,
        }).then((response) => {
            response.json().then((body) => {
                console.log(body);
                this.setState({ data: body });
                console.log(this.state.data);
                this.setState({started:false});
            });
        });

    }

    render() {
        return (
            <form onSubmit={this.handleUploadImage}>
                <div>
                    <input className="btn" ref={(ref) => { this.uploadInput = ref; }} type="file" />
                </div>
                <br />
                <div style={{paddingBottom:"5%"}}>
                    <button className="btn btn-primary js-scroll-trigger">Run</button>
                </div>
                <DisplayTable style={{paddingTop:"5%"}} data={this.state.data} started={this.state.started}/>
            </form>


        );
    }
}

export default Main;
