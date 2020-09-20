
import React from 'react';
import DTable from './DTable.jsx';

function DisplayTable(props) {
    console.log(props.data);
    if (props.data !== null && props.data !== undefined) {
        console.log("hello");
        return <DTable style={{paddingTop:"50%"}} data={props.data}/>;
    } else {
        return null;
    }

}
class Main extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            data: null,
        };

        this.handleUploadImage = this.handleUploadImage.bind(this);
    }

    handleUploadImage(ev) {
        ev.preventDefault();

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
            });
        });
    }

    render() {
        return (
            <form className="form-control-file" onSubmit={this.handleUploadImage}>
                <div>
                    <input className="btn" ref={(ref) => { this.uploadInput = ref; }} type="file" />
                </div>
                <br />
                <div>
                    <button style={{marginBottom:"10%"}} className="btn btn-primary js-scroll-trigger">Run</button>
                </div>
                <DisplayTable class="table" data={this.state.data}/>
            </form>


        );
    }
}

export default Main;
